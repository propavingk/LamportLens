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

