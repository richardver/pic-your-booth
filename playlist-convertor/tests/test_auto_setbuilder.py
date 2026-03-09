"""Tests for the auto set builder sequencing engine."""

import json
from pathlib import Path
from unittest.mock import patch

import pytest
from playlist_convertor.auto_setbuilder import (
    HARMONIC_SCORES,
    SetResult,
    _bpm_to_rough_energy,
    _estimate_duration,
    _get_energy,
    _score_candidate,
    _score_transition,
    build_auto_set,
)


def _make_song(title, artist, bpm, camelot_key, energy=None, duration_ms=None, **kwargs):
    """Helper to create a mock library song dict."""
    song = {
        "title": title,
        "artist": artist,
        "bpm": bpm,
        "key": "",
        "camelot_key": camelot_key,
        "file_path": f"/tmp/fake/{artist} - {title}.mp3",
        "playlists": kwargs.get("playlists", ["Test"]),
        "spotify_uri": kwargs.get("spotify_uri", f"spotify:track:{title.lower().replace(' ', '')}"),
    }
    if energy is not None:
        song["energy"] = energy
    if duration_ms is not None:
        song["duration_ms"] = duration_ms
    return song


class TestBpmToRoughEnergy:
    def test_low_bpm(self):
        e = _bpm_to_rough_energy(70)
        assert 1 <= e <= 3

    def test_mid_bpm(self):
        e = _bpm_to_rough_energy(128)
        assert 5 <= e <= 8

    def test_high_bpm(self):
        e = _bpm_to_rough_energy(150)
        assert 7 <= e <= 10

    def test_clamped_low(self):
        assert _bpm_to_rough_energy(50) >= 1.0

    def test_clamped_high(self):
        assert _bpm_to_rough_energy(200) <= 10.0


class TestGetEnergy:
    def test_uses_energy_field(self):
        song = _make_song("A", "B", 128, "8A", energy=7)
        assert _get_energy(song) == 7.0

    def test_falls_back_to_bpm(self):
        song = _make_song("A", "B", 128, "8A")
        energy = _get_energy(song)
        assert 5 <= energy <= 8  # BPM proxy range


class TestScoreTransition:
    def test_perfect_transition(self):
        t = _score_transition(
            _make_song("A", "X", 124, "8A"),
            _make_song("B", "Y", 125, "9A"),
        )
        assert t["harmonic_tier"] == 1
        assert t["bpm_jump"] == 1.0
        assert t["rating"] == "green"

    def test_acceptable_transition(self):
        t = _score_transition(
            _make_song("A", "X", 124, "8A"),
            _make_song("B", "Y", 128, "10A"),
        )
        assert t["harmonic_tier"] == 2
        assert t["bpm_jump"] == 4.0
        assert t["rating"] == "yellow"

    def test_rough_transition(self):
        t = _score_transition(
            _make_song("A", "X", 120, "8A"),
            _make_song("B", "Y", 135, "3B"),
        )
        assert t["harmonic_tier"] == 4
        assert t["rating"] == "red"


class TestScoreCandidate:
    def test_first_slot_no_prev(self):
        candidate = _make_song("A", "X", 125, "8A", energy=5)
        score = _score_candidate(None, candidate, target_energy=5.0, target_bpm=125.0)
        assert score > 0

    def test_perfect_match_scores_high(self):
        prev = _make_song("A", "X", 124, "8A", energy=5)
        perfect = _make_song("B", "Y", 125, "9A", energy=6)
        bad = _make_song("C", "Z", 140, "3B", energy=2)

        score_perfect = _score_candidate(prev, perfect, target_energy=6.0, target_bpm=125.0)
        score_bad = _score_candidate(prev, bad, target_energy=6.0, target_bpm=125.0)
        assert score_perfect > score_bad


class TestEstimateDuration:
    def test_empty_tracks(self):
        assert _estimate_duration([], 30) == 0.0

    def test_single_track_no_overlap(self):
        tracks = [_make_song("A", "X", 120, "8A", duration_ms=210000)]
        duration = _estimate_duration(tracks, 30)
        assert duration == pytest.approx(3.5, abs=0.1)

    def test_two_tracks_with_overlap(self):
        tracks = [
            _make_song("A", "X", 120, "8A", duration_ms=210000),
            _make_song("B", "Y", 122, "9A", duration_ms=210000),
        ]
        duration = _estimate_duration(tracks, 30)
        # First track 210s, second 210-30=180s = 390s = 6.5 min
        assert duration == pytest.approx(6.5, abs=0.1)

    def test_fallback_duration(self):
        tracks = [_make_song("A", "X", 120, "8A")]
        duration = _estimate_duration(tracks, 30)
        assert duration == pytest.approx(3.5, abs=0.1)  # DEFAULT_TRACK_DURATION = 210s


