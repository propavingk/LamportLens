"""Cross-engine parity check for LamportLens.

Runs the Python core and the TypeScript verifier on the same fixtures and
compares the numbers they report. This is a build-time check, not part of the
offline tool: neither implementation spawns the other at runtime.

Usage (from the repository root, after `cd verifier && npm run build`):

    python scripts/parity.py

Exit 0 when every fixture agrees, 1 otherwise.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERIFIER = ROOT / "verifier" / "dist" / "verify.js"
FIXTURES = ["clean-snapshot.jsonl", "snapshot.jsonl", "broken-lines.jsonl"]

STATUS_KEYS = [
    "underfunded",
    "at-minimum",
    "barely-above",
    "funded",
    "executable-excluded",
]
TOTAL_KEYS = ["locked", "balance", "deficit", "reclaimable"]


def python_report(fixture: Path) -> dict:
    env = dict(os.environ, PYTHONPATH=str(ROOT / "src"))
    result = subprocess.run(
        [sys.executable, "-m", "lamportlens", "audit", str(fixture), "--format", "json"],
        capture_output=True,
        text=True,
        env=env,
