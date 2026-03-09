"""Tests for the library module — focused on new energy/duration_ms fields."""

import json
from pathlib import Path
from unittest.mock import patch

import pytest
from playlist_convertor.library import add_song, _load, LIBRARY_FILE


@pytest.fixture
def temp_library(tmp_path, monkeypatch):
    """Redirect the library file to a temp directory."""
    lib_file = tmp_path / ".library.json"
    monkeypatch.setattr("playlist_convertor.library.LIBRARY_FILE", lib_file)
    return lib_file


class TestAddSongEnergyDuration:
    def test_stores_energy(self, temp_library):
        add_song(
            spotify_uri="spotify:track:abc",
            file_path=Path("/tmp/test.mp3"),
            title="Test",
            artist="Artist",
            energy=7,
        )
        library = json.loads(temp_library.read_text())
        assert library["songs"]["spotify:track:abc"]["energy"] == 7

    def test_stores_duration_ms(self, temp_library):
        add_song(
            spotify_uri="spotify:track:abc",
            file_path=Path("/tmp/test.mp3"),
            title="Test",
            artist="Artist",
            duration_ms=210000,
        )
        library = json.loads(temp_library.read_text())
        assert library["songs"]["spotify:track:abc"]["duration_ms"] == 210000

    def test_stores_both(self, temp_library):
        add_song(
            spotify_uri="spotify:track:abc",
            file_path=Path("/tmp/test.mp3"),
            title="Test",
            artist="Artist",
            energy=5,
            duration_ms=180000,
        )
        library = json.loads(temp_library.read_text())
        song = library["songs"]["spotify:track:abc"]
        assert song["energy"] == 5
        assert song["duration_ms"] == 180000

    def test_omits_when_none(self, temp_library):
        add_song(
            spotify_uri="spotify:track:abc",
            file_path=Path("/tmp/test.mp3"),
            title="Test",
            artist="Artist",
        )
        library = json.loads(temp_library.read_text())
        song = library["songs"]["spotify:track:abc"]
        assert "energy" not in song
        assert "duration_ms" not in song

    def test_preserves_existing_fields(self, temp_library):
        # First add with BPM
        add_song(
            spotify_uri="spotify:track:abc",
            file_path=Path("/tmp/test.mp3"),
            title="Test",
            artist="Artist",
            bpm=124.5,
        )
        # Update with energy
        add_song(
            spotify_uri="spotify:track:abc",
            file_path=Path("/tmp/test.mp3"),
            title="Test",
            artist="Artist",
            bpm=124.5,
            energy=6,
        )
        library = json.loads(temp_library.read_text())
        song = library["songs"]["spotify:track:abc"]
        assert song["bpm"] == 124.5
        assert song["energy"] == 6
