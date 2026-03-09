"""BPM and key detection using librosa."""

import logging
from pathlib import Path

import librosa
import numpy as np

logger = logging.getLogger(__name__)

# Krumhansl-Schmuckler key profiles
MAJOR_PROFILE = np.array([6.35, 2.23, 3.48, 2.33, 4.38, 4.09, 2.52, 5.19, 2.39, 3.66, 2.29, 2.88])
MINOR_PROFILE = np.array([6.33, 2.68, 3.52, 5.38, 2.60, 3.53, 2.54, 4.75, 3.98, 2.69, 3.34, 3.17])

PITCH_CLASSES = ["C", "C#", "D", "Eb", "E", "F", "F#", "G", "Ab", "A", "Bb", "B"]

# DJ-friendly BPM range
BPM_MIN = 60
BPM_MAX = 180


def detect_bpm(file_path: Path) -> float:
    """Detect BPM of an audio file using librosa.

    Normalizes to DJ range (60-180 BPM) by halving or doubling.
    """
    y, sr = librosa.load(str(file_path), sr=22050, mono=True)
    tempo, _ = librosa.beat.beat_track(y=y, sr=sr)

    # librosa may return an array; extract scalar
    bpm = float(np.atleast_1d(tempo)[0])

    # Normalize to DJ range
    while bpm > BPM_MAX:
        bpm /= 2
    while bpm < BPM_MIN:
        bpm *= 2

    return round(bpm, 1)


def detect_key(file_path: Path) -> tuple[str, float]:
    """Detect musical key using chroma features and Krumhansl-Schmuckler algorithm.

    Returns:
        Tuple of (key_name, confidence) where key_name is e.g. "C major"
        and confidence is 0.0-1.0.
    """
    y, sr = librosa.load(str(file_path), sr=22050, mono=True)
    chroma = librosa.feature.chroma_cqt(y=y, sr=sr)

    # Average chroma across time
    chroma_avg = np.mean(chroma, axis=1)

    # Correlate with all 24 key profiles (12 major + 12 minor)
    best_corr = -1.0
    best_key = "C major"

    for shift in range(12):
        shifted_chroma = np.roll(chroma_avg, -shift)

        major_corr = float(np.corrcoef(shifted_chroma, MAJOR_PROFILE)[0, 1])
        if major_corr > best_corr:
            best_corr = major_corr
            best_key = f"{PITCH_CLASSES[shift]} major"

        minor_corr = float(np.corrcoef(shifted_chroma, MINOR_PROFILE)[0, 1])
        if minor_corr > best_corr:
            best_corr = minor_corr
            best_key = f"{PITCH_CLASSES[shift]} minor"

    # Normalize confidence to 0-1 range (correlation can be -1 to 1)
    confidence = max(0.0, (best_corr + 1) / 2)

    return best_key, round(confidence, 3)


def _snap_to_beat(time_s: float, beat_times: np.ndarray) -> float:
    """Snap a time position to the nearest beat."""
    if len(beat_times) == 0:
        return time_s
    idx = np.argmin(np.abs(beat_times - time_s))
    return float(beat_times[idx])


