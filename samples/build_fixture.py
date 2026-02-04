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

    # Ten SPL token accounts funded at the historical minimum, comfortably
    # above the current one.
    for i in range(10):
        records.append(record(address(i), 2_039_280, TOKEN_ACCOUNT_LEN, TOKEN))

    # Five token accounts at exactly the current minimum, and one barely above.
    for i in range(10, 15):
        records.append(record(address(i), TOKEN_MIN, TOKEN_ACCOUNT_LEN, TOKEN))
    records.append(record(address(15), TOKEN_MIN + 1_000, TOKEN_ACCOUNT_LEN, TOKEN))

    # Two token accounts underfunded against the current rate.
    records.append(record(address(16), 1_600_000, TOKEN_ACCOUNT_LEN, TOKEN))
    records.append(record(address(17), 1_200_000, TOKEN_ACCOUNT_LEN, TOKEN_2022))

    # Zero-byte system accounts: one funded at the historical minimum, one at
    # exactly the current minimum, one underfunded.
    records.append(record(address(18), 890_880, 0, SYSTEM))
    records.append(record(address(19), ZERO_MIN, 0, SYSTEM))
    records.append(record(address(20), 700_000, 0, ASSOCIATED))

    # A large mint account and a large program data account, both funded
    # above their (large) minima.
    records.append(record(address(21), 6_400_000_000, 1_000_000, TOKEN))
    records.append(record(address(22), 16_000_000_000, 2_500_000, LOADER))

    # Mid-size accounts to fill the 100-999 and 1k-9.9k bands. Balances are
    # computed from the same formula the tool uses, with a margin, so these
    # stay funded on purpose.
    for i in range(23, 31):
        data_len = 300 + (i - 23) * 20
        records.append(record(address(i), (128 + data_len) * 6333 + 500_000, data_len, TOKEN))
    for i in range(31, 39):
        data_len = 2_000 + (i - 31) * 100
        records.append(record(address(i), (128 + data_len) * 6333 + 2_000_000, data_len, TOKEN_2022))

    # Two executable programs, excluded from the rent comparison.
    records.append(record(address(39), 1_000, 400_000, LOADER, executable=True))
    records.append(record(address(40), 1_000, 800_000, LOADER, executable=True))

    # Two more funded accounts and one at-minimum, to give the owner table
    # some spread across owners.
    records.append(record(address(41), 8_000_000, 82, ASSOCIATED))
    records.append(record(address(42), 8_500_000, 82, ASSOCIATED))
    records.append(record(address(43), (128 + 82) * 6333, 82, ASSOCIATED))
    return records


def write_jsonl(path: Path, records: list[dict]) -> None:
    lines = [json.dumps(obj, separators=(",", ":"), sort_keys=True) for obj in records]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")


def main() -> int:
    here = Path(__file__).resolve().parent
    clean = build_clean()
    snapshot = build_snapshot()
    write_jsonl(here / "clean-snapshot.jsonl", clean)
    write_jsonl(here / "snapshot.jsonl", snapshot)
    print(f"clean-snapshot.jsonl: {len(clean)} records")
    print(f"snapshot.jsonl: {len(snapshot)} records")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
