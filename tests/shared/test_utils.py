"""Tests for shared.utils — dependency-free helpers."""

import pytest

from mechlab.shared.utils import clamp, is_close


def test_clamp_within_range():
    assert clamp(5, 0, 10) == 5


def test_clamp_below_range():
    assert clamp(-5, 0, 10) == 0


def test_clamp_above_range():
    assert clamp(15, 0, 10) == 10


def test_clamp_invalid_bounds_raises():
    with pytest.raises(ValueError):
        clamp(5, 10, 0)


def test_is_close_true_within_tolerance():
    assert is_close(1.0000000001, 1.0) is True


def test_is_close_false_outside_tolerance():
    assert is_close(1.1, 1.0) is False
