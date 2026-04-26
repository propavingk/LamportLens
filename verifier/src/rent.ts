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

export interface AccountRecord {
  address: string;
  lamports: number;
  dataLen: number;
  owner: string;
  executable: boolean;
  line: number;
}

export function minimumBalance(dataLen: number, lamportsPerByte = DEFAULT_LAMPORTS_PER_BYTE): number {
  if (dataLen < 0) throw new Error("dataLen must be >= 0");
  if (lamportsPerByte <= 0) throw new Error("lamportsPerByte must be > 0");
  return (ACCOUNT_STORAGE_OVERHEAD + dataLen) * lamportsPerByte;
}

export function assess(record: AccountRecord, lamportsPerByte = DEFAULT_LAMPORTS_PER_BYTE): string {
  const minimum = minimumBalance(record.dataLen, lamportsPerByte);
  if (record.executable) return STATUS_EXCLUDED;
  if (record.lamports < minimum) return STATUS_UNDERFUNDED;
  if (record.lamports === minimum) return STATUS_AT_MINIMUM;
  if (record.lamports <= Math.trunc(minimum * BARELY_ABOVE_RATIO)) return STATUS_BARELY_ABOVE;
  return STATUS_FUNDED;
}
