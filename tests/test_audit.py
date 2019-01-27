"""Tests for the snapshot audit over the fixtures."""
from __future__ import annotations

import unittest
from pathlib import Path

from lamportlens.audit import audit
from lamportlens.model import parse_file
from lamportlens.rent import STATUS_AT_MINIMUM, STATUS_EXCLUDED, STATUS_FUNDED, STATUS_UNDERFUNDED

SAMPLES = Path(__file__).resolve().parents[1] / "samples"


class CleanSnapshotTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        records, errors = parse_file(SAMPLES / "clean-snapshot.jsonl")
        assert not errors
        cls.report = audit(records)

    def test_counts(self):
        self.assertEqual(self.report.record_count, 12)
        self.assertEqual(self.report.status_counts.get(STATUS_FUNDED), 11)
        self.assertEqual(self.report.status_counts.get(STATUS_EXCLUDED), 1)
        self.assertEqual(self.report.findings, 0)
