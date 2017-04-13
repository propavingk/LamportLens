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

