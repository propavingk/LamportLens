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
