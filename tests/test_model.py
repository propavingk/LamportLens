"""Tests for account record parsing and validation."""
from __future__ import annotations

import json
import unittest
from pathlib import Path

from lamportlens.model import FormatError, parse_record, parse_text

