"""Energy estimation from audio features."""

import logging
from pathlib import Path

import librosa
import numpy as np

from .config import (
    ENERGY_CENTROID_CEILING,
    ENERGY_ONSET_CEILING,
    ENERGY_RMS_CEILING,
    ENERGY_WEIGHT_CENTROID,
    ENERGY_WEIGHT_ONSET,
    ENERGY_WEIGHT_RMS,
    STEM_ENERGY_WEIGHT_BASS,
    STEM_ENERGY_WEIGHT_DRUMS,
)

logger = logging.getLogger(__name__)


def _compute_energy_features(y: np.ndarray, sr: int) -> dict:
    """Compute energy features from audio signal.

    Returns dict with rms_median, spectral_centroid, onset_density, raw_score (0-1).
    """
    frame_length = 2048
    hop_length = 512
    rms = librosa.feature.rms(y=y, frame_length=frame_length, hop_length=hop_length)[0]
    body_start = len(rms) // 4
    body_end = 3 * len(rms) // 4
    rms_median = float(np.median(rms[body_start:body_end]))

    centroid = librosa.feature.spectral_centroid(y=y, sr=sr, hop_length=hop_length)[0]
    centroid_median = float(np.median(centroid[body_start:body_end]))

    onset_frames = librosa.onset.onset_detect(y=y, sr=sr, hop_length=hop_length)
    duration = librosa.get_duration(y=y, sr=sr)
    onset_density = len(onset_frames) / duration if duration > 0 else 0.0

    rms_norm = min(1.0, rms_median / ENERGY_RMS_CEILING)
    centroid_norm = min(1.0, centroid_median / ENERGY_CENTROID_CEILING)
    onset_norm = min(1.0, onset_density / ENERGY_ONSET_CEILING)

    raw_score = (
        ENERGY_WEIGHT_RMS * rms_norm
        + ENERGY_WEIGHT_CENTROID * centroid_norm
        + ENERGY_WEIGHT_ONSET * onset_norm
    )

    return {
        "rms_median": round(rms_median, 6),
        "spectral_centroid": round(centroid_median, 1),
        "onset_density": round(onset_density, 2),
        "raw_score": raw_score,
    }


def _score_to_energy(raw_score: float) -> int:
    """Convert a 0-1 raw score to a 1-10 integer energy level."""
    return max(1, min(10, round(raw_score * 9 + 1)))


def detect_energy(file_path: Path) -> dict:
    """Compute energy score 1-10 from audio features.

    Uses weighted combination of:
    - RMS loudness (body median, middle 50%)
    - Spectral centroid (brightness / perceived energy)
    - Onset density (rhythmic intensity, onsets per second)

    Returns dict with energy, rms_median, spectral_centroid, onset_density.
    """
    y, sr = librosa.load(str(file_path), sr=22050, mono=True)
    features = _compute_energy_features(y, sr)
    energy = _score_to_energy(features["raw_score"])

    logger.debug(
        "%s: energy=%d (rms=%.4f, centroid=%.0f, onsets=%.2f/s)",
        file_path.name, energy, features["rms_median"],
        features["spectral_centroid"], features["onset_density"],
    )

    return {
        "energy": energy,
        "rms_median": features["rms_median"],
        "spectral_centroid": features["spectral_centroid"],
        "onset_density": features["onset_density"],
    }


def detect_energy_from_stems(drums_path: Path, bass_path: Path) -> dict:
    """Compute energy score from isolated drum and bass stems.

    Analyzes each stem separately and combines with configured weights
    (drums 55%, bass 45% by default).

    Returns same dict shape as detect_energy() plus stem_enhanced: True.
    """
    y_drums, sr_drums = librosa.load(str(drums_path), sr=22050, mono=True)
    y_bass, sr_bass = librosa.load(str(bass_path), sr=22050, mono=True)

    drums_features = _compute_energy_features(y_drums, sr_drums)
    bass_features = _compute_energy_features(y_bass, sr_bass)

    # Weighted combination of drum and bass energy
    combined_score = (
        STEM_ENERGY_WEIGHT_DRUMS * drums_features["raw_score"]
        + STEM_ENERGY_WEIGHT_BASS * bass_features["raw_score"]
    )
    energy = _score_to_energy(combined_score)

    logger.debug(
        "Stem energy: drums=%.3f bass=%.3f combined=%d",
        drums_features["raw_score"], bass_features["raw_score"], energy,
    )

    return {
        "energy": energy,
        "rms_median": round(
            STEM_ENERGY_WEIGHT_DRUMS * drums_features["rms_median"]
            + STEM_ENERGY_WEIGHT_BASS * bass_features["rms_median"],
            6,
        ),
        "spectral_centroid": round(
            STEM_ENERGY_WEIGHT_DRUMS * drums_features["spectral_centroid"]
            + STEM_ENERGY_WEIGHT_BASS * bass_features["spectral_centroid"],
            1,
        ),
        "onset_density": round(
            STEM_ENERGY_WEIGHT_DRUMS * drums_features["onset_density"]
            + STEM_ENERGY_WEIGHT_BASS * bass_features["onset_density"],
            2,
        ),
        "stem_enhanced": True,
    }
