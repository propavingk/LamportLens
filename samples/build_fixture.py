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
