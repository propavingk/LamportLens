"""Tests for account record parsing and validation."""
from __future__ import annotations

import json
import unittest
from pathlib import Path

from lamportlens.model import FormatError, parse_record, parse_text

SAMPLES = Path(__file__).resolve().parents[1] / "samples"


class ParseRecordTests(unittest.TestCase):
    def test_minimal_valid_record(self):
        record = parse_record(
            {"address": "A", "lamports": 1, "data_len": 0, "owner": "O"}, 1
        )
        self.assertEqual(record.data_len, 0)
        self.assertFalse(record.executable)
