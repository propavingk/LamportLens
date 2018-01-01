"""LamportLens: rent-exempt and balance hygiene for Solana account snapshots.

The package is offline and deterministic. It reads a JSONL export of account
records, validates every line, and reports which accounts hold less than the
rent-exempt minimum, where storage bonds concentrate, and how lamports are
