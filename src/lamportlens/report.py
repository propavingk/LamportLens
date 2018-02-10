"""Deterministic text and JSON rendering.

The text report is line oriented so two runs diff cleanly in git. Lists are
truncated with an explicit `... N more` line, never silently cut. Lamport
amounts are printed raw, in lamports, because this tool never converts units
on the reader's behalf.
"""
from __future__ import annotations

from dataclasses import dataclass

from .audit import AuditReport, statuses_in_order
from .rent import STATUS_UNDERFUNDED

LIST_LIMIT = 10


@dataclass
class Analysis:
    source: str
    report: AuditReport
    parse_errors: list[tuple[int, str]]
    list_limit: int = LIST_LIMIT

    @property
    def findings(self) -> int:
        return self.report.findings + len(self.parse_errors)


def render_text(analysis: Analysis, limit: int | None = None) -> str:
    limit = analysis.list_limit if limit is None else limit
    report = analysis.report
    lines: list[str] = []
    lines.append("LAMPORTLENS REPORT")
    lines.append(f"input: {analysis.source}")
    lines.append(
        f"records: {report.record_count} | "
        f"lamports per byte: {report.lamports_per_byte} | "
        f"parse errors: {len(analysis.parse_errors)}"
    )
    lines.append("")
    lines.append("STATUS COUNTS")
    for status in statuses_in_order(report):
        lines.append(f"  {status}: {report.status_counts.get(status, 0)}")
    lines.append("")
    lines.append("TOTALS")
    lines.append(f"  locked in exemptions: {report.total_locked}")
    lines.append(f"  balances observed: {report.total_balance}")
    lines.append(f"  underfunded deficit: {report.total_deficit}")
    lines.append(f"  reclaimable on close: {report.reclaimable}")
    lines.append("")
    lines.append(f"UNDERFUNDED (first {limit}, smallest surplus first)")
    for assessment in report.underfunded[:limit]:
        lines.append(
            f"  {assessment.record.address} "
            f"owner {assessment.record.owner} "
            f"lamports {assessment.record.lamports} "
            f"deficit {-assessment.surplus}"
        )
    if len(report.underfunded) > limit:
        lines.append(f"  ... {len(report.underfunded) - limit} more")
    if not report.underfunded:
        lines.append("  none")
    lines.append("")
    lines.append(f"BANDS (first {limit})")
    for band in report.bands:
        lines.append(f"  {band.label}: accounts {band.count}, locked {band.locked}")
    lines.append("")
    lines.append(f"OWNERS (top {min(5, limit)} by locked lamports)")
    ranked = sorted(
        report.owners.values(), key=lambda o: (-o.locked, -o.accounts, o.owner)
    )
    for owner in ranked[: min(5, limit)]:
        lines.append(
            f"  {owner.owner}  accounts {owner.accounts} "
            f"underfunded {owner.underfunded} locked {owner.locked}"
        )
    if not ranked:
        lines.append("  none")
    lines.append("")
    lines.append(f"PARSE ERRORS (first {limit})")
    for number, message in analysis.parse_errors[:limit]:
        lines.append(f"  {message}")
    if len(analysis.parse_errors) > limit:
        lines.append(f"  ... {len(analysis.parse_errors) - limit} more")
    if not analysis.parse_errors:
        lines.append("  none")
    lines.append("")
    lines.append(f"FINDINGS: {analysis.findings}")
    return "\n".join(lines) + "\n"


def render_json(analysis: Analysis) -> dict:
    report = analysis.report
    return {
        "input": analysis.source,
        "records": report.record_count,
        "lamports_per_byte": report.lamports_per_byte,
        "findings": analysis.findings,
        "status_counts": {
            status: report.status_counts.get(status, 0)
            for status in statuses_in_order(report)
        },
        "totals": {
            "locked": report.total_locked,
