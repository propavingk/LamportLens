"""Tests for the rent arithmetic."""
from __future__ import annotations

import unittest

from lamportlens.model import AccountRecord
from lamportlens.rent import (
    DEFAULT_LAMPORTS_PER_BYTE,
    RATE_PRESETS,
    STATUS_AT_MINIMUM,
    STATUS_BARELY_ABOVE,
    STATUS_EXCLUDED,
    STATUS_FUNDED,
    STATUS_UNDERFUNDED,
    assess,
    minimum_balance,
)


def record(lamports: int, data_len: int, executable: bool = False) -> AccountRecord:
    return AccountRecord(
        address="A" * 44,
        lamports=lamports,
        data_len=data_len,
        owner="O" * 44,
        executable=executable,
        line=1,
    )


class MinimumBalanceTests(unittest.TestCase):
    def test_default_rate_is_the_mainnet_step(self):
        self.assertEqual(DEFAULT_LAMPORTS_PER_BYTE, 6333)

    def test_zero_byte_accounts(self):
        self.assertEqual(minimum_balance(0), 810_624)
        self.assertEqual(minimum_balance(0, 6960), 890_880)

    def test_token_account_size(self):
        # (128 + 165) * 6333 = 1,855,569 at the current step, and the familiar
        # 2,039,280 at the historical rate.
        self.assertEqual(minimum_balance(165), 1_855_569)
        self.assertEqual(minimum_balance(165, 6960), 2_039_280)

    def test_presets_are_ordered(self):
        self.assertEqual(RATE_PRESETS["historical"], 6960)
        self.assertEqual(RATE_PRESETS["simd-0437-1"], 6333)
        self.assertEqual(RATE_PRESETS["salvage"], 696)

    def test_invalid_inputs_raise(self):
        with self.assertRaises(ValueError):
            minimum_balance(-1)
        with self.assertRaises(ValueError):
            minimum_balance(0, 0)


class AssessTests(unittest.TestCase):
    def test_underfunded(self):
        result = assess(record(800_000, 0))
        self.assertEqual(result.status, STATUS_UNDERFUNDED)
        self.assertEqual(result.surplus, -10_624)
