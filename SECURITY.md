# Security Policy

## Supported versions

| Version | Supported |
|---------|-----------|
| 0.1.x   | Yes       |

## What LamportLens is, in security terms

LamportLens is an offline auditor. It reads a JSONL export of account records,
validates the fields, and prints a report about rent-exempt balances. It does
not:

- open sockets, make HTTP requests, or resolve DNS names;
- connect to a cluster, hold keys, sign anything, or send transactions;
- execute anything from the input, including field values that resemble code
  or paths;
- write files by default; `--output` writes exactly one report file to the
  path you name.

A snapshot is public information by construction: account addresses, lamports,
data lengths, owners, and the executable flag are all visible to any node.
The tool's own design rule is that a snapshot file must never contain private
keys or seed phrases, and the fixtures in this repository follow that rule.

The realistic threat model for a tool like this is malformed input:

1. **Parser crashes.** A crafted line might trigger an unhandled exception.
   The parser is covered by tests for every documented validation rule, and a
   crash is treated as a bug, not a hardening incident.
2. **Resource consumption.** A very large snapshot consumes memory for the
   record list and the aggregates. There is no streaming mode yet; a
   multi-gigabyte snapshot is not a supported input today.
3. **Output rendering.** Addresses and owner program ids are printed as they
   appear in the input. If your snapshot contains control characters in
   string fields, your terminal will render them. The tool does not sanitize
   output beyond what the JSON parser already strips.
4. **Path handling in `--output`.** The path is used exactly as given. Running
   the tool as a privileged user against an attacker-controlled output path is
   the same risk class as any CLI that writes a file.

## What LamportLens does not protect against

- It does not verify that the snapshot is truthful. It checks internal
  consistency against the rent formula, not provenance.
- It does not validate addresses or program ids. Any non-empty string is
  accepted; the tool compares and prints them, it does not verify them.
- It does not model fees. The exemption numbers it reports are bonds, not
  costs, and closing an account is a transaction that costs fees the tool
  does not compute.
- It is not a monitoring system. A clean report on a stale snapshot says
  nothing about the current cluster state.

## Handling snapshots responsibly

Snapshots are usually harmless, but they can be sensitive in aggregate: a full
dump of your program's accounts reveals your user base size, your storage
costs, and the exact lamport flows you operate. Treat large snapshots like any
internal dataset. The fixtures in this repository are synthetic and exist so
you can test without any real data at all.

## Reporting a vulnerability

Report suspected vulnerabilities privately through the repository security
advisory feature, or contact the maintainers at [MAINTAINER CONTACT]. Please
include:

- the smallest snapshot that reproduces the issue (two or three lines are
  usually enough);
- the exact command line;
- the observed output or crash, pasted verbatim.

You can expect an acknowledgement within a few days. Fixes ship in a patch
release with a changelog entry that describes the trigger honestly, without
overstating the impact.

## Scope of fixes

Anything that crashes the parser, hangs the process on small input, writes
outside the file named by `--output`, or produces an arithmetic result that
disagrees with the documented formula is in scope. Social engineering,
physical access, and issues in third-party tooling are out of scope.
