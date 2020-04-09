// Independent TypeScript implementation of the lamportlens rent arithmetic.
//
// This module exists to cross-check the Python core on the same fixtures. It
// shares the format contract in docs/FORMAT.md, not code. Standard library
// only (JSON, process, fs), no runtime dependencies.

export const ACCOUNT_STORAGE_OVERHEAD = 128;

export const RATE_PRESETS: Record<string, number> = {
  salvage: 696,
  "simd-0437-5": 696,
  "simd-0437-4": 1322,
  "simd-0437-3": 2575,
  "simd-0437-2": 5080,
  "simd-0437-1": 6333,
  "simd-0194": 6960,
  historical: 6960,
};

export const DEFAULT_LAMPORTS_PER_BYTE = 6333;

export const STATUS_UNDERFUNDED = "underfunded";
export const STATUS_AT_MINIMUM = "at-minimum";
export const STATUS_BARELY_ABOVE = "barely-above";
export const STATUS_FUNDED = "funded";
export const STATUS_EXCLUDED = "executable-excluded";

export const BARELY_ABOVE_RATIO = 1.01;

export const MAX_ACCOUNT_DATA_LEN = 10_485_760;
