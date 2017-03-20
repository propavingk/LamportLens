"""Account record model and parsing.

The document format is line-oriented JSON (JSONL). Each line is one account
record. Validation is strict about fields that carry meaning and liberal
about unknown keys. Invalid lines are collected with their line numbers and
reported as findings; parsing continues.
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

# Solana's own limit: MAX_ACCOUNT_DATA_LEN, 10 MiB.
MAX_ACCOUNT_DATA_LEN = 10_485_760


class FormatError(ValueError):
    """Raised when a single record fails validation."""


@dataclass(frozen=True)
class AccountRecord:
    address: str
    lamports: int
    data_len: int
    owner: str
    executable: bool
    line: int


def _require_non_empty_str(obj: dict, key: str, line: int) -> str:
    if key not in obj:
        raise FormatError(f"line {line}: missing required field '{key}'")
    value = obj[key]
    if not isinstance(value, str) or not value:
        raise FormatError(f"line {line}: field '{key}' must be a non-empty string")
    return value
