"""Spotify track search using spotipy.

Looks up tracks by artist + title, returning pipeline-compatible dicts.
Reuses credentials from ~/.spotdl/config.json.
"""

import json
import logging
from pathlib import Path

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

logger = logging.getLogger(__name__)

_client: spotipy.Spotify | None = None


def _get_client() -> spotipy.Spotify:
    """Get or create a Spotify client using spotdl's stored credentials."""
    global _client
    if _client is not None:
        return _client

    config_path = Path.home() / ".spotdl" / "config.json"
    if config_path.exists():
        config = json.loads(config_path.read_text())
        client_id = config.get("client_id", "")
        client_secret = config.get("client_secret", "")
    else:
        client_id = ""
        client_secret = ""

    _client = spotipy.Spotify(
        auth_manager=SpotifyClientCredentials(
            client_id=client_id or None,
            client_secret=client_secret or None,
        )
    )
    return _client


def _track_to_dict(track: dict, track_number: int = 0) -> dict:
    """Convert a Spotify API track object to a pipeline-compatible dict."""
    artists = ", ".join(a["name"] for a in track["artists"])
    album = track.get("album", {})
    year = (album.get("release_date") or "")[:4]

    return {
        "title": track["name"],
        "artist": artists,
        "album": album.get("name", ""),
        "track_number": track_number,
        "year": year,
        "duration_ms": track.get("duration_ms", 0),
        "artwork_url": None,
        "spotify_uri": track["uri"],
        "spotify_url": track["external_urls"].get("spotify", ""),
    }


def search_track(artist: str, title: str) -> dict | None:
    """Search Spotify for a track.

    Returns a pipeline-compatible track dict or None if not found.
    Tries structured search first, falls back to loose search.
    """
    sp = _get_client()

    # Structured search
    query = f"track:{title} artist:{artist}"
    results = sp.search(q=query, type="track", limit=5)
    items = results["tracks"]["items"]

    if items:
        logger.debug("Found '%s - %s' via structured search", artist, title)
        return _track_to_dict(items[0])

    # Fallback: loose search
    query = f"{artist} {title}"
    results = sp.search(q=query, type="track", limit=5)
    items = results["tracks"]["items"]

    if items:
        logger.debug("Found '%s - %s' via loose search", artist, title)
        return _track_to_dict(items[0])

    logger.warning("Not found on Spotify: '%s - %s'", artist, title)
    return None


def search_artist_top_tracks(artist_name: str, limit: int = 30) -> list[dict]:
    """Search Spotify for an artist and return their top/popular tracks.

    Fetches the artist's top tracks plus additional tracks from their albums
    to reach the requested limit. Returns pipeline-compatible track dicts.
    """
    sp = _get_client()

    # Find the artist
    results = sp.search(q=f"artist:{artist_name}", type="artist", limit=5)
    artists = results["artists"]["items"]
    if not artists:
        logger.warning("Artist not found on Spotify: '%s'", artist_name)
        return []

    artist = artists[0]
    artist_id = artist["id"]
    artist_display = artist["name"]
    logger.info("Found artist: %s (ID: %s)", artist_display, artist_id)

    seen_uris = set()
    tracks = []

    # Get top tracks (max 10 from Spotify API)
    top = sp.artist_top_tracks(artist_id, country="US")
    for item in top["tracks"]:
        if item["uri"] not in seen_uris:
            seen_uris.add(item["uri"])
            tracks.append(_track_to_dict(item, len(tracks) + 1))

    # If we need more, get tracks from albums
    if len(tracks) < limit:
        albums = sp.artist_albums(artist_id, album_type="album,single", limit=50)
        for album in albums["items"]:
            if len(tracks) >= limit:
                break
            album_tracks = sp.album_tracks(album["id"], limit=50)
            for item in album_tracks["items"]:
                if len(tracks) >= limit:
                    break
                if item["uri"] in seen_uris:
                    continue
                # album_tracks don't include album info, add it
                item["album"] = album
                item["external_urls"] = item.get("external_urls", {})
                seen_uris.add(item["uri"])
                tracks.append(_track_to_dict(item, len(tracks) + 1))

    logger.info("Found %d tracks for artist '%s'", len(tracks), artist_display)
    return tracks


def search_tracks(track_list: list[dict]) -> tuple[list[dict], list[dict]]:
    """Search Spotify for multiple tracks.

    Each item in track_list should have 'artist' and 'title' keys.
    Returns (found, not_found) where found items have full pipeline dicts
    and not_found items are the original input dicts.
    """
    found = []
    not_found = []

    for i, item in enumerate(track_list, 1):
        artist = item["artist"]
        title = item["title"]
        result = search_track(artist, title)
        if result:
            result["track_number"] = i
            found.append(result)
        else:
            not_found.append(item)

    logger.info(
        "Spotify search: %d/%d found, %d not found",
        len(found), len(track_list), len(not_found),
    )
    return found, not_found
