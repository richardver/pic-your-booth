"""ID3v2.3 tagging using mutagen."""

import logging
from pathlib import Path
from urllib.request import urlopen

logger = logging.getLogger(__name__)

from mutagen.id3 import (
    APIC,
    COMM,
    ID3,
    TALB,
    TBPM,
    TCON,
    TDRC,
    TIT2,
    TKEY,
    TPE1,
    TRCK,
    TXXX,
    TYER,
)
from mutagen.mp3 import MP3


def tag_track(
    file_path: Path,
    metadata: dict,
    analysis: dict | None = None,
    camelot_in_comments: bool = False,
) -> None:
    """Write ID3v2.3 tags to an MP3 file.

    Args:
        file_path: Path to the MP3 file.
        metadata: Dict with title, artist, album, track_number, year, artwork_url.
        analysis: Optional dict with bpm, key, camelot_key, key_confidence.
        camelot_in_comments: Also write Camelot key to COMM field.
    """
    audio = MP3(str(file_path))

    # Ensure ID3 tags exist, using v2.3 for Serato compatibility
    if audio.tags is None:
        audio.add_tags()
    tags = audio.tags

    # Basic metadata
    tags.add(TIT2(encoding=3, text=[metadata.get("title", "")]))
    tags.add(TPE1(encoding=3, text=[metadata.get("artist", "")]))
    tags.add(TALB(encoding=3, text=[metadata.get("album", "")]))

    if metadata.get("track_number"):
        tags.add(TRCK(encoding=3, text=[str(metadata["track_number"])]))

    if metadata.get("year"):
        tags.add(TYER(encoding=3, text=[metadata["year"]]))
        tags.add(TDRC(encoding=3, text=[metadata["year"]]))

    if metadata.get("genre"):
        # Use / separator for Serato compatibility
        tags.add(TCON(encoding=3, text=[metadata["genre"]]))

    # Album artwork
    artwork_url = metadata.get("artwork_url")
    if artwork_url:
        try:
            image_data = urlopen(artwork_url).read()
            tags.add(APIC(
                encoding=3,
                mime="image/jpeg",
                type=3,  # Cover (front)
                desc="Cover",
                data=image_data,
            ))
        except Exception:
            logger.warning("Failed to embed artwork from %s for %s", artwork_url, file_path.name)

    # Analysis data (BPM, key, Camelot)
    if analysis:
        if analysis.get("bpm"):
            tags.add(TBPM(encoding=3, text=[str(int(round(analysis["bpm"])))]))

        if analysis.get("key"):
            tags.add(TKEY(encoding=3, text=[analysis["key"]]))

        if analysis.get("camelot_key"):
            tags.add(TXXX(encoding=3, desc="CamelotKey", text=[analysis["camelot_key"]]))

            if camelot_in_comments:
                tags.add(COMM(encoding=3, lang="eng", desc="", text=[analysis["camelot_key"]]))

        if analysis.get("mix_in") is not None:
            tags.add(TXXX(encoding=3, desc="MixInPoint", text=[str(analysis["mix_in"])]))
        if analysis.get("mix_out") is not None:
            tags.add(TXXX(encoding=3, desc="MixOutPoint", text=[str(analysis["mix_out"])]))

    # Save as ID3v2.3
    audio.save(v2_version=3)
    logger.debug("Tagged %s", file_path.name)
