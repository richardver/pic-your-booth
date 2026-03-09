"""Auto set builder — greedy Camelot-guided sequencing with energy arc enforcement."""

import logging
from dataclasses import dataclass, field
from pathlib import Path

from .arc_presets import get_target_bpm, get_target_energy, PRESETS
from .camelot import harmonic_distance
from .config import DEFAULT_SET_PRESET, DEFAULT_TRACK_DURATION, DEFAULT_TRANSITION_OVERLAP
from .library import get_all_songs

logger = logging.getLogger(__name__)

# Scoring weights (without vocal scoring)
W_HARMONIC = 0.35
W_BPM_ARC = 0.25
W_ENERGY_ARC = 0.25
W_BPM_SMOOTH = 0.15

# Scoring weights (with vocal scoring)
W_HARMONIC_V = 0.30
W_BPM_ARC_V = 0.22
W_ENERGY_ARC_V = 0.23
W_BPM_SMOOTH_V = 0.15
W_VOCAL = 0.10

# Harmonic tier -> score mapping
HARMONIC_SCORES = {1: 1.0, 2: 0.6, 3: 0.3, 4: 0.0}


@dataclass
class SetResult:
    tracks: list[dict] = field(default_factory=list)
    transitions: list[dict] = field(default_factory=list)
    preset: str = ""
    estimated_minutes: float = 0.0
    tracks_needed: int = 0
    candidates_available: int = 0
    xml_path: object = None       # Path to Rekordbox XML (set by setbuilder)
    m3u8_path: object = None     # Path to Serato M3U8 (set by setbuilder)
    serato_report: dict | None = None  # Serato compat report (set by setbuilder)
    set_name: str = ""            # Generated set name (set by setbuilder)


def build_auto_set(
    set_minutes: int,
    preset_name: str = DEFAULT_SET_PRESET,
    bpm_min: float | None = None,
    bpm_max: float | None = None,
    start_key: str | None = None,
    playlists: list[str] | None = None,
    use_vocal_scoring: bool = False,
) -> SetResult:
    """Build an optimally sequenced set from the library.

    Args:
        set_minutes: Target set length in minutes.
        preset_name: Energy arc preset key.
        bpm_min: Minimum BPM filter (inclusive).
        bpm_max: Maximum BPM filter (inclusive).
        start_key: Optional Camelot key for the first track (e.g. "8A").
        playlists: Optional list of playlist names to filter by.

    Returns:
        SetResult with ordered tracks and transition ratings.
    """
    if preset_name not in PRESETS:
        raise ValueError(f"Unknown preset: {preset_name}. Options: {', '.join(PRESETS)}")

    # Step 1: Filter library to analyzed tracks within BPM range
    all_songs = get_all_songs()
    candidates = []
    for song in all_songs:
        if not song.get("bpm") or not song.get("camelot_key"):
            continue
        if bpm_min is not None and song["bpm"] < bpm_min:
            continue
        if bpm_max is not None and song["bpm"] > bpm_max:
            continue
        if playlists and not any(p in song.get("playlists", []) for p in playlists):
            continue
        if not Path(song.get("file_path", "")).exists():
            continue
        candidates.append(song)

    if not candidates:
        logger.warning("No candidates match the filters")
        return SetResult(preset=preset_name, candidates_available=0)

    # Step 2: Calculate tracks needed
    effective_track_time = DEFAULT_TRACK_DURATION - DEFAULT_TRANSITION_OVERLAP
    tracks_needed = max(1, round(set_minutes * 60 / effective_track_time))
    tracks_needed = min(tracks_needed, len(candidates))

    # Determine BPM range from candidates if not specified
    effective_bpm_min = bpm_min or min(s["bpm"] for s in candidates)
    effective_bpm_max = bpm_max or max(s["bpm"] for s in candidates)

    logger.info(
        "Auto set: %d min, preset=%s, BPM=%.0f-%.0f, %d candidates, need %d tracks",
        set_minutes, preset_name, effective_bpm_min, effective_bpm_max,
        len(candidates), tracks_needed,
    )

    # Step 3-4: Greedy selection
    selected = []
    remaining = list(candidates)

    for slot in range(tracks_needed):
        position = slot / max(1, tracks_needed - 1)

        # Get arc targets for this position
        target_energy = get_target_energy(preset_name, position)
        target_bpm = get_target_bpm(preset_name, position, effective_bpm_min, effective_bpm_max)

        prev = selected[-1] if selected else None

        # Special handling for first track with start_key constraint
        if slot == 0 and start_key:
            key_matches = [c for c in remaining if c["camelot_key"] == start_key.upper()]
            if key_matches:
                # Pick closest to target energy/BPM among key matches
                best = min(
                    key_matches,
                    key=lambda c: abs(_get_energy(c) - target_energy) + abs(c["bpm"] - target_bpm) * 0.1,
                )
                selected.append(best)
                remaining.remove(best)
                continue

        # Score every remaining candidate
        best_score = -1.0
        best_candidate = None

        for candidate in remaining:
            score = _score_candidate(prev, candidate, target_energy, target_bpm, use_vocal_scoring)
            if score > best_score:
                best_score = score
                best_candidate = candidate

        if best_candidate:
            selected.append(best_candidate)
            remaining.remove(best_candidate)

    # Step 5: Score transitions
    transitions = []
    for i in range(len(selected) - 1):
        transition = _score_transition(selected[i], selected[i + 1], use_vocal_scoring)
        transitions.append(transition)

    # Step 6: Estimate duration
    estimated = _estimate_duration(selected, DEFAULT_TRANSITION_OVERLAP)

    result = SetResult(
        tracks=selected,
        transitions=transitions,
        preset=preset_name,
        estimated_minutes=round(estimated, 1),
        tracks_needed=tracks_needed,
        candidates_available=len(candidates),
    )

    logger.info(
        "Auto set built: %d tracks, ~%.0f min, %d green / %d yellow / %d red transitions",
        len(selected), estimated,
        sum(1 for t in transitions if t["rating"] == "green"),
        sum(1 for t in transitions if t["rating"] == "yellow"),
        sum(1 for t in transitions if t["rating"] == "red"),
    )

    return result


