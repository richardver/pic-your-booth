"""Vocal presence detection from isolated vocal stems."""

import logging
from pathlib import Path

import librosa
import numpy as np

from .config import (
    VOCAL_HEAD_SECONDS,
    VOCAL_MIN_SEGMENT_SECONDS,
    VOCAL_RMS_THRESHOLD,
    VOCAL_TAIL_SECONDS,
)

logger = logging.getLogger(__name__)


def detect_vocal_activity(vocal_stem_path: Path) -> dict:
    """Detect vocal presence from an isolated vocal stem.

    Args:
        vocal_stem_path: Path to the vocal stem audio file.

    Returns:
        Dict with vocal_segments, vocal_pct, vocal_head_pct, vocal_tail_pct.
    """
    y, sr = librosa.load(str(vocal_stem_path), sr=22050, mono=True)
    duration = librosa.get_duration(y=y, sr=sr)

    # Compute RMS energy envelope
    hop_length = 512
    frame_length = 2048
    rms = librosa.feature.rms(y=y, frame_length=frame_length, hop_length=hop_length)[0]
    times = librosa.frames_to_time(np.arange(len(rms)), sr=sr, hop_length=hop_length)
    frame_duration = hop_length / sr

    # Create binary vocal mask from RMS threshold
    mask = rms >= VOCAL_RMS_THRESHOLD

    # Convert mask to time segments
    segments = _mask_to_segments(mask, times)

    # Merge short gaps between segments
    segments = _merge_short_gaps(segments, VOCAL_MIN_SEGMENT_SECONDS)

    # Calculate percentages
    vocal_pct = _total_vocal_time(segments) / duration if duration > 0 else 0.0
    vocal_head_pct = _region_vocal_pct(segments, 0.0, VOCAL_HEAD_SECONDS, duration)
    vocal_tail_pct = _region_vocal_pct(segments, max(0, duration - VOCAL_TAIL_SECONDS), duration, duration)

    logger.debug(
        "%s: vocal_pct=%.1f%%, head=%.1f%%, tail=%.1f%%, %d segments",
        vocal_stem_path.name, vocal_pct * 100, vocal_head_pct * 100,
        vocal_tail_pct * 100, len(segments),
    )

    return {
        "vocal_segments": [[round(s, 3), round(e, 3)] for s, e in segments],
        "vocal_pct": round(vocal_pct, 3),
        "vocal_head_pct": round(vocal_head_pct, 3),
        "vocal_tail_pct": round(vocal_tail_pct, 3),
    }


def _mask_to_segments(mask: np.ndarray, times: np.ndarray) -> list[list[float]]:
    """Convert a boolean frame mask to [[start, end], ...] time segments."""
    segments = []
    in_segment = False
    start = 0.0

    for i, active in enumerate(mask):
        if active and not in_segment:
            start = float(times[i])
            in_segment = True
        elif not active and in_segment:
            end = float(times[i])
            segments.append([start, end])
            in_segment = False

    # Close final segment
    if in_segment and len(times) > 0:
        segments.append([start, float(times[-1])])

    return segments


def _merge_short_gaps(segments: list[list[float]], min_gap: float) -> list[list[float]]:
    """Merge segments separated by gaps shorter than min_gap seconds."""
    if len(segments) <= 1:
        return segments

    merged = [segments[0]]
    for start, end in segments[1:]:
        prev_end = merged[-1][1]
        if start - prev_end < min_gap:
            merged[-1][1] = end
        else:
            merged.append([start, end])

    return merged


def _total_vocal_time(segments: list[list[float]]) -> float:
    """Sum total time across all vocal segments."""
    return sum(end - start for start, end in segments)


def _region_vocal_pct(
    segments: list[list[float]],
    region_start: float,
    region_end: float,
    duration: float,
) -> float:
    """Calculate the fraction of a time region covered by vocal segments."""
    region_length = min(region_end, duration) - region_start
    if region_length <= 0:
        return 0.0

    overlap = 0.0
    for seg_start, seg_end in segments:
        # Clip segment to region
        clipped_start = max(seg_start, region_start)
        clipped_end = min(seg_end, region_end)
        if clipped_end > clipped_start:
            overlap += clipped_end - clipped_start

    return overlap / region_length
