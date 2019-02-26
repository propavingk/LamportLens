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
