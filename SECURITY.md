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

