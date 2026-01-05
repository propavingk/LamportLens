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
        cwd=str(ROOT),
    )
    return json.loads(result.stdout)


def verifier_report(fixture: Path) -> dict:
    result = subprocess.run(
        ["node", str(VERIFIER), str(fixture)],
        capture_output=True,
        text=True,
        cwd=str(ROOT),
    )
    return json.loads(result.stdout)


def compare(name: str, py: dict, ts: dict) -> list[str]:
    disagreements: list[str] = []

    def check(key: str, py_value, ts_value) -> None:
        if py_value != ts_value:
            disagreements.append(f"{key}: python={py_value} typescript={ts_value}")

    check("records", py["records"], ts["records"])
    check("lamports_per_byte", py["lamports_per_byte"], ts["lamports_per_byte"])
    for status in STATUS_KEYS:
        check(f"status.{status}", py["status_counts"].get(status), ts["status_counts"].get(status))
    for key in TOTAL_KEYS:
        check(f"totals.{key}", py["totals"][key], ts["totals"][key])
    py_bands = {band["label"]: (band["accounts"], band["locked"]) for band in py["bands"]}
    ts_bands = {band["label"]: (band["accounts"], band["locked"]) for band in ts["bands"]}
    check("bands", py_bands, ts_bands)
    py_under = [(a["address"], a["deficit"]) for a in py["underfunded"]]
    ts_under = [(a["address"], a["deficit"]) for a in ts["underfunded"]]
    check("underfunded", py_under, ts_under)
    check("parse_error_count", len(py["parse_errors"]), len(ts["parse_errors"]))
    check("findings", py["findings"], ts["findings"])
    return disagreements


def main() -> int:
    if not VERIFIER.exists():
        print(f"verifier build missing at {VERIFIER}")
        print("run: cd verifier && npm install && npm run build")
        return 1
    failures = 0
    for name in FIXTURES:
        fixture = ROOT / "samples" / name
        py = python_report(fixture)
        ts = verifier_report(fixture)
        disagreements = compare(name, py, ts)
        if disagreements:
            failures += 1
            print(f"{name}: DIFF " + "; ".join(disagreements))
        else:
            print(f"{name}: OK")
    print(f"parity: {len(FIXTURES) - failures}/{len(FIXTURES)} fixtures agree")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())

// draft note 1415
