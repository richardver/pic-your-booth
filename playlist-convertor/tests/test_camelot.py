"""Tests for Camelot wheel mapping and harmonic distance."""

import pytest
from playlist_convertor.camelot import (
    compatible_keys,
    harmonic_distance,
    key_to_camelot,
)


class TestKeyToCamelot:
    def test_major_keys(self):
        assert key_to_camelot("C major") == "8B"
        assert key_to_camelot("G major") == "9B"
        assert key_to_camelot("B major") == "1B"

    def test_minor_keys(self):
        assert key_to_camelot("A minor") == "8A"
        assert key_to_camelot("E minor") == "9A"
        assert key_to_camelot("Ab minor") == "1A"

    def test_enharmonic_equivalents(self):
        assert key_to_camelot("G# minor") == "1A"
        assert key_to_camelot("F# major") == "2B"
        assert key_to_camelot("Gb major") == "2B"

    def test_unknown_key(self):
        assert key_to_camelot("X major") is None
        assert key_to_camelot("") is None


class TestCompatibleKeys:
    def test_returns_four_keys(self):
        result = compatible_keys("8A")
        assert len(result) == 4

    def test_includes_same_key(self):
        assert "8A" in compatible_keys("8A")

    def test_includes_neighbors(self):
        result = compatible_keys("8A")
        assert "7A" in result
        assert "9A" in result

    def test_includes_relative(self):
        assert "8B" in compatible_keys("8A")
        assert "8A" in compatible_keys("8B")

    def test_wraps_around(self):
        result = compatible_keys("1A")
        assert "12A" in result
        assert "2A" in result

        result = compatible_keys("12A")
        assert "11A" in result
        assert "1A" in result


class TestHarmonicDistance:
    # Tier 1: perfect
    def test_same_key(self):
        assert harmonic_distance("8A", "8A") == 1

    def test_plus_one(self):
        assert harmonic_distance("8A", "9A") == 1

    def test_minus_one(self):
        assert harmonic_distance("8A", "7A") == 1

    def test_relative_major_minor(self):
        assert harmonic_distance("8A", "8B") == 1
        assert harmonic_distance("8B", "8A") == 1

    # Tier 2: acceptable
    def test_plus_two(self):
        assert harmonic_distance("8A", "10A") == 2

    def test_minus_two(self):
        assert harmonic_distance("8A", "6A") == 2

    def test_diagonal(self):
        assert harmonic_distance("8A", "9B") == 2
        assert harmonic_distance("8A", "7B") == 2

    # Tier 3: dramatic
    def test_two_with_mode_switch(self):
        assert harmonic_distance("8A", "10B") == 3
        assert harmonic_distance("8A", "6B") == 3

    def test_tritone(self):
        # Circular distance between 1 and 8 is min(7,5)=5, which is tier 4
        assert harmonic_distance("1A", "8A") == 4
        # True distance-7 pair: 1A and 6A → min(5,7)=5, also tier 4
        # Actual tier 3 via ±2 + mode switch:
        assert harmonic_distance("8A", "10B") == 3

    # Tier 4: incompatible
    def test_far_apart(self):
        assert harmonic_distance("8A", "3A") == 4
        assert harmonic_distance("1A", "5A") == 4

    # Edge cases
    def test_wraps_around_tier1(self):
        assert harmonic_distance("12A", "1A") == 1

    def test_wraps_around_tier2(self):
        assert harmonic_distance("12A", "2A") == 2

    def test_invalid_keys(self):
        assert harmonic_distance("", "8A") == 4
        assert harmonic_distance("8A", "") == 4
        assert harmonic_distance("X", "Y") == 4
        assert harmonic_distance("13A", "8A") == 4
        assert harmonic_distance("0A", "8A") == 4

    def test_symmetry(self):
        """Distance should be the same regardless of order."""
        assert harmonic_distance("8A", "10A") == harmonic_distance("10A", "8A")
        assert harmonic_distance("3B", "5A") == harmonic_distance("5A", "3B")
