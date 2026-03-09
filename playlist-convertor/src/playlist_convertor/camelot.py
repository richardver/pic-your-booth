"""Camelot Wheel mapping for harmonic mixing."""

# Standard key notation -> Camelot code
# Maps both major and minor keys to their Camelot Wheel position
KEY_TO_CAMELOT = {
    "Ab minor": "1A",  "G# minor": "1A",
    "B major":  "1B",
    "Eb minor": "2A",  "D# minor": "2A",
    "F# major": "2B",  "Gb major": "2B",
    "Bb minor": "3A",  "A# minor": "3A",
    "Db major": "3B",  "C# major": "3B",
    "F minor":  "4A",
    "Ab major": "4B",  "G# major": "4B",
    "C minor":  "5A",
    "Eb major": "5B",  "D# major": "5B",
    "G minor":  "6A",
    "Bb major": "6B",  "A# major": "6B",
    "D minor":  "7A",
    "F major":  "7B",
    "A minor":  "8A",
    "C major":  "8B",
    "E minor":  "9A",
    "G major":  "9B",
    "B minor":  "10A",
    "D major":  "10B",
    "F# minor": "11A", "Gb minor": "11A",
    "A major":  "11B",
    "C# minor": "12A", "Db minor": "12A",
    "E major":  "12B",
}

# Reverse mapping: Camelot code -> standard key
CAMELOT_TO_KEY = {
    "1A": "Ab minor",  "1B": "B major",
    "2A": "Eb minor",  "2B": "F# major",
    "3A": "Bb minor",  "3B": "Db major",
    "4A": "F minor",   "4B": "Ab major",
    "5A": "C minor",   "5B": "Eb major",
    "6A": "G minor",   "6B": "Bb major",
    "7A": "D minor",   "7B": "F major",
    "8A": "A minor",   "8B": "C major",
    "9A": "E minor",   "9B": "G major",
    "10A": "B minor",  "10B": "D major",
    "11A": "F# minor", "11B": "A major",
    "12A": "C# minor", "12B": "E major",
}


def key_to_camelot(key: str) -> str | None:
    """Convert a standard key name to Camelot notation.

    Args:
        key: e.g. "C major", "Ab minor", "F# minor"

    Returns:
        Camelot code like "8B", "1A", "11A", or None if not found.
    """
    return KEY_TO_CAMELOT.get(key)


def compatible_keys(camelot: str) -> list[str]:
    """Return harmonically compatible Camelot keys.

    Compatible keys for mixing:
    - Same key (e.g. 8A -> 8A)
    - +1 / -1 on the wheel (e.g. 8A -> 7A, 9A)
    - Relative major/minor (e.g. 8A -> 8B)
    """
    if len(camelot) < 2:
        return []

    letter = camelot[-1]  # A or B
    number = int(camelot[:-1])

    same = camelot
    minus_one = f"{(number - 2) % 12 + 1}{letter}"
    plus_one = f"{number % 12 + 1}{letter}"
    relative = f"{number}{'B' if letter == 'A' else 'A'}"

    return [same, minus_one, plus_one, relative]


def _parse_camelot(camelot: str) -> tuple[int, str] | None:
    """Parse Camelot code into (number, letter) or None if invalid."""
    if not camelot or len(camelot) < 2:
        return None
    letter = camelot[-1].upper()
    if letter not in ("A", "B"):
        return None
    try:
        number = int(camelot[:-1])
    except ValueError:
        return None
    if not 1 <= number <= 12:
        return None
    return number, letter


def harmonic_distance(key_a: str, key_b: str) -> int:
    """Compute harmonic distance between two Camelot keys.

    Returns tier 1-4:
        1 = perfect:  same key, ±1 on wheel, relative major/minor
        2 = acceptable: ±2 on wheel, diagonal (±1 + mode switch)
        3 = dramatic: semitone shift (±1 + opposite mode via number shift)
        4 = incompatible: everything else
    """
    parsed_a = _parse_camelot(key_a)
    parsed_b = _parse_camelot(key_b)
    if not parsed_a or not parsed_b:
        return 4

    num_a, let_a = parsed_a
    num_b, let_b = parsed_b

    # Circular distance on 12-position wheel
    circle_dist = min((num_a - num_b) % 12, (num_b - num_a) % 12)
    same_mode = let_a == let_b

    # Tier 1: same key, ±1 same mode, relative major/minor (same number, different mode)
    if circle_dist == 0 and same_mode:
        return 1  # same key
    if circle_dist == 1 and same_mode:
        return 1  # ±1 on wheel
    if circle_dist == 0 and not same_mode:
        return 1  # relative major/minor

    # Tier 2: ±2 same mode, diagonal (±1 + mode switch)
    if circle_dist == 2 and same_mode:
        return 2
    if circle_dist == 1 and not same_mode:
        return 2  # diagonal

    # Tier 3: dramatic (±2 + mode switch, ±3 same mode)
    if circle_dist == 2 and not same_mode:
        return 3
    if circle_dist == 3 and same_mode:
        return 3

    # Tier 4: everything else
    return 4
