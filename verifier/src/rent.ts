// Independent TypeScript implementation of the lamportlens rent arithmetic.
//
// This module exists to cross-check the Python core on the same fixtures. It
// shares the format contract in docs/FORMAT.md, not code. Standard library
// only (JSON, process, fs), no runtime dependencies.

export const ACCOUNT_STORAGE_OVERHEAD = 128;

export const RATE_PRESETS: Record<string, number> = {
  salvage: 696,
  "simd-0437-5": 696,
