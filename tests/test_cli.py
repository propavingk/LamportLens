"""End to end tests through the CLI entry point."""
from __future__ import annotations

import contextlib
import io
import json
import unittest
from pathlib import Path

from lamportlens.cli import main

SAMPLES = Path(__file__).resolve().parents[1] / "samples"


def run(args: list[str]) -> tuple[int, str]:
    buffer = io.StringIO()
    with contextlib.redirect_stdout(buffer):
        code = main(args)
    return code, buffer.getvalue()


class ExitCodeTests(unittest.TestCase):
    def test_clean_snapshot_exits_zero(self):
        code, output = run(["audit", str(SAMPLES / "clean-snapshot.jsonl")])
        self.assertEqual(code, 0)
        self.assertIn("FINDINGS: 0", output)

    def test_snapshot_exits_one(self):
        code, output = run(["audit", str(SAMPLES / "snapshot.jsonl")])
        self.assertEqual(code, 1)
        self.assertIn("FINDINGS: 3", output)

    def test_broken_lines_exit_one_with_parse_errors(self):
        code, output = run(["audit", str(SAMPLES / "broken-lines.jsonl")])
        self.assertEqual(code, 1)
        self.assertIn("records: 2", output)
        self.assertIn("parse errors: 7", output)

    def test_missing_input_exits_two(self):
        with self.assertRaises(SystemExit) as caught:
            run(["audit", str(SAMPLES / "nope.jsonl")])
        self.assertEqual(caught.exception.code, 2)

    def test_version_exits_zero(self):
        with self.assertRaises(SystemExit) as caught:
            run(["--version"])
        self.assertEqual(caught.exception.code, 0)


class FormatTests(unittest.TestCase):
    def test_json_shape(self):
        buffer = io.StringIO()
        with contextlib.redirect_stdout(buffer):
            code = main(["audit", str(SAMPLES / "snapshot.jsonl"), "--format", "json"])
        self.assertEqual(code, 1)
        payload = json.loads(buffer.getvalue())
        self.assertEqual(payload["records"], 44)
        self.assertEqual(payload["findings"], 3)
        self.assertEqual(payload["lamports_per_byte"], 6333)
        self.assertEqual(len(payload["underfunded"]), 3)
        self.assertEqual(len(payload["bands"]), 7)
        self.assertIn("totals", payload)
