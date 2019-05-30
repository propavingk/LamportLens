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
