"""The rent-exempt arithmetic.

Solana requires every account to hold a minimum lamport balance sized to its
data, a bond that is returned in full when the account is closed. The formula
the cluster uses is:

    minimum_balance = (ACCOUNT_STORAGE_OVERHEAD + data_len) * lamports_per_byte

The historical form of the same formula used two constants,
lamports_per_byte_year (3480) and an exemption threshold (2.0), which multiply
to 6960. The proposal that replaced the floating point form, SIMD-0194, folded
the threshold into a single lamports_per_byte value of 6960, and SIMD-0437
reduces that value in steps toward 696.

This module keeps the named steps so a snapshot can be audited against the
rate that was live when it was captured. The default is the step that the
Solana Foundation upgrade notes list as live on mainnet: 6,333 lamports per
byte, active since epoch 1028 on 2026-09-03.
"""
from __future__ import annotations

from dataclasses import dataclass

from .model import AccountRecord

ACCOUNT_STORAGE_OVERHEAD = 128

RATE_PRESETS: dict[str, int] = {
    "salvage": 696,
    "simd-0437-5": 696,
    "simd-0437-4": 1322,
    "simd-0437-3": 2575,
    "simd-0437-2": 5080,
    "simd-0437-1": 6333,
    "simd-0194": 6960,
    "historical": 6960,
}

DEFAULT_LAMPORTS_PER_BYTE = 6333

STATUS_UNDERFUNDED = "underfunded"
