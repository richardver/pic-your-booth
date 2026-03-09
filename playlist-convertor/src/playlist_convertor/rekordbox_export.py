"""Rekordbox XML export for importing playlists into Rekordbox."""

import xml.etree.ElementTree as ET
from pathlib import Path
from xml.dom import minidom


def _file_uri(path: Path) -> str:
    """Convert a file path to a file:// URI for Rekordbox."""
    return path.resolve().as_uri()


def generate_xml(
    playlist_name: str,
    tracks: list[dict],
    output_path: Path,
) -> Path:
    """Generate a Rekordbox-compatible XML file.

    Args:
        playlist_name: Name of the playlist.
        tracks: List of dicts, each with:
            - file_path: Path to the audio file
            - title, artist, album, genre, year
            - bpm (float, optional)
            - key (str, optional) e.g. "C minor"
            - camelot_key (str, optional) e.g. "5A"
            - duration_ms (int)
            - track_number (int)
        output_path: Where to write the XML file.

    Returns:
        Path to the written XML file.
    """
    root = ET.Element("DJ_PLAYLISTS", Version="1.0.0")

    # Product info
    ET.SubElement(root, "PRODUCT", Name="playlist-convertor", Version="0.1.0", Company="")

    # Collection
    collection = ET.SubElement(root, "COLLECTION", Entries=str(len(tracks)))

    for i, track in enumerate(tracks, 1):
        file_path = track["file_path"]
        duration_s = track.get("duration_ms", 0) // 1000

        attrs = {
            "TrackID": str(i),
            "Name": track.get("title", ""),
            "Artist": track.get("artist", ""),
            "Album": track.get("album", ""),
            "Genre": track.get("genre", ""),
            "Kind": "MP3 File",
            "Size": str(file_path.stat().st_size) if file_path.exists() else "0",
            "TotalTime": str(duration_s),
            "Location": _file_uri(file_path),
            "TrackNumber": str(track.get("track_number", i)),
        }

        if track.get("year"):
            attrs["Year"] = str(track["year"])

        if track.get("bpm"):
            attrs["AverageBpm"] = f"{track['bpm']:.2f}"

        if track.get("key"):
            attrs["Tonality"] = track["key"]

        track_el = ET.SubElement(collection, "TRACK", **attrs)

        if track.get("mix_in") is not None:
            ET.SubElement(track_el, "POSITION_MARK",
                Name="Mix In", Type="0",
                Start=f"{track['mix_in']:.3f}",
                Num="0", Red="40", Green="226", Blue="20")
        if track.get("mix_out") is not None:
            ET.SubElement(track_el, "POSITION_MARK",
                Name="Mix Out", Type="0",
                Start=f"{track['mix_out']:.3f}",
                Num="1", Red="0", Green="100", Blue="255")

    # Playlists
    playlists = ET.SubElement(root, "PLAYLISTS")
    root_node = ET.SubElement(playlists, "NODE", Type="0", Name="ROOT", Count="1")

    playlist_node = ET.SubElement(
        root_node, "NODE",
        Name=playlist_name,
        Type="1",
        KeyType="0",
        Entries=str(len(tracks)),
    )

    for i in range(1, len(tracks) + 1):
        ET.SubElement(playlist_node, "TRACK", Key=str(i))

    # Write with pretty formatting
    output_path.parent.mkdir(parents=True, exist_ok=True)
    xml_str = ET.tostring(root, encoding="unicode", xml_declaration=False)
    pretty = minidom.parseString(xml_str).toprettyxml(indent="  ", encoding="UTF-8")

    output_path.write_bytes(pretty)
    return output_path
