"""Tests for energy arc presets."""

import pytest
from playlist_convertor.arc_presets import (
    PRESETS,
    _find_peak_position,
    get_target_bpm,
    get_target_energy,
    list_presets,
)


class TestGetTargetEnergy:
    def test_start_of_preset(self):
        energy = get_target_energy("peak-time", 0.0)
        assert energy == 3  # first control point

    def test_end_of_preset(self):
        energy = get_target_energy("peak-time", 1.0)
        assert energy == 5  # last control point

    def test_interpolates_midpoint(self):
        energy = get_target_energy("peak-time", 0.10)
        # Between (0.0, 3) and (0.20, 5) -> midpoint should be 4
        assert energy == pytest.approx(4.0)

    def test_clamps_below_zero(self):
        energy = get_target_energy("peak-time", -0.5)
        assert energy == 3  # clamped to position 0.0

    def test_clamps_above_one(self):
        energy = get_target_energy("peak-time", 1.5)
        assert energy == 5  # clamped to position 1.0

    def test_all_presets_valid(self):
        for preset_name in PRESETS:
            for pos in [0.0, 0.25, 0.5, 0.75, 1.0]:
                energy = get_target_energy(preset_name, pos)
                assert 1 <= energy <= 10, f"{preset_name} at {pos}: energy={energy}"

    def test_unknown_preset_raises(self):
        with pytest.raises(ValueError, match="Unknown preset"):
            get_target_energy("nonexistent", 0.5)


class TestGetTargetBpm:
    def test_start_at_bpm_min(self):
        bpm = get_target_bpm("peak-time", 0.0, 120, 130)
        assert bpm == pytest.approx(120.0)

    def test_peak_higher_than_start(self):
        peak_pos = _find_peak_position("peak-time")
        bpm_at_peak = get_target_bpm("peak-time", peak_pos, 120, 130)
        bpm_at_start = get_target_bpm("peak-time", 0.0, 120, 130)
        assert bpm_at_peak > bpm_at_start

    def test_eases_after_peak(self):
        peak_pos = _find_peak_position("peak-time")
        bpm_at_peak = get_target_bpm("peak-time", peak_pos, 120, 130)
        bpm_at_end = get_target_bpm("peak-time", 1.0, 120, 130)
        assert bpm_at_end < bpm_at_peak

    def test_stays_within_range(self):
        for pos in [0.0, 0.25, 0.5, 0.75, 1.0]:
            bpm = get_target_bpm("peak-time", pos, 120, 130)
            assert 119 <= bpm <= 131  # allow small float rounding

    def test_unknown_preset_raises(self):
        with pytest.raises(ValueError, match="Unknown preset"):
            get_target_bpm("nonexistent", 0.5, 120, 130)


class TestFindPeakPosition:
    def test_peak_time_peaks_at_two_thirds(self):
        peak = _find_peak_position("peak-time")
        assert peak == 0.65

    def test_warm_up_peaks_late(self):
        peak = _find_peak_position("warm-up")
        assert peak >= 0.5

    def test_closer_peaks_early(self):
        peak = _find_peak_position("closer")
        assert peak <= 0.25


class TestListPresets:
    def test_returns_all_presets(self):
        presets = list_presets()
        assert len(presets) == 5

    def test_preset_has_required_fields(self):
        for p in list_presets():
            assert "key" in p
            assert "name" in p
            assert "description" in p
            assert "energy_range" in p

    def test_preset_keys_match(self):
        preset_keys = {p["key"] for p in list_presets()}
        assert preset_keys == {"warm-up", "peak-time", "marathon", "chill", "closer"}
