"""Tests for the snapshot audit over the fixtures."""
from __future__ import annotations

import unittest
from pathlib import Path

from lamportlens.audit import audit
from lamportlens.model import parse_file
