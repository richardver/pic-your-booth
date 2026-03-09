"""Set builder - build DJ sets from the library."""

import json
import shutil
from collections import Counter
from datetime import datetime
from pathlib import Path

from .config import ACTIVE_SET_DIR, SETS_DIR, DEFAULT_OUTPUT_DIR
from .library import get_all_songs, search as library_search


def _active_dir() -> Path:
    return DEFAULT_OUTPUT_DIR / ACTIVE_SET_DIR


def _sets_dir() -> Path:
    return DEFAULT_OUTPUT_DIR / SETS_DIR


def _meta_path() -> Path:
    return _active_dir() / ".set.json"


def _load_meta() -> dict:
    meta_path = _meta_path()
    if meta_path.exists():
        return json.loads(meta_path.read_text())
    return {"name": "", "created": "", "songs": []}


def _save_meta(meta: dict) -> None:
    _meta_path().parent.mkdir(parents=True, exist_ok=True)
    _meta_path().write_text(json.dumps(meta, indent=2, ensure_ascii=False))


def new_set(name: str = "") -> Path:
    """Start a new set, clearing the active one.

    Returns the active set path.
    """
    active = _active_dir()

    # Clear existing
    if active.exists():
        shutil.rmtree(active)

    active.mkdir(parents=True, exist_ok=True)

    meta = {
        "name": name,
        "created": datetime.now().strftime("%Y-%m-%d_%H%M"),
        "songs": [],
    }
    _save_meta(meta)
    return active


def add_to_set(songs: list[dict]) -> list[dict]:
    """Add songs to the active set by copying files.

    Args:
        songs: List of library song dicts (must have file_path, title, artist).

    Returns:
        List of songs that were actually added (skips duplicates).
    """
    active = _active_dir()
    active.mkdir(parents=True, exist_ok=True)
    meta = _load_meta()

    existing_uris = {s["spotify_uri"] for s in meta["songs"]}
    added = []

    for song in songs:
        if song.get("spotify_uri") in existing_uris:
            continue

        src = Path(song["file_path"])

        # Number sequentially in the set
        idx = len(meta["songs"]) + 1
        dest = active / f"{idx:02d} - {song['artist']} - {song['title']}{src.suffix}"
        if src.exists():
            shutil.copy2(str(src), str(dest))

        entry = {
            "spotify_uri": song.get("spotify_uri", ""),
            "title": song["title"],
            "artist": song["artist"],
            "bpm": song.get("bpm"),
            "key": song.get("key", ""),
            "camelot_key": song.get("camelot_key", ""),
            "file": dest.name,
        }
        meta["songs"].append(entry)
        existing_uris.add(entry["spotify_uri"])
        added.append(entry)

    _save_meta(meta)
    return added


def add_by_search(query: str) -> list[dict]:
    """Search library and add matching songs to set."""
    results = library_search(query)
    return add_to_set(results)


def add_by_bpm(bpm_min: float, bpm_max: float) -> list[dict]:
    """Add songs within a BPM range to the set."""
    songs = get_all_songs()
    matches = [s for s in songs if s.get("bpm") and bpm_min <= s["bpm"] <= bpm_max]
    return add_to_set(matches)


def add_by_key(camelot_key: str) -> list[dict]:
    """Add songs with a compatible Camelot key to the set."""
    from .camelot import compatible_keys

    compat = compatible_keys(camelot_key)
    songs = get_all_songs()
    matches = [s for s in songs if s.get("camelot_key") in compat]
    return add_to_set(matches)


def add_by_playlist(playlist_name: str) -> list[dict]:
    """Add all songs from a specific playlist to the set."""
    songs = get_all_songs()
    matches = [s for s in songs if playlist_name in s.get("playlists", [])]
    return add_to_set(matches)


def get_set_songs() -> list[dict]:
    """Get all songs in the active set."""
    meta = _load_meta()
    return meta["songs"]


