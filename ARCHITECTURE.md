# Architecture

This document describes the modules that exist in `src/lamportlens/` and in
`verifier/src/`, the data flow between them, and why the boundaries fall where
they do. It was written by reading the source, not by planning an ideal
system.

## Shape of the program

LamportLens is a batch auditor. One process reads one snapshot, validates
every line, classifies every account against the rent-exempt minimum for the
active lamports-per-byte rate, and renders one report. There is no server, no
daemon, no state on disk, and no configuration file.

The TypeScript verifier in `verifier/` is a second implementation of the same
arithmetic. It exists to cross-check the rules, not to be called by the Python
core. The two programs share the format contract (`docs/FORMAT.md`), not code.

## Python modules

```
src/lamportlens/
  __init__.py       __version__ only
  __main__.py       python -m lamportlens entry point
  model.py          AccountRecord, validation, JSONL parsing
  rent.py           the rent-exempt arithmetic and rate presets
  audit.py          statuses, storage bands, owner summaries
  report.py         deterministic text and JSON rendering
  cli.py            argparse, subcommands, exit codes, file IO
```

### model.py

Owns everything that can be said about a single line. `AccountRecord` is
frozen, so no later stage can mutate parsed data. `parse_record` applies every
validation rule in one place, and `parse_text` collects errors with their line
numbers instead of raising. A malformed snapshot is a finding about the
snapshot, not a reason to stop reading the file.

Validation is strict about fields that carry meaning. `data_len` is bounded by
`MAX_ACCOUNT_DATA_LEN`, Solana's own 10 MiB account size limit, because an
account larger than that cannot exist and a snapshot claiming otherwise has a
bug in its exporter. Unknown keys are ignored, because different exporters add
fields this tool has no opinion about.

### rent.py

The arithmetic lives here and nowhere else. Two constants define it:
`ACCOUNT_STORAGE_OVERHEAD` (128 bytes, the space an empty account occupies)
and the active `lamports_per_byte`, with the named SIMD-0437 steps kept as
presets. The formula is:

```
minimum_balance = (128 + data_len) * lamports_per_byte
```

`assess()` maps one record plus a rate to a status. The status vocabulary is
deliberately small: underfunded, at-minimum, barely-above, funded, and the
separate executable-excluded bucket. Executable accounts are excluded from the
rent comparison on purpose; the loader holds programs, and applying the
account rule to them would produce phantom findings at scale.

### audit.py

Folds a list of records into the aggregates a reader needs: status counts,
the total lamport bond represented by the exemptions, the underfunded deficit,
what a closure sweep would return, per-band concentration, and a per-owner
summary. Every aggregate is a pure function of the assessments.

Band edges live here, not in the report, because they are analysis policy:
where "small" ends and "large" begins is a decision about the data, and the
renderer should not be able to change it silently.

### report.py

Two renderers over one `Analysis` object. The text renderer is line oriented
and truncates every list with an explicit `... N more` line. The JSON renderer
mirrors the same numbers with stable key order. Both are pure functions of the
analysis: no clock, no randomness, no locale reads. Lamport amounts are
printed raw, in lamports, because this tool never converts units on the
reader's behalf.