def _get_energy(song: dict) -> float:
    """Get energy score, falling back to BPM-as-proxy."""
    if song.get("energy"):
        return float(song["energy"])
    return _bpm_to_rough_energy(song.get("bpm", 120))


def _bpm_to_rough_energy(bpm: float) -> float:
    """Map BPM to a rough 1-10 energy proxy."""
    # 70 BPM -> ~2, 100 BPM -> ~4, 128 BPM -> ~7, 150+ BPM -> ~9
    return max(1.0, min(10.0, (bpm - 60) / 12 + 1))


def _score_vocal_compatibility(prev: dict, candidate: dict) -> float:
    """Score vocal compatibility at a transition point (0-1, higher is better).

    Lower vocal activity at transition boundaries = higher score.
    Returns neutral 0.5 when vocal data is missing.
    """
    prev_tail = prev.get("vocal_tail_pct")
    cand_head = candidate.get("vocal_head_pct")

    if prev_tail is None and cand_head is None:
        return 0.5  # neutral when no data

    # Average vocal presence at the transition boundary
    tail = prev_tail if prev_tail is not None else 0.5
    head = cand_head if cand_head is not None else 0.5
    avg_vocal = (tail + head) / 2

    # Less vocals = better score for transitions
    return 1.0 - avg_vocal


def _score_candidate(
    prev: dict | None,
    candidate: dict,
    target_energy: float,
    target_bpm: float,
    use_vocal_scoring: bool = False,
) -> float:
    """Score a candidate for a slot. Higher is better."""
    energy = _get_energy(candidate)
    bpm = candidate["bpm"]

    # Energy proximity to arc target (0-1)
    energy_score = max(0.0, 1.0 - abs(energy - target_energy) / 10.0)

    # BPM proximity to arc target (0-1)
    bpm_arc_score = max(0.0, 1.0 - abs(bpm - target_bpm) / 20.0)

    if prev is None:
        # First track: only energy and BPM arc matter
        w_e = W_ENERGY_ARC_V if use_vocal_scoring else W_ENERGY_ARC
        w_b = W_BPM_ARC_V if use_vocal_scoring else W_BPM_ARC
        return w_e * energy_score + w_b * bpm_arc_score

    # Harmonic compatibility with previous track
    tier = harmonic_distance(prev.get("camelot_key", ""), candidate.get("camelot_key", ""))
    harmonic_score = HARMONIC_SCORES.get(tier, 0.0)

    # BPM smoothness from previous track (penalize large jumps)
    bpm_jump = abs(prev["bpm"] - bpm)
    smooth_score = max(0.0, 1.0 - bpm_jump / 10.0)

    if use_vocal_scoring:
        vocal_score = _score_vocal_compatibility(prev, candidate)
        return (
            W_HARMONIC_V * harmonic_score
            + W_BPM_ARC_V * bpm_arc_score
            + W_ENERGY_ARC_V * energy_score
            + W_BPM_SMOOTH_V * smooth_score
            + W_VOCAL * vocal_score
        )

    return (
        W_HARMONIC * harmonic_score
        + W_BPM_ARC * bpm_arc_score
        + W_ENERGY_ARC * energy_score
        + W_BPM_SMOOTH * smooth_score
    )


def _score_transition(track_a: dict, track_b: dict, use_vocal_scoring: bool = False) -> dict:
    """Rate the transition between two adjacent tracks."""
    tier = harmonic_distance(
        track_a.get("camelot_key", ""),
        track_b.get("camelot_key", ""),
    )
    bpm_jump = abs(track_a["bpm"] - track_b["bpm"])

    # Rating: green (smooth), yellow (workable), red (rough)
    if tier <= 1 and bpm_jump <= 3:
        rating = "green"
    elif tier <= 2 and bpm_jump <= 6:
        rating = "yellow"
    else:
        rating = "red"

    result = {
        "from_idx": 0,  # will be set by caller context
        "to_idx": 0,
        "harmonic_tier": tier,
        "bpm_jump": round(bpm_jump, 1),
        "rating": rating,
        "from_key": track_a.get("camelot_key", ""),
        "to_key": track_b.get("camelot_key", ""),
    }

    if use_vocal_scoring:
        vocal_score = _score_vocal_compatibility(track_a, track_b)
        result["vocal_score"] = round(vocal_score, 2)
        # Thresholds for warnings/boosts
        if vocal_score < 0.3:
            result["vocal_warning"] = True
        elif vocal_score > 0.7:
            result["vocal_boost"] = True

    return result


def _estimate_duration(tracks: list[dict], overlap: int) -> float:
    """Estimate total set duration in minutes, accounting for transition overlaps."""
    if not tracks:
        return 0.0

    total_seconds = 0.0
    for i, track in enumerate(tracks):
        # Use actual duration if available, else fallback
        if track.get("duration_ms"):
            track_seconds = track["duration_ms"] / 1000
        elif track.get("mix_in") is not None and track.get("mix_out") is not None:
            track_seconds = track["mix_out"] - track["mix_in"]
        else:
            track_seconds = DEFAULT_TRACK_DURATION

        # Subtract overlap for all but the first track
        if i > 0:
            track_seconds -= overlap

        total_seconds += max(0, track_seconds)

    return total_seconds / 60