def generate_set_name() -> str:
    """Auto-generate a set name from song tags.

    Format: YYYY-MM-DD_HHMM_genre_bpmrange
    """
    meta = _load_meta()
    songs = meta["songs"]
    timestamp = meta.get("created") or datetime.now().strftime("%Y-%m-%d_%H%M")

    if not songs:
        return timestamp

    parts = [timestamp]

    # Add custom name if set
    if meta.get("name"):
        parts.append(meta["name"])
        return "_".join(parts)

    # Dominant genre (from library data - look up full song data)
    all_songs = {s.get("spotify_uri"): s for s in get_all_songs()}
    genres = []
    for song in songs:
        lib_song = all_songs.get(song.get("spotify_uri"), {})
        if lib_song.get("genre"):
            genres.append(lib_song["genre"].lower())
    if genres:
        dominant = Counter(genres).most_common(1)[0][0]
        dominant = dominant.split("/")[0].strip().replace(" ", "-")
        parts.append(dominant)

    # BPM range
    bpms = [s["bpm"] for s in songs if s.get("bpm")]
    if bpms:
        bpm_min = int(min(bpms))
        bpm_max = int(max(bpms))
        if bpm_min == bpm_max:
            parts.append(f"{bpm_min}bpm")
        else:
            parts.append(f"{bpm_min}-{bpm_max}bpm")

    # Camelot range
    keys = sorted(set(s.get("camelot_key", "") for s in songs if s.get("camelot_key")))
    if keys:
        if len(keys) <= 3:
            parts.append("-".join(keys))

    return "_".join(parts)


def save_set(name: str = "") -> Path:
    """Archive the active set to the sets folder.

    Returns the path to the saved set.
    """
    if not name:
        name = generate_set_name()

    set_path = _sets_dir() / name
    active = _active_dir()

    if not active.exists() or not any(active.iterdir()):
        raise ValueError("Active set is empty - nothing to save")

    # Copy active set to archive
    if set_path.exists():
        shutil.rmtree(set_path)
    shutil.copytree(str(active), str(set_path))

    return set_path


def auto_build_set(
    set_minutes: int,
    preset_name: str = "peak-time",
    bpm_min: float | None = None,
    bpm_max: float | None = None,
    start_key: str | None = None,
    playlists: list[str] | None = None,
    use_vocal_scoring: bool = False,
    target: str = "rekordbox",
) -> "auto_setbuilder.SetResult":
    """Auto-build a set, populate active-set/, generate DJ software exports.

    Args:
        target: DJ software target — 'rekordbox', 'serato', or 'both'.

    Returns the SetResult from the sequencing engine.
    """
    from . import auto_setbuilder
    from .rekordbox_export import generate_xml

    # Build the sequenced set
    result = auto_setbuilder.build_auto_set(
        set_minutes=set_minutes,
        preset_name=preset_name,
        bpm_min=bpm_min,
        bpm_max=bpm_max,
        start_key=start_key,
        playlists=playlists,
        use_vocal_scoring=use_vocal_scoring,
    )

    if not result.tracks:
        return result

    name = f"autoset_{preset_name}_{set_minutes}min"

    # Build export track list using original file paths (no copying)
    export_tracks = []
    for i, song in enumerate(result.tracks):
        export_tracks.append({
            "title": song["title"],
            "artist": song["artist"],
            "file_path": Path(song["file_path"]),
            "bpm": song.get("bpm"),
            "key": song.get("key", ""),
            "camelot_key": song.get("camelot_key", ""),
            "mix_in": song.get("mix_in"),
            "mix_out": song.get("mix_out"),
            "duration_ms": song.get("duration_ms", 0),
            "album": song.get("album", ""),
            "track_number": i + 1,
        })

    # Rekordbox XML export — saved in output/ root
    xml_path = None
    if target in ("rekordbox", "both"):
        xml_path = DEFAULT_OUTPUT_DIR / f"{name}.xml"
        generate_xml(name, export_tracks, xml_path)

    # Serato M3U8 export + compatibility check
    m3u8_path = None
    serato_report = None
    if target in ("serato", "both"):
        from .serato_export import generate_m3u8
        from .serato_compat import check_playlist

        m3u8_path = DEFAULT_OUTPUT_DIR / f"{name}.m3u8"
        generate_m3u8(name, export_tracks, m3u8_path)

        file_paths = [t["file_path"] for t in export_tracks if t["file_path"].exists()]
        if file_paths:
            serato_report = check_playlist(file_paths)

    # Store export info on result for CLI display
    result.xml_path = xml_path
    result.m3u8_path = m3u8_path
    result.serato_report = serato_report
    result.set_name = name

    return result


def list_sets() -> list[dict]:
    """List all saved sets."""
    sets_dir = _sets_dir()
    if not sets_dir.exists():
        return []

    sets = []
    for d in sorted(sets_dir.iterdir()):
        if not d.is_dir():
            continue

        meta_path = d / ".set.json"
        track_count = len(list(d.glob("*.mp3"))) + len(list(d.glob("*.flac"))) + len(list(d.glob("*.wav")))

        info = {"name": d.name, "path": str(d), "tracks": track_count}

        if meta_path.exists():
            meta = json.loads(meta_path.read_text())
            info["created"] = meta.get("created", "")

        sets.append(info)

    return sets
