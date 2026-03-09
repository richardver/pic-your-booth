"""Tests for stem separation — Demucs and torch are mocked."""

import importlib
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest


class TestSeparateTrack:
    def test_separate_track_returns_expected_keys(self, tmp_path):
        """separate_track should return dict with all expected stem keys."""
        fake_tensor = MagicMock()

        mock_demucs = MagicMock()
        mock_demucs_api = MagicMock()
        mock_torch = MagicMock()
        mock_torch.stack.return_value.sum.return_value = fake_tensor
        mock_torchaudio = MagicMock()

        mock_separator = MagicMock()
        mock_separator.samplerate = 44100
        mock_separator.separate_audio_file.return_value = (
            None,
            {
                "vocals": fake_tensor,
                "drums": fake_tensor,
                "bass": fake_tensor,
                "other": fake_tensor,
            },
        )
        mock_demucs_api.Separator.return_value = mock_separator
        mock_demucs.api = mock_demucs_api

        modules_patch = {
            "demucs": mock_demucs,
            "demucs.api": mock_demucs_api,
            "torch": mock_torch,
            "torchaudio": mock_torchaudio,
        }

        saved = sys.modules.pop("playlist_convertor.stems", None)
        try:
            with patch.dict(sys.modules, modules_patch):
                mod = importlib.import_module("playlist_convertor.stems")

                # Patch the _save_stem_as_mp3 and shutil on the fresh module
                mod._save_stem_as_mp3 = MagicMock()
                mod.shutil = MagicMock()

                input_file = tmp_path / "test.mp3"
                input_file.touch()
                output_dir = tmp_path / "stems_out"

                result = mod.separate_track(input_file, output_dir)
        finally:
            if saved is not None:
                sys.modules["playlist_convertor.stems"] = saved
            else:
                sys.modules.pop("playlist_convertor.stems", None)

        assert "stems_path" in result
        assert "vocals" in result
        assert "drums" in result
        assert "bass" in result
        assert "other" in result
        assert "instrumental" in result
        assert "acapella" in result
        assert result["stems_path"] == str(output_dir)

    def test_check_demucs_raises_without_package(self):
        """_check_demucs should raise ImportError when demucs is not installed."""
        from playlist_convertor.stems import _check_demucs

        with patch.dict(sys.modules, {"demucs": None, "demucs.api": None}):
            with pytest.raises(ImportError, match="stems extra"):
                _check_demucs()


class TestBitrateToCompression:
    def test_192k(self):
        from playlist_convertor.stems import _bitrate_to_compression

        assert _bitrate_to_compression("192k") == 192.0

    def test_320k(self):
        from playlist_convertor.stems import _bitrate_to_compression

        assert _bitrate_to_compression("320k") == 320.0

    def test_128k(self):
        from playlist_convertor.stems import _bitrate_to_compression

        assert _bitrate_to_compression("128k") == 128.0
