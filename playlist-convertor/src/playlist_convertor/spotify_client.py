"""Spotify metadata - fetches track data from Spotify's embed page.

Bypasses the restricted Spotify Web API playlist_tracks endpoint by
scraping the public embed page, which contains full track listings
in its __NEXT_DATA__ JSON blob. No API auth needed for public playlists.
"""

import json
import logging
import re

import requests

logger = logging.getLogger(__name__)


def extract_playlist_id(url: str) -> str:
    """Extract playlist ID from a Spotify URL or URI."""
    match = re.search(r"playlist[/:]([a-zA-Z0-9]+)", url)
    if match:
        return match.group(1)
    raise ValueError(f"Could not extract playlist ID from: {url}")


def fetch_tracks(spotify_url: str) -> tuple[str, list[dict]]:
    """Fetch playlist name and tracks from Spotify's embed page.

    Uses the public embed page which includes track data in __NEXT_DATA__,
    bypassing the restricted Web API endpoints entirely.

    Returns (playlist_name, tracks).
    """
    playlist_id = extract_playlist_id(spotify_url)
    embed_url = f"https://open.spotify.com/embed/playlist/{playlist_id}"
    logger.debug(f"Fetching embed page for {playlist_id}...")

    resp = requests.get(embed_url, timeout=15)
    resp.raise_for_status()

    # Extract __NEXT_DATA__ JSON from the page
    match = re.search(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', resp.text, re.DOTALL)
    if not match:
        raise RuntimeError("Could not find track data in Spotify embed page")

    data = json.loads(match.group(1))
    entity = data["props"]["pageProps"]["state"]["data"]["entity"]

    playlist_name = entity.get("name") or entity.get("title", "Unknown Playlist")
    logger.debug(f"Playlist: {playlist_name}")

    track_list = entity.get("trackList", [])
    if not track_list:
        raise RuntimeError(
            f"No tracks found for '{playlist_name}'. "
            "The playlist may be empty or private."
        )

    tracks = []
    for i, item in enumerate(track_list, 1):
        if item.get("entityType") != "track":
            continue

        # Parse artist from subtitle (artists joined with non-breaking spaces)
        artist = item.get("subtitle", "Unknown Artist")
        # Clean up non-breaking spaces used as separators
        artist = artist.replace("\u00a0", " ")

        uri = item.get("uri", "")
        # Convert spotify:track:ID to URL
        track_id = uri.split(":")[-1] if uri else ""
        spotify_url_track = f"https://open.spotify.com/track/{track_id}" if track_id else ""

        tracks.append({
            "title": item.get("title", "Unknown"),
            "artist": artist,
            "album": "",  # Not available in embed data
            "track_number": i,
            "year": "",
            "duration_ms": item.get("duration", 0),
            "artwork_url": None,  # Will use playlist artwork
            "spotify_uri": uri,
            "spotify_url": spotify_url_track,
        })

    logger.debug(f"Total: {len(tracks)} tracks")
    return playlist_name, tracks
