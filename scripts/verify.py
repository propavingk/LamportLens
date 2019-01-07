"""Executable quality gate for LamportLens.

Runs eight mechanical checks over the repository and prints one line per
check. Exit code 0 when every check passes, 1 otherwise.

    python scripts/verify.py

The checks implement the standing lessons for this project tree. A claim of
correctness is the exit code of this script, not a sentence in a report.
"""
from __future__ import annotations

import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "docs" / "assets"

TEXT_EXTENSIONS = {
    ".py", ".md", ".svg", ".yml", ".yaml", ".toml", ".cff", ".jsonl",
    ".txt", ".cfg", ".ini", ".editorconfig", ".gitattributes", ".gitignore",
    ".html", ".css", ".js", ".mjs", ".ts", ".json", ".rs", ".go", ".sh",
}

BANNED_TERMS = [
    "AI powered", "seamless", "revolutionary", "enterprise-grade",
    "next generation", "cutting edge", "blazing fast", "production ready",
    "battle tested", "lightning fast", "effortless",
]

# Assembled from parts so this file does not contain the forms it searches
# for: a checker that flags itself is not a checker.
