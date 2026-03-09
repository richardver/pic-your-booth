"""FAT32-safe file organization."""

import re
from datetime import date
from pathlib import Path

from unidecode import unidecode

from .config import FAT32_ILLEGAL_CHARS, MAX_PATH_LENGTH


def sanitize_filename(name: str, fat32_safe: bool = True) -> str:
    """Make a filename safe for FAT32 filesystems."""
    if fat32_safe:
        name = unidecode(name)

    for char in FAT32_ILLEGAL_CHARS:
        name = name.replace(char, "")

    name = re.sub(r"\s+", " ", name).strip()
    name = name.strip(".")

    if len(name) > MAX_PATH_LENGTH - 10:
        name = name[: MAX_PATH_LENGTH - 10]

    return name


def build_track_filename(index: int, artist: str, title: str, ext: str = "mp3", fat32_safe: bool = True) -> str:
    """Build a DJ-friendly filename: [##] - Artist - Title.ext"""
    artist = sanitize_filename(artist, fat32_safe)
    title = sanitize_filename(title, fat32_safe)
    return f"{index:02d} - {artist} - {title}.{ext}"


def build_folder_name(playlist_name: str, target: str = "", bpm_range: tuple[int, int] | None = None, fat32_safe: bool = True) -> str:
    """Build folder name: YYYY-MM-DD_PlaylistName_rekordbox_120-128bpm"""
    safe_name = sanitize_filename(playlist_name, fat32_safe)
    today = date.today().isoformat()
    parts = [today, safe_name]

    if target:
        parts.append(target)

    if bpm_range:
        bpm_min, bpm_max = bpm_range
        if bpm_min == bpm_max:
            parts.append(f"{bpm_min}bpm")
        else:
            parts.append(f"{bpm_min}-{bpm_max}bpm")

    return "_".join(parts)


def create_output_dir(base_dir: Path, playlist_name: str, target: str = "", fat32_safe: bool = True) -> Path:
    """Create the output directory for a playlist (no subfolders)."""
    folder_name = build_folder_name(playlist_name, target=target, fat32_safe=fat32_safe)
    output_dir = base_dir / folder_name
    output_dir.mkdir(parents=True, exist_ok=True)
    return output_dir


def rename_with_bpm(playlist_dir: Path, bpm_range: tuple[int, int], playlist_name: str, target: str = "", fat32_safe: bool = True) -> Path:
    """Rename the playlist folder to include BPM range after analysis."""
    new_name = build_folder_name(playlist_name, target=target, bpm_range=bpm_range, fat32_safe=fat32_safe)
    new_path = playlist_dir.parent / new_name

    if new_path == playlist_dir:
        return playlist_dir

    if new_path.exists():
        return playlist_dir

    playlist_dir.rename(new_path)
    return new_path
