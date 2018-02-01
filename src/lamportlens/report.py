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
