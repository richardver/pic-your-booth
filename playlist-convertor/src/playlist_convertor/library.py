"""Global library tracking all downloaded songs across sessions."""

import json
from datetime import datetime, timezone
from pathlib import Path

from unidecode import unidecode

from .config import DEFAULT_OUTPUT_DIR

LIBRARY_FILE = DEFAULT_OUTPUT_DIR / ".library.json"


def make_synthetic_uri(artist: str, title: str) -> str:
    """Generate a synthetic URI for tracks not found on Spotify.

    Returns 'search:artist--title' with ASCII-safe, lowercase slug.
    """
    slug = unidecode(f"{artist}--{title}").lower().replace(" ", "-")
    return f"search:{slug}"


def _load() -> dict:
    """Load the library from disk."""
    if not LIBRARY_FILE.exists():
        return {"songs": {}, "playlists": {}}
    return json.loads(LIBRARY_FILE.read_text())


def _save(library: dict) -> None:
    """Save the library to disk."""
    LIBRARY_FILE.parent.mkdir(parents=True, exist_ok=True)
    LIBRARY_FILE.write_text(json.dumps(library, indent=2, ensure_ascii=False))


def is_downloaded(spotify_uri: str) -> dict | None:
    """Check if a song has already been downloaded.

    Returns the song entry if found, None otherwise.
    """
    library = _load()
    return library["songs"].get(spotify_uri)


def add_song(
    spotify_uri: str,
    file_path: Path,
    title: str,
    artist: str,
    album: str = "",
    playlist_name: str = "",
    bpm: float | None = None,
    key: str = "",
    camelot_key: str = "",
    mix_in: float | None = None,
    mix_out: float | None = None,
    energy: int | None = None,
    duration_ms: int | None = None,
    stems_path: str | None = None,
    has_stems: bool = False,
    vocal_segments: list | None = None,
    vocal_pct: float | None = None,
    vocal_head_pct: float | None = None,
    vocal_tail_pct: float | None = None,
) -> None:
    """Add a song to the library."""
    library = _load()

    existing = library["songs"].get(spotify_uri)
    playlists = existing["playlists"] if existing else []
    if playlist_name and playlist_name not in playlists:
        playlists.append(playlist_name)

    song = {
        "title": title,
        "artist": artist,
        "album": album,
        "file_path": str(file_path),
        "playlists": playlists,
        "bpm": bpm,
        "key": key,
        "camelot_key": camelot_key,
        "downloaded_at": existing["downloaded_at"] if existing else datetime.now(timezone.utc).isoformat(),
        "updated_at": datetime.now(timezone.utc).isoformat(),
    }

    if mix_in is not None:
        song["mix_in"] = mix_in
    if mix_out is not None:
        song["mix_out"] = mix_out
    if energy is not None:
        song["energy"] = energy
    if duration_ms is not None:
        song["duration_ms"] = duration_ms
    if stems_path is not None:
        song["stems_path"] = stems_path
    if has_stems:
        song["has_stems"] = True
    if vocal_segments is not None:
        song["vocal_segments"] = vocal_segments
    if vocal_pct is not None:
        song["vocal_pct"] = vocal_pct
    if vocal_head_pct is not None:
        song["vocal_head_pct"] = vocal_head_pct
    if vocal_tail_pct is not None:
        song["vocal_tail_pct"] = vocal_tail_pct

    library["songs"][spotify_uri] = song

    _save(library)


def add_playlist(playlist_name: str, spotify_url: str, track_count: int) -> None:
    """Record a playlist session."""
    library = _load()
    library["playlists"][playlist_name] = {
        "spotify_url": spotify_url,
        "track_count": track_count,
        "last_synced": datetime.now(timezone.utc).isoformat(),
    }
    _save(library)


def get_all_songs() -> list[dict]:
    """Get all songs in the library."""
    library = _load()
    songs = []
    for uri, data in library["songs"].items():
        songs.append({**data, "spotify_uri": uri})
    return songs


def get_all_playlists() -> dict:
    """Get all playlists in the library."""
    library = _load()
    return library["playlists"]


def get_stats() -> dict:
    """Get library statistics."""
    library = _load()
    songs = library["songs"]
    playlists = library["playlists"]

    # Count songs with analysis data
    analyzed = sum(1 for s in songs.values() if s.get("bpm"))
    with_stems = sum(1 for s in songs.values() if s.get("has_stems"))

    # Collect unique artists
    artists = set()
    for s in songs.values():
        artists.add(s["artist"])

    return {
        "total_songs": len(songs),
        "total_playlists": len(playlists),
        "analyzed": analyzed,
        "with_stems": with_stems,
        "unique_artists": len(artists),
    }


def search(query: str) -> list[dict]:
    """Search the library by title, artist, or album."""
    query_lower = query.lower()
    results = []
    for song in get_all_songs():
        if (
            query_lower in song["title"].lower()
            or query_lower in song["artist"].lower()
            or query_lower in song.get("album", "").lower()
        ):
            results.append(song)
    return results


def remove_missing() -> int:
    """Remove entries whose files no longer exist on disk.

    Returns the number of entries removed.
    """
    library = _load()
    to_remove = []
    for uri, data in library["songs"].items():
        if not Path(data["file_path"]).exists():
            to_remove.append(uri)

    for uri in to_remove:
        del library["songs"][uri]

    if to_remove:
        _save(library)

    return len(to_remove)
