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
                {"address": "A", "lamports": "1", "data_len": 0, "owner": "O"}, 3
            )

    def test_non_boolean_executable_is_rejected(self):
        with self.assertRaises(FormatError):
            parse_record(
                {"address": "A", "lamports": 1, "data_len": 0, "owner": "O", "executable": "yes"},
                3,
            )

    def test_unknown_keys_are_ignored(self):
        record = parse_record(
            {"address": "A", "lamports": 1, "data_len": 0, "owner": "O", "rent_epoch": 4},
            1,
        )
        self.assertEqual(record.owner, "O")


class ParseTextTests(unittest.TestCase):
    def test_broken_lines_collect_errors_and_keep_going(self):
        text = (SAMPLES / "broken-lines.jsonl").read_text(encoding="utf-8")
        records, errors = parse_text(text)
        self.assertEqual(len(records), 2)
        self.assertEqual(len(errors), 7)
        self.assertEqual([number for number, _ in errors], [2, 3, 4, 5, 6, 7, 8])

    def test_blank_lines_are_ignored(self):
        text = "\n\n" + json.dumps(
            {"address": "A", "lamports": 1, "data_len": 0, "owner": "O"}
        ) + "\n"
        records, errors = parse_text(text)
        self.assertEqual(len(records), 1)
        self.assertEqual(errors, [])


if __name__ == "__main__":
    unittest.main()
