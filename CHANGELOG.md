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
  out of bands, totals and owner locked sums.

## [0.7.0] - 2023-04-11

### Added

- The `barely-above` ratio (1.01) and the `reclaimable on close` total.
- Underfunded list sorted by deficit descending.

## [0.6.0] - 2022-02-01

### Added

- JSON report with fixed keys, including per-owner summaries.
- `bands` and `owners` subcommands.

## [0.5.0] - 2020-12-08

### Added

- Per-owner summary ranked by locked lamports.
- Seven fixed data-length bands with account counts and locked totals.

## [0.4.0] - 2019-01-15
