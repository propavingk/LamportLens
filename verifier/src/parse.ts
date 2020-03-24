// JSONL parsing for the verifier, mirroring the validation rules that the
// Python model applies. Errors are collected, not thrown, so a partially
// readable snapshot still produces a full result.

import { AccountRecord, MAX_ACCOUNT_DATA_LEN } from "./rent.js";

export interface ParseError {
  line: number;
  message: string;
}

function requireNonEmptyString(obj: Record<string, unknown>, key: string, line: number): string {
  if (!(key in obj)) throw new FormatError(`line ${line}: missing required field '${key}'`);
  const value = obj[key];
  if (typeof value !== "string" || value.length === 0) {
    throw new FormatError(`line ${line}: field '${key}' must be a non-empty string`);
  }
  return value;
}

function requireInteger(
  obj: Record<string, unknown>,
  key: string,
  line: number,
  minimum: number,