def detect_mix_points(file_path: Path, bpm: float) -> dict | None:
    """Detect optimal mix-in and mix-out points using energy analysis.

    Returns dict with mix_in, mix_out, mix_in_confidence, mix_out_confidence,
    or None for tracks too short to analyze.
    """
    from .config import (
        MIX_IN_MAX_POSITION,
        MIX_OUT_MIN_POSITION,
        MIX_POINT_ENERGY_THRESHOLD,
        MIX_POINT_FALLBACK_BEATS,
        MIX_POINT_MIN_TRACK_DURATION,
        MIX_POINT_SMOOTHING_SECONDS,
        MIX_POINT_SUSTAIN_BEATS,
    )

    y, sr = librosa.load(str(file_path), sr=22050, mono=True)
    duration = librosa.get_duration(y=y, sr=sr)

    if duration < MIX_POINT_MIN_TRACK_DURATION:
        logger.debug("%s: too short (%.1fs), skipping mix points", file_path.name, duration)
        return None

    # Compute RMS energy envelope
    frame_length = 2048
    hop_length = 512
    rms = librosa.feature.rms(y=y, frame_length=frame_length, hop_length=hop_length)[0]
    rms_times = librosa.frames_to_time(np.arange(len(rms)), sr=sr, hop_length=hop_length)

    # Smooth with a window
    smooth_frames = int(MIX_POINT_SMOOTHING_SECONDS * sr / hop_length)
    if smooth_frames > 1:
        kernel = np.ones(smooth_frames) / smooth_frames
        rms = np.convolve(rms, kernel, mode="same")

    # Get beat grid
    _, beat_frames = librosa.beat.beat_track(y=y, sr=sr, bpm=bpm)
    beat_times = librosa.frames_to_time(beat_frames, sr=sr)

    if len(beat_times) < 4:
        logger.debug("%s: too few beats, skipping mix points", file_path.name)
        return None

    # Body = middle 50% of the track; compute median energy as reference
    body_start_idx = len(rms) // 4
    body_end_idx = 3 * len(rms) // 4
    body_median = float(np.median(rms[body_start_idx:body_end_idx]))

    if body_median <= 0:
        logger.debug("%s: flat energy, using fallback", file_path.name)
        beat_dur = 60.0 / bpm
        mix_in = _snap_to_beat(MIX_POINT_FALLBACK_BEATS * beat_dur, beat_times)
        mix_out = _snap_to_beat(duration - MIX_POINT_FALLBACK_BEATS * beat_dur, beat_times)
        return {
            "mix_in": round(mix_in, 3),
            "mix_out": round(mix_out, 3),
            "mix_in_confidence": 0.3,
            "mix_out_confidence": 0.3,
        }

    threshold = MIX_POINT_ENERGY_THRESHOLD * body_median
    beat_dur = 60.0 / bpm
    sustain_window = MIX_POINT_SUSTAIN_BEATS * beat_dur
    max_mix_in_time = MIX_IN_MAX_POSITION * duration
    min_mix_out_time = MIX_OUT_MIN_POSITION * duration

    # --- Mix-in: scan from start, find first sustained crossing above threshold ---
    mix_in_time = None
    mix_in_conf = 0.3
    for i, t in enumerate(rms_times):
        if t > max_mix_in_time:
            break
        if rms[i] >= threshold:
            # Check sustained: all frames within the sustain window above threshold
            end_t = t + sustain_window
            sustain_mask = (rms_times >= t) & (rms_times <= end_t)
            if np.all(rms[sustain_mask] >= threshold * 0.9):
                mix_in_time = t
                # Confidence: how sharp the energy contrast is at this boundary
                pre_energy = float(np.mean(rms[max(0, i - smooth_frames):i])) if i > 0 else 0
                contrast = (rms[i] - pre_energy) / body_median if body_median > 0 else 0
                mix_in_conf = min(1.0, 0.5 + contrast)
                break

    if mix_in_time is None:
        mix_in_time = MIX_POINT_FALLBACK_BEATS * beat_dur
        mix_in_conf = 0.3

    mix_in_time = min(mix_in_time, max_mix_in_time)
    mix_in_time = _snap_to_beat(mix_in_time, beat_times)

    # --- Mix-out: scan from end backward, find where energy drops below threshold ---
    mix_out_time = None
    mix_out_conf = 0.3
    for i in range(len(rms_times) - 1, -1, -1):
        t = rms_times[i]
        if t < min_mix_out_time:
            break
        if rms[i] >= threshold:
            # Check sustained: frames just before this point are above threshold
            start_t = t - sustain_window
            sustain_mask = (rms_times >= start_t) & (rms_times <= t)
            if np.all(rms[sustain_mask] >= threshold * 0.9):
                mix_out_time = t
                # Confidence from energy contrast at the boundary
                post_start = min(i + 1, len(rms) - 1)
                post_end = min(i + smooth_frames + 1, len(rms))
                post_energy = float(np.mean(rms[post_start:post_end])) if post_end > post_start else 0
                contrast = (rms[i] - post_energy) / body_median if body_median > 0 else 0
                mix_out_conf = min(1.0, 0.5 + contrast)
                break

    if mix_out_time is None:
        mix_out_time = duration - MIX_POINT_FALLBACK_BEATS * beat_dur
        mix_out_conf = 0.3

    mix_out_time = max(mix_out_time, min_mix_out_time)
    mix_out_time = _snap_to_beat(mix_out_time, beat_times)

    # Ensure mix_out > mix_in
    if mix_out_time <= mix_in_time:
        mix_out_time = _snap_to_beat(duration - MIX_POINT_FALLBACK_BEATS * beat_dur, beat_times)

    logger.debug(
        "%s: mix_in=%.3fs (conf=%.2f), mix_out=%.3fs (conf=%.2f)",
        file_path.name, mix_in_time, mix_in_conf, mix_out_time, mix_out_conf,
    )

    return {
        "mix_in": round(mix_in_time, 3),
        "mix_out": round(mix_out_time, 3),
        "mix_in_confidence": round(mix_in_conf, 2),
        "mix_out_confidence": round(mix_out_conf, 2),
    }


