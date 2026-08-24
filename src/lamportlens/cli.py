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
    bands.add_argument("input", type=Path, help="account snapshot (JSONL)")
    bands.add_argument("--preset", choices=sorted(RATE_PRESETS), default=None)

    owners = sub.add_parser("owners", help="per-owner summary only")
    owners.add_argument("input", type=Path, help="account snapshot (JSONL)")
    owners.add_argument("--preset", choices=sorted(RATE_PRESETS), default=None)

    return parser


def resolve_rate(lamports_per_byte: int | None, preset: str | None) -> int:
    if lamports_per_byte is not None:
        if lamports_per_byte <= 0:
            print("lamportlens: lamports-per-byte must be > 0", file=sys.stderr)
            raise SystemExit(2)
        return lamports_per_byte
    if preset is not None:
        return RATE_PRESETS[preset]
    return DEFAULT_LAMPORTS_PER_BYTE


def load(path: Path) -> tuple:
    if not path.exists():
        print(f"lamportlens: input not found: {path}", file=sys.stderr)
        raise SystemExit(2)
    if not path.is_file():
        print(f"lamportlens: input is not a file: {path}", file=sys.stderr)
        raise SystemExit(2)
    try:
        return parse_file(path)
    except OSError as exc:
        print(f"lamportlens: cannot read {path}: {exc}", file=sys.stderr)
        raise SystemExit(2)


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    records, errors = load(args.input)

    if args.command == "bands":
        rate = resolve_rate(None, args.preset)
        report = audit(records, rate)
        for band in report.bands:
            print(f"{band.label}: accounts {band.count}, locked {band.locked}")
        return 1 if errors else 0

    if args.command == "owners":
        rate = resolve_rate(None, args.preset)
        report = audit(records, rate)
        ranked = sorted(
            report.owners.values(), key=lambda o: (-o.locked, -o.accounts, o.owner)
        )
        for owner in ranked:
            print(
                f"{owner.owner}  accounts {owner.accounts} "
                f"underfunded {owner.underfunded} locked {owner.locked}"
            )
        if not ranked:
            print("no owners present in snapshot")
        return 1 if errors else 0

    rate = resolve_rate(args.lamports_per_byte, args.preset)
    report = audit(records, rate)
    analysis = Analysis(
        source=str(args.input),
        report=report,
        parse_errors=errors,
        list_limit=max(0, args.limit),
    )
    if args.format == "json":
        payload = json.dumps(render_json(analysis), indent=2, sort_keys=False)
    else:
        payload = render_text(analysis)
    if args.output is not None:
        args.output.write_text(payload, encoding="utf-8", newline="\n")
    else:
        sys.stdout.write(payload)
    return 1 if analysis.findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
