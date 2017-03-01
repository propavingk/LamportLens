"""Account record model and parsing.

The document format is line-oriented JSON (JSONL). Each line is one account
record. Validation is strict about fields that carry meaning and liberal
about unknown keys. Invalid lines are collected with their line numbers and
reported as findings; parsing continues.
"""
from __future__ import annotations

