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

    def test_no_deficit(self):
        self.assertEqual(self.report.total_deficit, 0)
        self.assertEqual(self.report.underfunded, [])


class SnapshotTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        records, errors = parse_file(SAMPLES / "snapshot.jsonl")
        assert not errors
        cls.report = audit(records)

    def test_status_counts(self):
        self.assertEqual(self.report.status_counts.get(STATUS_UNDERFUNDED), 3)
        self.assertEqual(self.report.status_counts.get(STATUS_AT_MINIMUM), 7)
        self.assertEqual(self.report.status_counts.get("barely-above"), 1)
        self.assertEqual(self.report.status_counts.get(STATUS_FUNDED), 31)
        self.assertEqual(self.report.status_counts.get(STATUS_EXCLUDED), 2)

    def test_findings_are_the_underfunded_accounts(self):
        self.assertEqual(self.report.findings, 3)
        addresses = [a.record.address for a in self.report.underfunded]
        self.assertEqual(len(addresses), 3)

    def test_total_deficit_is_the_sum_of_the_three(self):
        # 1,855,569 - 1,600,000 + 1,855,569 - 1,200,000 + 810,624 - 700,000
        expected = 255_569 + 655_569 + 110_624
        self.assertEqual(self.report.total_deficit, expected)

    def test_zero_byte_band(self):
        band = next(b for b in self.report.bands if b.label == "0 bytes")
        self.assertEqual(band.count, 3)
        self.assertEqual(band.locked, 3 * 810_624)

    def test_executable_accounts_are_not_in_bands(self):
        total_banded = sum(b.count for b in self.report.bands)
        self.assertEqual(total_banded, self.report.record_count - 2)

    def test_system_owner_summary(self):
        owner = self.report.owners["11111111111111111111111111111111"]
        self.assertEqual(owner.accounts, 2)
