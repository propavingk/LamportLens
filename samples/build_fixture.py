"""Deterministic builder for the LamportLens sample fixtures.

These JSONL files are synthetic test vectors, not captures. This script
rebuilds them byte for byte:

- samples/clean-snapshot.jsonl: 12 accounts, every one exempt, one executable
  program excluded from the rent comparison. Zero findings, exit 0.
- samples/snapshot.jsonl: 44 accounts across every data band, including three
  underfunded accounts, several accounts held at exactly the minimum, one
  barely above it, and two executable programs. Exit 1.
- samples/broken-lines.jsonl: validation errors only, plus two good records.

Owner program ids that appear are real, well-known Solana program addresses
(system, SPL token, associated token, token-2022, BPF upgradeable loader).
Account addresses are synthetic and clearly patterned; no real account is
represented.

Balances are chosen to sit on the arithmetic boundaries of the current
lamports-per-byte step (6333): an SPL token account of 165 bytes has a
minimum of (128 + 165) * 6333 = 1,855,569 lamports, and a zero-byte account
has a minimum of 128 * 6333 = 810,624 lamports. The historical rate (6960)
gives the familiar 2,039,280 and 890,880 lamports for the same sizes.
"""
from __future__ import annotations

import json
from pathlib import Path

SYSTEM = "11111111111111111111111111111111"
TOKEN = "TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA"
TOKEN_2022 = "TokenzQdBNbLqP5VEhdkAS6EPFLC1PHnBqCXEpPxuEb"
ASSOCIATED = "ATokenGPvbdGVxr1b2hvZbsiqW5xWH25efTNsLJA8knL"
LOADER = "BPFLoaderUpgradeab1e11111111111111111111111"

TOKEN_ACCOUNT_LEN = 165
TOKEN_MIN = (128 + TOKEN_ACCOUNT_LEN) * 6333
ZERO_MIN = 128 * 6333


def address(index: int) -> str:
    body = "AbCdEfGhJkMnPqRsTuVwXyZ123456789AbCdEf"
    return ("FixTure" + f"{index:03d}" + body)[:44]


def record(address_value, lamports, data_len, owner, executable=False):
    obj = {
        "address": address_value,
        "lamports": lamports,
        "data_len": data_len,
        "owner": owner,
    }
    if executable:
        obj["executable"] = True
    return obj


def build_clean() -> list[dict]:
    records = []
    for i in range(10):
        records.append(record(address(i), 2_500_000, TOKEN_ACCOUNT_LEN, TOKEN))
    records.append(record(address(10), 9_000_000, 0, SYSTEM))
    records.append(record(address(11), 500_000, 300_000, LOADER, executable=True))
    return records


def build_snapshot() -> list[dict]:
    records = []