def analyze_track(
    file_path: Path,
    analyze_mix_points: bool = False,
    analyze_energy: bool = False,
    analyze_stems: bool = False,
    stem_model: str = "htdemucs",
    stems_output_dir: Path | None = None,
) -> dict:
    """Run full analysis on a track.

    Returns dict with bpm, key, camelot_key, key_confidence.
    When analyze_mix_points is True, also includes mix_in, mix_out, and confidence scores.
    When analyze_energy is True, also includes energy (1-10), rms_median, spectral_centroid, onset_density.
    When analyze_stems is True, runs Demucs separation, stem-enhanced energy, and vocal activity.
    """
    from .camelot import key_to_camelot

    bpm = detect_bpm(file_path)
    key, confidence = detect_key(file_path)
    camelot = key_to_camelot(key)

    logger.debug(
        "%s -> BPM=%.1f, Key=%s (confidence=%.3f), Camelot=%s",
        file_path.name, bpm, key, confidence, camelot or "?",
    )

    result = {
        "bpm": bpm,
        "key": key,
        "camelot_key": camelot or "",
        "key_confidence": confidence,
    }

    if analyze_mix_points:
        mix_points = detect_mix_points(file_path, bpm)
        if mix_points:
            result.update(mix_points)

    if analyze_stems:
        from .stems import separate_track
        from .energy import detect_energy_from_stems
        from .vocal_activity import detect_vocal_activity

        if stems_output_dir is None:
            stems_output_dir = file_path.parent / "stems" / file_path.stem

        # Step 1: Separate stems
        stem_result = separate_track(file_path, stems_output_dir, model_name=stem_model)
        result["stems_path"] = stem_result["stems_path"]
        result["has_stems"] = True

        # Step 2: Stem-enhanced energy (from drums + bass)
        if stem_result["drums"] and stem_result["bass"]:
            energy_data = detect_energy_from_stems(
                Path(stem_result["drums"]), Path(stem_result["bass"])
            )
            result.update(energy_data)
            logger.debug("%s -> Stem energy=%d", file_path.name, energy_data["energy"])

        # Step 3: Vocal activity detection
        if stem_result["vocals"]:
            vocal_data = detect_vocal_activity(Path(stem_result["vocals"]))
            result.update(vocal_data)
            logger.debug(
                "%s -> Vocal: %.0f%% total, head=%.0f%%, tail=%.0f%%",
                file_path.name, vocal_data["vocal_pct"] * 100,
                vocal_data["vocal_head_pct"] * 100, vocal_data["vocal_tail_pct"] * 100,
            )

    elif analyze_energy:
        from .energy import detect_energy

        energy_data = detect_energy(file_path)
        result.update(energy_data)
        logger.debug("%s -> Energy=%d", file_path.name, energy_data["energy"])

    return result
