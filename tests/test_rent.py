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

