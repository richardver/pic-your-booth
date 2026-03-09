"""Tests for vocal activity detection — pure numpy/math, no Demucs needed."""

import numpy as np
import pytest

from playlist_convertor.vocal_activity import (
    _mask_to_segments,
    _merge_short_gaps,
    _region_vocal_pct,
    _total_vocal_time,
)


class TestMaskToSegments:
    def test_empty_mask(self):
        mask = np.array([], dtype=bool)
        times = np.array([], dtype=float)
        assert _mask_to_segments(mask, times) == []

    def test_all_silent(self):
        mask = np.array([False, False, False, False])
        times = np.array([0.0, 0.5, 1.0, 1.5])
        assert _mask_to_segments(mask, times) == []

    def test_all_vocal(self):
        mask = np.array([True, True, True, True])
        times = np.array([0.0, 0.5, 1.0, 1.5])
        segments = _mask_to_segments(mask, times)
        assert len(segments) == 1
        assert segments[0][0] == 0.0
        assert segments[0][1] == 1.5

    def test_single_segment_in_middle(self):
        mask = np.array([False, True, True, False])
        times = np.array([0.0, 0.5, 1.0, 1.5])
        segments = _mask_to_segments(mask, times)
        assert len(segments) == 1
        assert segments[0] == [0.5, 1.5]

    def test_two_segments(self):
        mask = np.array([True, False, False, True, True])
        times = np.array([0.0, 0.5, 1.0, 1.5, 2.0])
        segments = _mask_to_segments(mask, times)
        assert len(segments) == 2
        assert segments[0] == [0.0, 0.5]
        assert segments[1] == [1.5, 2.0]

    def test_segment_at_end(self):
        mask = np.array([False, False, True, True])
        times = np.array([0.0, 0.5, 1.0, 1.5])
        segments = _mask_to_segments(mask, times)
        assert len(segments) == 1
        assert segments[0] == [1.0, 1.5]


class TestMergeShortGaps:
    def test_no_segments(self):
        assert _merge_short_gaps([], 2.0) == []

    def test_single_segment(self):
        assert _merge_short_gaps([[1.0, 3.0]], 2.0) == [[1.0, 3.0]]

    def test_gap_shorter_than_threshold(self):
        segments = [[0.0, 1.0], [2.0, 3.0]]
        merged = _merge_short_gaps(segments, 2.0)
        assert len(merged) == 1
        assert merged[0] == [0.0, 3.0]

    def test_gap_longer_than_threshold(self):
        segments = [[0.0, 1.0], [5.0, 6.0]]
        merged = _merge_short_gaps(segments, 2.0)
        assert len(merged) == 2

    def test_multiple_merges(self):
        segments = [[0.0, 1.0], [1.5, 2.0], [2.5, 3.0], [10.0, 11.0]]
        merged = _merge_short_gaps(segments, 2.0)
        assert len(merged) == 2
        assert merged[0] == [0.0, 3.0]
        assert merged[1] == [10.0, 11.0]

    def test_exact_threshold(self):
        """Gap exactly equal to threshold should NOT be merged."""
        segments = [[0.0, 1.0], [3.0, 4.0]]
        merged = _merge_short_gaps(segments, 2.0)
        assert len(merged) == 2


class TestRegionVocalPct:
    def test_no_segments(self):
        assert _region_vocal_pct([], 0.0, 30.0, 180.0) == 0.0

    def test_full_coverage(self):
        segments = [[0.0, 30.0]]
        assert _region_vocal_pct(segments, 0.0, 30.0, 180.0) == 1.0

    def test_half_coverage(self):
        segments = [[0.0, 15.0]]
        result = _region_vocal_pct(segments, 0.0, 30.0, 180.0)
        assert result == pytest.approx(0.5)

    def test_segment_partially_in_region(self):
        segments = [[20.0, 40.0]]
        # Region is 0-30, segment overlaps 20-30 = 10s out of 30s
        result = _region_vocal_pct(segments, 0.0, 30.0, 180.0)
        assert result == pytest.approx(10.0 / 30.0)

    def test_tail_region(self):
        segments = [[160.0, 180.0]]
        # Region is 150-180, segment overlaps 160-180 = 20s out of 30s
        result = _region_vocal_pct(segments, 150.0, 180.0, 180.0)
        assert result == pytest.approx(20.0 / 30.0)

    def test_segment_outside_region(self):
        segments = [[50.0, 60.0]]
        result = _region_vocal_pct(segments, 0.0, 30.0, 180.0)
        assert result == 0.0

    def test_zero_region(self):
        segments = [[0.0, 10.0]]
        result = _region_vocal_pct(segments, 5.0, 5.0, 180.0)
        assert result == 0.0


class TestTotalVocalTime:
    def test_empty(self):
        assert _total_vocal_time([]) == 0.0

    def test_single_segment(self):
        assert _total_vocal_time([[1.0, 5.0]]) == 4.0

    def test_multiple_segments(self):
        assert _total_vocal_time([[0.0, 2.0], [5.0, 8.0]]) == 5.0
