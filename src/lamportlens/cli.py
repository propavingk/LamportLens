"""Command line interface.

Exit codes, documented in docs/FORMAT.md:

- 0: every account is exempt, no parse errors
- 1: findings are present (underfunded accounts or parse errors)
- 2: usage error (bad arguments, missing or unreadable input)
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from . import __version__
from .audit import audit
from .model import parse_file
from .rent import DEFAULT_LAMPORTS_PER_BYTE, RATE_PRESETS
from .report import Analysis, render_json, render_text


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="lamportlens",
        description="Rent-exempt and balance hygiene for captured Solana account snapshots.",
    )
    parser.add_argument("--version", action="version", version=f"lamportlens {__version__}")
    sub = parser.add_subparsers(dest="command", required=True)

    audit_cmd = sub.add_parser("audit", help="full audit report")
    audit_cmd.add_argument("input", type=Path, help="account snapshot (JSONL)")
    audit_cmd.add_argument("--format", choices=("text", "json"), default="text")
    audit_cmd.add_argument("--limit", type=int, default=10, help="list entries shown per section")
    audit_cmd.add_argument("--output", type=Path, default=None, help="write the report to a file")
    audit_cmd.add_argument(
        "--lamports-per-byte",
        type=int,
        default=None,
        help=f"override the rate (default {DEFAULT_LAMPORTS_PER_BYTE})",
    )
    audit_cmd.add_argument(
        "--preset",
        choices=sorted(RATE_PRESETS),
        default=None,
        help="named SIMD-0437 step or the historical rate",
    )

    bands = sub.add_parser("bands", help="storage bands only")
