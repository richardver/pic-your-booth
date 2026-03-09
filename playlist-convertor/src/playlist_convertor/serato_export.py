"""Serato playlist export — generates M3U8 playlists importable as Serato crates."""

from pathlib import Path


def generate_m3u8(
    playlist_name: str,
    tracks: list[dict],
    output_path: Path,
) -> Path:
    """Generate an M3U8 playlist file for Serato import.

    Serato can import M3U/M3U8 files via File > Import Crate.
    Each track is listed with absolute paths.

    Args:
        playlist_name: Name of the playlist (used in header comment).
        tracks: List of dicts, each with:
            - file_path: Path to the audio file
            - title, artist (for EXTINF metadata)
            - duration_ms (int, optional)
        output_path: Where to write the M3U8 file.

    Returns:
        Path to the written M3U8 file.
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)

    lines = ["#EXTM3U", f"# Playlist: {playlist_name}"]

    for track in tracks:
        file_path = track["file_path"]
        if not isinstance(file_path, Path):
            file_path = Path(file_path)

        duration_s = track.get("duration_ms", 0) // 1000 if track.get("duration_ms") else -1
        artist = track.get("artist", "")
        title = track.get("title", "")
        display = f"{artist} - {title}" if artist else title

        lines.append(f"#EXTINF:{duration_s},{display}")
        lines.append(str(file_path.resolve()))

    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return output_path
