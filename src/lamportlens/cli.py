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
