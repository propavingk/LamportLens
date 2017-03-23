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


def _require_int(obj: dict, key: str, line: int, minimum: int, maximum: int | None = None) -> int:
    if key not in obj:
        raise FormatError(f"line {line}: missing required field '{key}'")
    value = obj[key]
    if isinstance(value, bool) or not isinstance(value, int):
        raise FormatError(f"line {line}: field '{key}' must be an integer")
    if value < minimum:
        raise FormatError(f"line {line}: field '{key}' must be >= {minimum}")
    if maximum is not None and value > maximum:
        raise FormatError(f"line {line}: field '{key}' must be <= {maximum}")
    return value


def parse_record(obj: object, line: int) -> AccountRecord:
    """Validate one decoded JSON value into an AccountRecord."""
    if not isinstance(obj, dict):
        raise FormatError(f"line {line}: record must be a JSON object")
    address = _require_non_empty_str(obj, "address", line)
    lamports = _require_int(obj, "lamports", line, minimum=0)
    data_len = _require_int(obj, "data_len", line, minimum=0, maximum=MAX_ACCOUNT_DATA_LEN)
    owner = _require_non_empty_str(obj, "owner", line)
    executable = False
    if "executable" in obj and obj["executable"] is not None:
        if not isinstance(obj["executable"], bool):
            raise FormatError(f"line {line}: field 'executable' must be a boolean")
        executable = obj["executable"]
    return AccountRecord(
