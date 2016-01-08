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
