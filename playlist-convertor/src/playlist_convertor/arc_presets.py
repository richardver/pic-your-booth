"""Energy arc presets for DJ set building."""

PRESETS = {
    "warm-up": {
        "name": "Warm-Up",
        "description": "Opening set, gentle build to moderate energy",
        "curve": [
            (0.0, 2), (0.25, 3), (0.50, 5), (0.75, 7), (1.0, 6),
        ],
        "bpm_climb": 6,
        "bpm_ease": 2,
    },
    "peak-time": {
        "name": "Peak Time",
        "description": "Classic 4-act arc, peak at 2/3",
        "curve": [
            (0.0, 3), (0.20, 5), (0.40, 7), (0.65, 10), (0.80, 8), (1.0, 5),
        ],
        "bpm_climb": 8,
        "bpm_ease": 4,
    },
    "marathon": {
        "name": "Marathon",
        "description": "Waves with increasing intensity, 3h+ sets",
        "curve": [
            (0.0, 2), (0.10, 4), (0.20, 3), (0.35, 5),
            (0.50, 7), (0.60, 5), (0.75, 8), (0.85, 10),
            (0.92, 7), (1.0, 4),
        ],
        "bpm_climb": 10,
        "bpm_ease": 6,
    },
    "chill": {
        "name": "Chill",
        "description": "Lounge / after-party, low energy throughout",
        "curve": [
            (0.0, 2), (0.20, 3), (0.40, 4), (0.60, 5), (0.80, 4), (1.0, 3),
        ],
        "bpm_climb": 4,
        "bpm_ease": 2,
    },
    "closer": {
        "name": "Closer",
        "description": "Last set of the night, start high and wind down",
        "curve": [
            (0.0, 7), (0.15, 9), (0.35, 8), (0.55, 6), (0.75, 4), (1.0, 3),
        ],
        "bpm_climb": 2,
        "bpm_ease": 8,
    },
}


def get_target_energy(preset_name: str, position: float) -> float:
    """Interpolate energy at a position (0.0-1.0) along the preset curve."""
    preset = PRESETS.get(preset_name)
    if not preset:
        raise ValueError(f"Unknown preset: {preset_name}")

    curve = preset["curve"]
    position = max(0.0, min(1.0, position))

    # Find surrounding control points
    for i in range(len(curve) - 1):
        pos_a, energy_a = curve[i]
        pos_b, energy_b = curve[i + 1]
        if pos_a <= position <= pos_b:
            # Linear interpolation
            t = (position - pos_a) / (pos_b - pos_a) if pos_b != pos_a else 0
            return energy_a + t * (energy_b - energy_a)

    # Fallback: return last point
    return curve[-1][1]


def get_target_bpm(preset_name: str, position: float, bpm_min: float, bpm_max: float) -> float:
    """Interpolate target BPM at a position along the preset's BPM progression.

    BPM climbs from bpm_min toward bpm_max at the peak, then eases back.
    """
    preset = PRESETS.get(preset_name)
    if not preset:
        raise ValueError(f"Unknown preset: {preset_name}")

    peak_pos = _find_peak_position(preset_name)
    bpm_range = bpm_max - bpm_min

    if position <= peak_pos:
        # Climbing phase
        t = position / peak_pos if peak_pos > 0 else 1.0
        climb_frac = min(preset["bpm_climb"], bpm_range) / bpm_range if bpm_range > 0 else 0
        return bpm_min + t * climb_frac * bpm_range
    else:
        # Easing phase
        t = (position - peak_pos) / (1.0 - peak_pos) if peak_pos < 1.0 else 0
        climb_frac = min(preset["bpm_climb"], bpm_range) / bpm_range if bpm_range > 0 else 0
        ease_frac = min(preset["bpm_ease"], bpm_range) / bpm_range if bpm_range > 0 else 0
        peak_bpm = bpm_min + climb_frac * bpm_range
        end_bpm = peak_bpm - ease_frac * bpm_range
        end_bpm = max(bpm_min, end_bpm)
        return peak_bpm - t * (peak_bpm - end_bpm)


def _find_peak_position(preset_name: str) -> float:
    """Find the position (0.0-1.0) of maximum energy in a preset's curve."""
    preset = PRESETS[preset_name]
    curve = preset["curve"]
    max_energy = -1
    peak_pos = 0.5
    for pos, energy in curve:
        if energy > max_energy:
            max_energy = energy
            peak_pos = pos
    return peak_pos


def list_presets() -> list[dict]:
    """Return preset summaries for display."""
    return [
        {
            "key": key,
            "name": p["name"],
            "description": p["description"],
            "energy_range": f"{p['curve'][0][1]}-{max(e for _, e in p['curve'])}",
        }
        for key, p in PRESETS.items()
    ]
