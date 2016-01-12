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
