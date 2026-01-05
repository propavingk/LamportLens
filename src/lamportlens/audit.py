"""Snapshot audit: statuses, storage bands, owner concentration.

Every decision this module makes is a pure function of the records and the
active lamports-per-byte rate. Nothing depends on wall-clock time, locale or
hash ordering that is not sorted.
"""
from __future__ import annotations

from dataclasses import dataclass, field

from .model import MAX_ACCOUNT_DATA_LEN, AccountRecord
from .rent import (
    DEFAULT_LAMPORTS_PER_BYTE,
    STATUS_AT_MINIMUM,
    STATUS_BARELY_ABOVE,
    STATUS_EXCLUDED,
    STATUS_FUNDED,
    STATUS_UNDERFUNDED,
    AccountAssessment,
    assess,
)

BANDS: list[tuple[str, int, int]] = [
    ("0 bytes", 0, 0),
    ("1-99", 1, 99),
    ("100-999", 100, 999),
    ("1k-9.9k", 1_000, 9_999),
    ("10k-99k", 10_000, 99_999),
    ("100k-999k", 100_000, 999_999),
    ("1M and above", 1_000_000, MAX_ACCOUNT_DATA_LEN),
]


@dataclass
class OwnerSummary:
    owner: str
    accounts: int = 0
    underfunded: int = 0
    locked: int = 0
    balance: int = 0


@dataclass
class BandSummary:
    label: str
    count: int = 0
    locked: int = 0


@dataclass
class AuditReport:
    record_count: int = 0
    lamports_per_byte: int = DEFAULT_LAMPORTS_PER_BYTE
    assessments: list[AccountAssessment] = field(default_factory=list)
    status_counts: dict[str, int] = field(default_factory=dict)
    underfunded: list[AccountAssessment] = field(default_factory=list)
    bands: list[BandSummary] = field(default_factory=list)
    owners: dict[str, OwnerSummary] = field(default_factory=dict)
    total_locked: int = 0
    total_balance: int = 0
    total_deficit: int = 0
    reclaimable: int = 0

    @property
    def findings(self) -> int:
        return len(self.underfunded)


def band_label(data_len: int) -> str:
    for label, low, high in BANDS:
        if low <= data_len <= high:
            return label
    return BANDS[-1][0]


def audit(
    records: list[AccountRecord],
    lamports_per_byte: int = DEFAULT_LAMPORTS_PER_BYTE,
) -> AuditReport:
    report = AuditReport(
        record_count=len(records),
        lamports_per_byte=lamports_per_byte,
        bands=[BandSummary(label=label) for label, _, _ in BANDS],
    )
    band_index = {band.label: band for band in report.bands}
    counts: dict[str, int] = {}

    for record in records:
        assessment = assess(record, lamports_per_byte)
        report.assessments.append(assessment)
        counts[assessment.status] = counts.get(assessment.status, 0) + 1
        if assessment.status == STATUS_UNDERFUNDED:
            report.underfunded.append(assessment)
            report.total_deficit += -assessment.surplus
        if assessment.status != STATUS_EXCLUDED:
            report.total_locked += assessment.minimum
            report.total_balance += record.lamports
            if assessment.status in (STATUS_AT_MINIMUM, STATUS_BARELY_ABOVE):
                report.reclaimable += record.lamports
            band = band_index[band_label(record.data_len)]
            band.count += 1
            band.locked += assessment.minimum
            owner = report.owners.setdefault(record.owner, OwnerSummary(owner=record.owner))
            owner.accounts += 1
            owner.locked += assessment.minimum
            owner.balance += record.lamports
            if assessment.status == STATUS_UNDERFUNDED:
                owner.underfunded += 1
        else:
            owner = report.owners.setdefault(record.owner, OwnerSummary(owner=record.owner))
            owner.accounts += 1

    report.status_counts = counts
    report.underfunded.sort(key=lambda a: (a.surplus, a.record.address))
    return report


def status_count(report: AuditReport, status: str) -> int:
    return report.status_counts.get(status, 0)


def statuses_in_order(report: AuditReport) -> list[str]:
    return [
        STATUS_UNDERFUNDED,
        STATUS_AT_MINIMUM,
        STATUS_BARELY_ABOVE,
        STATUS_FUNDED,
        STATUS_EXCLUDED,
    ]

// draft note 1417
