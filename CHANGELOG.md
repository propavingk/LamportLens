# Changelog

All notable changes to LamportLens are documented in this file.
The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### Changed

- Rule wording is being reviewed for the next patch.

## [1.0.0] - 2026-05-19

### Added

- Stable contract: exit codes 0, 1 and 2, and the written format contract in
  `docs/FORMAT.md`.
- Default rate updated to the SIMD-0437-1 step, 6,333 lamports per byte.

## [0.9.0] - 2025-06-17

### Added

- TypeScript verifier (`verifier/`) as an independent second implementation.
- `scripts/parity.py` comparing Python and TypeScript on every fixture.

## [0.8.0] - 2024-05-21

### Added

- Executable program accounts are classified as `executable-excluded` and left
