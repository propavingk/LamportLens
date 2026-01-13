# Contributing to LamportLens

Thanks for considering a contribution. LamportLens is an offline auditor: it
reads an account snapshot, validates it, and reports which accounts hold less
than the rent-exempt minimum at a chosen lamports-per-byte rate. Every output
is deterministic, and that property is part of the contract.

This file explains the setup, the checks, and what a good change looks like
here.

## Setup

The Python core needs Python 3.11 or newer and nothing else. The package uses
the standard library only.

```bash
git clone <repository>
cd lamportlens
export PYTHONPATH=src
```

The TypeScript verifier needs Node 20 or newer and installs a single build
dependency:

```bash
cd verifier
npm install
npm run build
```

## The checks

Run all of these before opening a pull request. They are the same checks CI
runs.

```bash
PYTHONPATH=src python -m unittest discover -s tests -v
cd verifier && npm run typecheck && npm run build && npm test && cd ..
python scripts/parity.py
python scripts/verify.py
```

`make test`, `make parity` and `make verify` wrap the same commands.

The parity script is the important one when you touch arithmetic. Python and
TypeScript implement the same rules independently, and any change to the rent
formula, the status thresholds, the band edges, or the totals must land in
both. A change that only edits one side will fail parity, and that failure is
the point of the check.

## The rate policy

The rent-exempt minimum depends on `lamports_per_byte`, which the SIMD-0437
schedule reduces in steps from 6,960 down to 696. The default in
`src/lamportlens/rent.py` must always be the step that is live on mainnet,
with a dated comment naming the source. Changing the default is a release
note, not a silent edit: snapshots audited before and after a default change
will report different deficits, and the changelog must say so.

## What a good change looks like

- One topic per pull request. A rule change does not also reorganize a module.
- Tests for behavior changes. A new validation rule needs a failing line in
  `samples/broken-lines.jsonl` or an in-memory record; a new arithmetic rule
  needs an anchor value computed by hand in both test suites.
- Re-run the CLI and the verifier after a change, and paste the real output
  into the pull request description if the report shape changed.
- Keep the report deterministic. If an output byte depends on wall-clock time,
  unsorted map iteration, or randomness, it is a bug.
- Line-oriented output. New sections start with a label line and use two
  spaces of indentation, matching the existing report.

## Standing rules

1. Python: standard library only. TypeScript: the verifier may depend on
   `typescript` and `@types/node` for building and nothing else. No runtime
   dependencies in either language.
2. No network access anywhere in the shipped code. The tools read files and
   write to stdout or to an explicitly named output path.
3. No em dash in any file, in any of its three forms. `scripts/verify.py`
   checks this mechanically.
4. Fixtures are honest. Synthetic fixtures are labelled as synthetic in
   `samples/README.md`, and `samples/build_fixture.py` must rebuild them byte
   for byte. Never present a constructed snapshot as a capture.
5. Numbers that appear in documentation, assets or commit messages must come
   from a real run. If you did not run it, do not write it.
6. Meaningful exit codes stay stable: 0 clean, 1 findings, 2 usage or input
   error.
7. The JSON output keys in `docs/FORMAT.md` are a contract. Adding keys is a
   minor change; renaming or removing them needs a changelog entry.
8. Program ids in fixtures may be real, well-known addresses (system, SPL
   token, token-2022, the loader). Account addresses must stay synthetic and
   clearly patterned, and no fixture may contain private keys or seeds, ever.

## Commit messages

Use conventional prefixes, one topic each:

```
feat: add a per-owner deficit column
fix: treat a zero balance at zero length as underfunded, not at-minimum
docs: record the SIMD-0437 step dates in docs/RATE_SCHEDULE.md
test: anchor the 165-byte minimum in both implementations
```

## Reviewing your own diff

Before asking for review, read your diff once as if it were someone else's:

- Does the change alter arithmetic? Then both implementations and parity moved
  together, and the changelog says which rate applies.
- Does the change alter aggregation? Then the tests that assert totals,
  bands, or owner summaries were updated, not deleted.
- Did you touch an asset? Then `python scripts/verify.py` exits 0 and the XML
  still parses.
- Did you add a number to a document? Where did it come from?

## Reporting bugs

Open an issue with the exact command you ran, the smallest snapshot that shows
the problem, and the real output. Two or three JSONL lines usually reproduce a
report bug. If the snapshot came from a real cluster and contains addresses
you would rather not publish, replace every address with a synthetic one of
the same shape; the arithmetic depends only on lamports and data length.
