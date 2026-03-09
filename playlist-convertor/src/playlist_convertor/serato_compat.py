"""Serato compatibility validation checks."""

from pathlib import Path

from mutagen.id3 import ID3
from mutagen.mp3 import MP3


def check_track(file_path: Path) -> list[str]:
    """Check a track for Serato compatibility issues.

    Returns a list of warning messages (empty = all good).
    """
    warnings = []

    if not file_path.exists():
        return [f"File not found: {file_path}"]

    try:
        audio = MP3(str(file_path))
    except Exception as e:
        return [f"Cannot read MP3: {e}"]

    tags = audio.tags

    if tags is None:
        warnings.append("No ID3 tags found")
        return warnings

    # Check ID3 version - Serato prefers v2.3
    if tags.version != (2, 3, 0):
        warnings.append(f"ID3 version is {tags.version}, Serato prefers v2.3")

    # Check for essential tags
    if not tags.getall("TIT2"):
        warnings.append("Missing title (TIT2)")
    if not tags.getall("TPE1"):
        warnings.append("Missing artist (TPE1)")

    # Check genre separator - Serato uses / not ;
    genre_frames = tags.getall("TCON")
    for frame in genre_frames:
        for text in frame.text:
            if ";" in text:
                warnings.append(f"Genre uses ';' separator (Serato prefers '/'): {text}")

    # Check for Serato GEOB tags (we shouldn't write these)
    for key in tags:
        if key.startswith("GEOB:Serato"):
            warnings.append(f"Contains Serato GEOB tag '{key}' - let Serato write these itself")

    # Check bitrate - Serato handles CBR better than VBR
    if audio.info.bitrate_mode is not None:
        try:
            from mutagen.mp3 import BitrateMode
            if audio.info.bitrate_mode == BitrateMode.VBR:
                warnings.append("VBR encoding detected - Serato handles CBR more reliably")
        except ImportError:
            pass

    return warnings


def check_playlist(file_paths: list[Path], verbose: bool = False) -> dict:
    """Check all tracks in a playlist for Serato compatibility.

    Returns dict with 'ok' count, 'warnings' count, and 'details' list.
    """
    ok = 0
    warn = 0
    details = []

    for path in file_paths:
        issues = check_track(path)
        if issues:
            warn += 1
            details.append({"file": path.name, "issues": issues})
        else:
            ok += 1

    return {"ok": ok, "warnings": warn, "details": details}