class TestBuildAutoSet:
    MOCK_LIBRARY = [
        _make_song("Track 1", "Artist A", 122, "8A", energy=4),
        _make_song("Track 2", "Artist B", 124, "9A", energy=5),
        _make_song("Track 3", "Artist C", 126, "8B", energy=6),
        _make_song("Track 4", "Artist D", 125, "7A", energy=7),
        _make_song("Track 5", "Artist E", 128, "9B", energy=8),
        _make_song("Track 6", "Artist F", 123, "10A", energy=5),
        _make_song("Track 7", "Artist G", 127, "8A", energy=9),
        _make_song("Track 8", "Artist H", 121, "6A", energy=3),
    ]

    @patch("playlist_convertor.auto_setbuilder.get_all_songs")
    @patch("pathlib.Path.exists", return_value=True)
    def test_builds_set(self, mock_exists, mock_songs):
        mock_songs.return_value = self.MOCK_LIBRARY
        result = build_auto_set(set_minutes=20, preset_name="peak-time")
        assert isinstance(result, SetResult)
        assert len(result.tracks) > 0
        assert result.preset == "peak-time"
        assert result.estimated_minutes > 0

    @patch("playlist_convertor.auto_setbuilder.get_all_songs")
    @patch("pathlib.Path.exists", return_value=True)
    def test_transitions_match_tracks(self, mock_exists, mock_songs):
        mock_songs.return_value = self.MOCK_LIBRARY
        result = build_auto_set(set_minutes=20, preset_name="peak-time")
        assert len(result.transitions) == len(result.tracks) - 1

    @patch("playlist_convertor.auto_setbuilder.get_all_songs")
    @patch("pathlib.Path.exists", return_value=True)
    def test_bpm_filter(self, mock_exists, mock_songs):
        mock_songs.return_value = self.MOCK_LIBRARY
        result = build_auto_set(set_minutes=20, bpm_min=125, bpm_max=130)
        for track in result.tracks:
            assert 125 <= track["bpm"] <= 130

    @patch("playlist_convertor.auto_setbuilder.get_all_songs")
    @patch("pathlib.Path.exists", return_value=True)
    def test_start_key_constraint(self, mock_exists, mock_songs):
        mock_songs.return_value = self.MOCK_LIBRARY
        result = build_auto_set(set_minutes=20, start_key="9A")
        if result.tracks:
            assert result.tracks[0]["camelot_key"] == "9A"

    @patch("playlist_convertor.auto_setbuilder.get_all_songs")
    def test_empty_library(self, mock_songs):
        mock_songs.return_value = []
        result = build_auto_set(set_minutes=60)
        assert result.tracks == []
        assert result.candidates_available == 0

    @patch("playlist_convertor.auto_setbuilder.get_all_songs")
    def test_no_analyzed_tracks(self, mock_songs):
        mock_songs.return_value = [
            {"title": "A", "artist": "B", "file_path": "/tmp/a.mp3", "playlists": []},
        ]
        result = build_auto_set(set_minutes=60)
        assert result.tracks == []

    def test_invalid_preset_raises(self):
        with pytest.raises(ValueError, match="Unknown preset"):
            build_auto_set(set_minutes=60, preset_name="nonexistent")

    @patch("playlist_convertor.auto_setbuilder.get_all_songs")
    @patch("pathlib.Path.exists", return_value=True)
    def test_transition_ratings_valid(self, mock_exists, mock_songs):
        mock_songs.return_value = self.MOCK_LIBRARY
        result = build_auto_set(set_minutes=20)
        for t in result.transitions:
            assert t["rating"] in ("green", "yellow", "red")
            assert 1 <= t["harmonic_tier"] <= 4
            assert t["bpm_jump"] >= 0

    @patch("playlist_convertor.auto_setbuilder.get_all_songs")
    @patch("pathlib.Path.exists", return_value=True)
    def test_no_duplicate_tracks(self, mock_exists, mock_songs):
        mock_songs.return_value = self.MOCK_LIBRARY
        result = build_auto_set(set_minutes=20)
        uris = [t["spotify_uri"] for t in result.tracks]
        assert len(uris) == len(set(uris))

    @patch("playlist_convertor.auto_setbuilder.get_all_songs")
    @patch("pathlib.Path.exists", return_value=True)
    def test_playlist_filter(self, mock_exists, mock_songs):
        songs = [
            _make_song("A", "X", 124, "8A", playlists=["House"]),
            _make_song("B", "Y", 126, "9A", playlists=["Techno"]),
            _make_song("C", "Z", 125, "8B", playlists=["House"]),
        ]
        mock_songs.return_value = songs
        result = build_auto_set(set_minutes=10, playlists=["House"])
        for track in result.tracks:
            assert "House" in track["playlists"]
