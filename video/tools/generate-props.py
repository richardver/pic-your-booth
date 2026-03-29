#!/usr/bin/env python3
"""
Generate Remotion props.json from audio analysis + user inputs.

Usage:
  python generate-props.py \
    --analysis path/to/analysis.json \
    --dj milo \
    --genre house \
    --series "House Grooves Vol 1" \
    --video1 footage/angle1.mp4 \
    --video2 footage/angle2.mp4 \
    --cover covers/milo-house.png \
    --hook "deep in the groove." \
    --output path/to/props.json
"""

import argparse
import json
import sys
from pathlib import Path

# --- Constants ---

DJ_DISPLAY_NAMES = {
    "gianni": "DJ GIANNI",
    "milo": "MILØ",
}

GENRE_TAGS = {
    "afro": ["Afro Beats", "Amapiano", "Afro House"],
    "caribbean": ["Caribbean", "Dancehall", "Reggaeton"],
    "urban": ["Urban", "Hip-Hop", "R&B"],
    "house": ["Tech House", "House", "Deep"],
    "techno": ["Techno", "Melodic Techno", "Dark"],
    "deep": ["Deep House", "Organic House", "Chill"],
}

DEFAULT_HOOKS = {
    "gianni": "feel the vibe.",
    "milo": "lose yourself.",
}

DEFAULT_DURATION_SEC = 25
FPS = 30
WINDOW_SEC = 0.5


def parse_args():
    parser = argparse.ArgumentParser(
        description="Generate Remotion props.json from audio analysis + user inputs."
    )
    parser.add_argument(
        "--analysis", required=True, help="Path to analysis.json from audio analyzer"
    )
    parser.add_argument(
        "--dj",
        required=True,
        choices=["gianni", "milo"],
        help="DJ profile: gianni or milo",
    )
    parser.add_argument(
        "--genre",
        required=True,
        choices=list(GENRE_TAGS.keys()),
        help="Genre identifier",
    )
    parser.add_argument("--series", required=True, help='Series name, e.g. "Afro Beats Vol 2"')
    parser.add_argument("--video1", required=True, help="Path to video angle 1 (hook, build-up, vibe)")
    parser.add_argument("--video2", required=True, help="Path to video angle 2 (pre-drop, drop)")
    parser.add_argument("--cover", required=True, help="Path to cover art image")
    parser.add_argument("--hook", default=None, help="Hook text (defaults to DJ-specific hook)")
    parser.add_argument("--output", default="props.json", help="Output path for props.json")
    parser.add_argument(
        "--duration",
        type=int,
        default=DEFAULT_DURATION_SEC,
        help=f"Clip duration in seconds (default: {DEFAULT_DURATION_SEC})",
    )
    return parser.parse_args()


def load_analysis(path: str) -> dict:
    analysis_path = Path(path)
    if not analysis_path.exists():
        print(f"Error: Analysis file not found: {path}", file=sys.stderr)
        sys.exit(1)
    try:
        with open(analysis_path) as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in {path}: {e}", file=sys.stderr)
        sys.exit(1)


def slice_energy_data(energy_data: list[float], start_sec: float, duration_sec: int) -> list[float]:
    """Slice energy_data to the clip window.

    energy_data has one value per WINDOW_SEC (0.5s).
    We need `duration_sec / WINDOW_SEC` values starting from the clip start.
    """
    start_index = int(start_sec / WINDOW_SEC)
    num_values = int(duration_sec / WINDOW_SEC)
    sliced = energy_data[start_index : start_index + num_values]

    # Pad with zeros if the source audio is shorter than the clip
    if len(sliced) < num_values:
        sliced.extend([0.0] * (num_values - len(sliced)))

    return sliced


def calculate_drop_timestamp(clip: dict) -> int:
    """Calculate drop frame number relative to clip start.

    The analyzer provides drop_in_clip_sec (seconds from clip start to drop).
    Convert to frame number at 30fps.
    """
    if "drop_in_clip_sec" in clip:
        return int(clip["drop_in_clip_sec"] * FPS)

    # Fallback: calculate from absolute values
    if "drop_at_sec" in clip and "start_sec" in clip:
        drop_in_clip = clip["drop_at_sec"] - clip["start_sec"]
        return int(drop_in_clip * FPS)

    # Last resort: use drop_at_frame_30fps relative to start_frame_30fps
    if "drop_at_frame_30fps" in clip and "start_frame_30fps" in clip:
        return clip["drop_at_frame_30fps"] - clip["start_frame_30fps"]

    print("Warning: Could not determine drop timestamp, defaulting to frame 0", file=sys.stderr)
    return 0


def generate_props(args, analysis: dict) -> dict:
    clip = analysis.get("recommended_clip", {})
    energy_data = analysis.get("energy_data", [])

    start_sec = clip.get("start_sec", 0.0)
    duration_sec = args.duration

    # Slice energy data to clip window
    clipped_energy = slice_energy_data(energy_data, start_sec, duration_sec)

    # Drop timestamp (frame relative to clip start)
    drop_timestamp = calculate_drop_timestamp(clip)

    # Calculate beat-synced cut points for Milø
    cut_points = []
    if args.dj == 'milo':
        transients = analysis.get('transients', [])
        clip_start = clip.get('start_sec', 0.0)

        # Filter transients to the set section (3s-19s into clip)
        set_start = clip_start + 3
        set_end = clip_start + 19

        set_transients = [t for t in transients if set_start <= t <= set_end]

        # Pick every Nth transient to get cuts every 4-8 seconds
        if set_transients:
            target_cuts = 4  # aim for 4-5 cuts in 16 seconds
            step = max(1, len(set_transients) // target_cuts)
            selected = set_transients[::step][:5]

            # Convert to frame numbers relative to clip start
            cut_points = [int((t - clip_start) * 30) for t in selected]
            print(f"  Cut points: {cut_points} ({len(cut_points)} angle switches)")

    # Hook text
    hook_text = args.hook if args.hook else DEFAULT_HOOKS.get(args.dj, "feel the music.")

    return {
        "genre": args.genre,
        "djProfile": args.dj,
        "djName": DJ_DISPLAY_NAMES[args.dj],
        "serieName": args.series,
        "genreTags": GENRE_TAGS[args.genre],
        "hookText": hook_text,
        "videoSrc1": args.video1,
        "videoSrc2": args.video2,
        "videoStartSec": start_sec,
        "dropTimestamp": drop_timestamp,
        "energyData": clipped_energy,
        "coverArtSrc": args.cover,
        "durationSec": duration_sec,
        "cutPoints": cut_points,
    }


def main():
    args = parse_args()

    analysis = load_analysis(args.analysis)
    props = generate_props(args, analysis)

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w") as f:
        json.dump(props, f, indent=2)

    print(f"Props written to {output_path}")
    print(f"  DJ: {props['djName']}")
    print(f"  Genre: {props['genre']} -> {props['genreTags']}")
    print(f"  Series: {props['serieName']}")
    print(f"  Hook: \"{props['hookText']}\"")
    print(f"  Clip: {props['videoStartSec']}s, {props['durationSec']}s duration")
    print(f"  Drop at frame: {props['dropTimestamp']} ({props['dropTimestamp'] / FPS:.1f}s into clip)")
    print(f"  Energy data: {len(props['energyData'])} values")


if __name__ == "__main__":
    main()
