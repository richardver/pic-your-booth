"""Download tracks using spotdl (wraps yt-dlp + ffmpeg)."""

import logging
import subprocess
import shutil
import sys
from pathlib import Path

logger = logging.getLogger(__name__)


def _find_tool(name: str) -> str | None:
    """Find a tool on PATH or in the current venv's bin directory."""
    # Check PATH first
    path = shutil.which(name)
    if path:
        return path

    # Check the venv's bin directory (same prefix as the running Python)
    venv_bin = Path(sys.executable).parent / name
    if venv_bin.exists():
        return str(venv_bin)

    return None


def check_dependencies() -> None:
    """Check that required external tools are available."""
    for tool in ("spotdl", "ffmpeg"):
        if _find_tool(tool) is None:
            raise RuntimeError(
                f"'{tool}' not found. Install it first:\n"
                f"  spotdl: pip install spotdl\n"
                f"  ffmpeg: brew install ffmpeg (macOS) or https://ffmpeg.org"
            )


def download_track(
    spotify_url: str,
    output_dir: Path,
    audio_format: str = "mp3",
    bitrate: str = "192k",
) -> Path | None:
    """Download a single track using spotdl.

    spotify_url can be a Spotify track URL (https://open.spotify.com/track/...)
    or an 'Artist - Title' search query — spotdl accepts both formats.

    Returns the path to the downloaded file, or None on failure.
    spotdl uses config from ~/.spotdl/config.json (user_auth + credentials).
    """
    output_dir.mkdir(parents=True, exist_ok=True)

    spotdl_path = _find_tool("spotdl")
    if not spotdl_path:
        return None

    # Resolve to absolute path to avoid nesting issues
    abs_output = output_dir.resolve()

    cmd = [
        spotdl_path,
        "download",
        spotify_url,
        "--output", str(abs_output),
        "--format", audio_format,
        "--bitrate", bitrate,
    ]

    # Snapshot existing files so we can detect what's new
    existing = set(abs_output.glob(f"*.{audio_format}"))

    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
    )

    if result.stdout:
        logger.debug("spotdl stdout: %s", result.stdout.strip())
    if result.stderr:
        logger.debug("spotdl stderr: %s", result.stderr.strip())
    if result.returncode != 0:
        logger.warning("spotdl exited with code %d for %s", result.returncode, spotify_url)

    # Find newly created file (ignore exit code — spotdl returns non-zero
    # for metadata errors even when the audio file downloaded successfully)
    new_files = sorted(
        (f for f in abs_output.glob(f"*.{audio_format}") if f not in existing),
        key=lambda f: f.stat().st_mtime,
    )
    if new_files:
        return new_files[-1]

    # Fallback: check most recent file
    all_files = sorted(abs_output.glob(f"*.{audio_format}"), key=lambda f: f.stat().st_mtime)
    if all_files and result.returncode == 0:
        return all_files[-1]

    return None
