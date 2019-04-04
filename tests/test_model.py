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

    def test_executable_true_is_kept(self):
        record = parse_record(
            {"address": "A", "lamports": 1, "data_len": 0, "owner": "O", "executable": True},
            1,
        )
        self.assertTrue(record.executable)

    def test_missing_address_is_rejected(self):
        with self.assertRaises(FormatError):
            parse_record({"lamports": 1, "data_len": 0, "owner": "O"}, 3)

    def test_empty_address_is_rejected(self):
        with self.assertRaises(FormatError):
            parse_record(
                {"address": "", "lamports": 1, "data_len": 0, "owner": "O"}, 3
            )

    def test_negative_lamports_is_rejected(self):
        with self.assertRaises(FormatError):
            parse_record(
                {"address": "A", "lamports": -1, "data_len": 0, "owner": "O"}, 3
            )

    def test_data_len_over_max_is_rejected(self):
        with self.assertRaises(FormatError):
            parse_record(
                {
                    "address": "A",
                    "lamports": 1,
                    "data_len": 10_485_761,
                    "owner": "O",
                },
                3,
            )

    def test_string_lamports_is_rejected(self):
        with self.assertRaises(FormatError):
            parse_record(
