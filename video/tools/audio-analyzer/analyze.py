#!/usr/bin/env python3
"""
Audio Analyzer — Find the best clip moments in a video/audio file.

Extracts audio via ffmpeg, computes RMS energy per window,
detects peaks (drops), and recommends the best clip window.

Outputs:
  - analysis.json  (timestamps, energy data, recommended clip)
  - waveform.html  (visual energy chart with highlighted clip window)

Usage:
  python analyze.py --input "path/to/video.mov" --clip-duration 25
  python analyze.py --input "path/to/video.mov" --clip-duration 25 --output ./out/
"""

import argparse
import json
import os
import struct
import subprocess
import sys
import tempfile
from pathlib import Path

import numpy as np


def extract_audio(input_path: str, sample_rate: int = 44100) -> np.ndarray:
    """Extract audio from video as mono PCM using ffmpeg."""
    with tempfile.NamedTemporaryFile(suffix=".pcm", delete=False) as tmp:
        tmp_path = tmp.name

    cmd = [
        "ffmpeg", "-y", "-i", input_path,
        "-vn",                      # no video
        "-ac", "1",                 # mono
        "-ar", str(sample_rate),    # sample rate
        "-f", "s16le",              # raw PCM signed 16-bit little-endian
        "-acodec", "pcm_s16le",
        tmp_path,
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"ffmpeg error: {result.stderr[:500]}")
        sys.exit(1)

    # Read raw PCM data
    with open(tmp_path, "rb") as f:
        raw = f.read()
    os.unlink(tmp_path)

    # Convert to numpy array (16-bit signed integers -> float)
    samples = np.frombuffer(raw, dtype=np.int16).astype(np.float32) / 32768.0
    print(f"  Extracted {len(samples) / sample_rate:.1f}s of audio ({len(samples)} samples)")
    return samples


def compute_energy(samples: np.ndarray, sample_rate: int, window_sec: float = 0.5) -> list:
    """Compute RMS energy per time window."""
    window_size = int(sample_rate * window_sec)
    num_windows = len(samples) // window_size
    energy = []

    for i in range(num_windows):
        start = i * window_size
        end = start + window_size
        chunk = samples[start:end]
        rms = float(np.sqrt(np.mean(chunk ** 2)))
        energy.append(rms)

    # Normalize to 0-1
    max_e = max(energy) if energy else 1.0
    if max_e > 0:
        energy = [e / max_e for e in energy]

    return energy


def find_peaks(energy: list, window_sec: float, min_distance_sec: float = 3.0) -> list:
    """Find energy peaks (drops) with minimum distance between them."""
    min_distance = int(min_distance_sec / window_sec)
    peaks = []

    for i in range(1, len(energy) - 1):
        if energy[i] > energy[i - 1] and energy[i] > energy[i + 1] and energy[i] > 0.6:
            # Check minimum distance from existing peaks
            too_close = False
            for p in peaks:
                if abs(i - p["index"]) < min_distance:
                    if energy[i] > p["energy"]:
                        peaks.remove(p)
                    else:
                        too_close = True
                    break
            if not too_close:
                peaks.append({
                    "index": i,
                    "time_sec": round(i * window_sec, 1),
                    "energy": round(energy[i], 3),
                })

    # Also check for sustained high energy (plateaus, not just peaks)
    # Find the window with highest average energy over 3 seconds
    avg_window = int(3.0 / window_sec)
    best_avg_start = 0
    best_avg_energy = 0
    for i in range(len(energy) - avg_window):
        avg = sum(energy[i:i + avg_window]) / avg_window
        if avg > best_avg_energy:
            best_avg_energy = avg
            best_avg_start = i

    # Add as a peak if it's not already near an existing peak
    sustained_time = round(best_avg_start * window_sec + 1.5, 1)  # center of 3s window
    is_new = all(abs(sustained_time - p["time_sec"]) > min_distance_sec for p in peaks)
    if is_new and best_avg_energy > 0.5:
        peaks.append({
            "index": best_avg_start + avg_window // 2,
            "time_sec": sustained_time,
            "energy": round(best_avg_energy, 3),
            "label": "sustained_energy",
        })

    # Sort by energy (highest first)
    peaks.sort(key=lambda p: p["energy"], reverse=True)

    # Label the top peak as "drop"
    if peaks:
        peaks[0]["label"] = "drop"
        for p in peaks[1:]:
            if "label" not in p:
                p["label"] = "build-up" if p["time_sec"] < peaks[0]["time_sec"] else "outro"

    return peaks


def recommend_clip(energy: list, peaks: list, window_sec: float, clip_duration: float, total_duration: float) -> dict:
    """Recommend the best clip window centered on the drop."""
    if not peaks:
        return {
            "start_sec": 0,
            "end_sec": min(clip_duration, total_duration),
            "drop_at_sec": clip_duration * 0.35,
            "reason": "No peaks detected, using start of recording",
        }

    drop = peaks[0]
    drop_time = drop["time_sec"]

    # Place the drop at ~35% into the clip (build-up before, vibe after)
    # For a 25s clip with drop at 35% = drop at 8.75s into clip
    drop_position_ratio = 0.35
    start = drop_time - (clip_duration * drop_position_ratio)
    end = start + clip_duration

    # Clamp to valid range
    if start < 0:
        start = 0
        end = min(clip_duration, total_duration)
    if end > total_duration:
        end = total_duration
        start = max(0, end - clip_duration)

    start = round(start, 1)
    end = round(end, 1)
    drop_in_clip = round(drop_time - start, 1)

    return {
        "start_sec": start,
        "end_sec": end,
        "duration_sec": round(end - start, 1),
        "drop_at_sec": drop_time,
        "drop_in_clip_sec": drop_in_clip,
        "drop_at_frame_24fps": int(drop_in_clip * 24),
        "drop_at_frame_30fps": int(drop_in_clip * 30),
        "start_frame_24fps": int(start * 24),
        "start_frame_30fps": int(start * 30),
        "reason": f"Highest energy peak at {drop_time}s (energy: {drop['energy']}), clip starts at {start}s with {drop_in_clip}s build-up before drop",
    }


def generate_html(energy: list, peaks: list, clip: dict, window_sec: float, source: str, total_duration: float, output_path: str):
    """Generate waveform HTML visualization."""
    # Build bar data
    bar_width = max(2, min(8, 800 // len(energy)))
    chart_width = len(energy) * (bar_width + 1)

    clip_start_idx = int(clip["start_sec"] / window_sec)
    clip_end_idx = int(clip["end_sec"] / window_sec)

    bars_html = ""
    for i, e in enumerate(energy):
        height = max(2, int(e * 200))
        in_clip = clip_start_idx <= i <= clip_end_idx
        is_drop = any(abs(i - p["index"]) < 2 for p in peaks[:3])

        if is_drop:
            # Peak/drop: coral red
            color = "#f0654a"
        elif in_clip:
            # Inside clip window: cyan green
            color = "#34d399"
        else:
            # Outside clip: energy-based gradient (low=dim, high=bright)
            # Low energy (0-0.3): dim blue-gray
            # Mid energy (0.3-0.6): muted cyan
            # High energy (0.6-1.0): bright amber/warm
            if e < 0.3:
                r, g, b = 100, 100, 130
                a = 0.25 + e * 0.5
            elif e < 0.6:
                t = (e - 0.3) / 0.3
                r = int(100 + t * 52)
                g = int(100 + t * 111)
                b = int(130 + t * 69)
                a = 0.4 + t * 0.3
            else:
                t = (e - 0.6) / 0.4
                r = int(152 + t * 93)
                g = int(211 - t * 50)
                b = int(199 - t * 150)
                a = 0.7 + t * 0.3
            color = f"rgba({r},{g},{b},{a:.2f})"

        time = round(i * window_sec, 1)
        bars_html += f'<div class="bar" style="width:{bar_width}px;height:{height}px;background:{color}" title="{time}s | energy: {e:.2f}"></div>\n'

    # Peak markers
    markers_html = ""
    for p in peaks[:5]:
        left = p["index"] * (bar_width + 1)
        color = "#f0654a" if p.get("label") == "drop" else "#f5b731"
        markers_html += f'<div class="marker" style="left:{left}px;border-color:{color}"><span>{p["time_sec"]}s<br>{p.get("label", "peak")}</span></div>\n'

    # Clip window overlay
    clip_left = clip_start_idx * (bar_width + 1)
    clip_width = (clip_end_idx - clip_start_idx) * (bar_width + 1)

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Audio Analysis - {source}</title>
<style>
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
body {{ font-family: 'SF Mono', 'Fira Code', monospace; background: #050508; color: #ededf0; padding: 32px; }}
h1 {{ font-size: 20px; font-weight: 700; color: #f0654a; margin-bottom: 4px; }}
.sub {{ font-size: 12px; color: rgba(237,237,240,0.45); margin-bottom: 32px; }}
.chart-container {{ overflow-x: auto; padding: 16px 0; }}
.chart {{ display: flex; align-items: flex-end; gap: 1px; height: 220px; position: relative; padding-bottom: 24px; min-width: {chart_width}px; }}
.bar {{ border-radius: 2px 2px 0 0; transition: opacity 0.1s; cursor: pointer; flex-shrink: 0; }}
.bar:hover {{ opacity: 0.7; }}
.clip-window {{ position: absolute; bottom: 0; height: 100%; background: rgba(52,211,153,0.06); border-left: 2px solid #34d399; border-right: 2px solid #34d399; pointer-events: none; z-index: 0; }}
.clip-label {{ position: absolute; bottom: -20px; left: 50%; transform: translateX(-50%); font-size: 10px; color: #34d399; white-space: nowrap; }}
.marker {{ position: absolute; bottom: 0; height: 100%; border-left: 2px dashed; z-index: 5; }}
.marker span {{ position: absolute; top: -4px; left: 6px; font-size: 9px; line-height: 1.3; white-space: nowrap; padding: 2px 6px; border-radius: 4px; background: rgba(5,5,8,0.9); }}
.info {{ margin-top: 32px; display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 16px; }}
.info-card {{ background: #111116; border: 1px solid rgba(255,255,255,0.06); border-radius: 10px; padding: 16px; }}
.info-card .label {{ font-size: 10px; color: rgba(237,237,240,0.45); text-transform: uppercase; letter-spacing: 0.1em; }}
.info-card .value {{ font-size: 18px; font-weight: 700; color: #f0654a; margin-top: 4px; }}
.info-card .detail {{ font-size: 11px; color: rgba(237,237,240,0.45); margin-top: 4px; }}
.legend {{ display: flex; gap: 24px; margin-top: 24px; font-size: 11px; color: rgba(237,237,240,0.45); }}
.legend-dot {{ width: 10px; height: 10px; border-radius: 2px; display: inline-block; margin-right: 6px; vertical-align: middle; }}
</style>
</head>
<body>
<h1>AUDIO ANALYSIS</h1>
<div class="sub">{source} | {total_duration:.1f}s | {len(energy)} windows @ {window_sec}s</div>

<div class="chart-container">
<div class="chart">
  <div class="clip-window" style="left:{clip_left}px;width:{clip_width}px">
    <div class="clip-label">Recommended clip: {clip['start_sec']}s - {clip['end_sec']}s ({clip['duration_sec']}s)</div>
  </div>
  {bars_html}
  {markers_html}
</div>
</div>

<div class="legend">
  <div><span class="legend-dot" style="background:#34d399"></span> Recommended clip window</div>
  <div><span class="legend-dot" style="background:#f0654a"></span> Drop / peak</div>
  <div><span class="legend-dot" style="background:rgba(152,211,199,0.5)"></span> Low-mid energy</div>
  <div><span class="legend-dot" style="background:rgba(245,183,49,0.9)"></span> High energy</div>
</div>

<div class="info">
  <div class="info-card">
    <div class="label">Best Drop</div>
    <div class="value">{clip['drop_at_sec']}s</div>
    <div class="detail">Energy: {peaks[0]['energy'] if peaks else 'N/A'}</div>
  </div>
  <div class="info-card">
    <div class="label">Clip Window</div>
    <div class="value">{clip['start_sec']}s - {clip['end_sec']}s</div>
    <div class="detail">{clip['duration_sec']}s duration</div>
  </div>
  <div class="info-card">
    <div class="label">Drop in Clip</div>
    <div class="value">{clip.get('drop_in_clip_sec', 'N/A')}s</div>
    <div class="detail">Frame {clip.get('drop_at_frame_30fps', 'N/A')} @30fps</div>
  </div>
  <div class="info-card">
    <div class="label">Remotion startFrom</div>
    <div class="value">Frame {clip.get('start_frame_24fps', 0)}</div>
    <div class="detail">@24fps source | {clip['start_sec']}s offset</div>
  </div>
</div>

<div style="margin-top:32px;font-size:11px;color:rgba(237,237,240,0.25)">
  PicYourBooth Audio Analyzer | {len(peaks)} peaks detected | Generated for video-editor agent
</div>
</body>
</html>"""

    with open(output_path, "w") as f:
        f.write(html)


def main():
    parser = argparse.ArgumentParser(description="Audio Analyzer — find best clip moments")
    parser.add_argument("--input", "-i", required=True, help="Path to video or audio file")
    parser.add_argument("--clip-duration", "-d", type=float, default=25, help="Desired clip duration in seconds (default: 25)")
    parser.add_argument("--window", "-w", type=float, default=0.5, help="Analysis window size in seconds (default: 0.5)")
    parser.add_argument("--output", "-o", default=".", help="Output directory for analysis.json and waveform.html")
    parser.add_argument("--sample-rate", type=int, default=44100, help="Audio sample rate (default: 44100)")
    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: File not found: {input_path}")
        sys.exit(1)

    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    source_name = input_path.name

    print(f"\n{'='*50}")
    print(f"Audio Analyzer")
    print(f"Input: {source_name}")
    print(f"Clip duration: {args.clip_duration}s")
    print(f"{'='*50}\n")

    # Step 1: Extract audio
    print("1. Extracting audio via ffmpeg...")
    samples = extract_audio(str(input_path), args.sample_rate)
    total_duration = len(samples) / args.sample_rate

    # Step 2: Compute energy
    print("2. Computing RMS energy...")
    energy = compute_energy(samples, args.sample_rate, args.window)
    print(f"  {len(energy)} windows analyzed")

    # Step 3: Find peaks
    print("3. Finding energy peaks...")
    peaks = find_peaks(energy, args.window)
    print(f"  {len(peaks)} peaks detected")
    for p in peaks[:3]:
        print(f"    {p['time_sec']}s — energy: {p['energy']} ({p.get('label', 'peak')})")

    # Step 4: Recommend clip
    print("4. Recommending clip window...")
    clip = recommend_clip(energy, peaks, args.window, args.clip_duration, total_duration)
    print(f"  Start: {clip['start_sec']}s | Drop: {clip['drop_at_sec']}s | End: {clip['end_sec']}s")
    print(f"  {clip['reason']}")

    # Step 5: Write JSON
    json_path = output_dir / "analysis.json"
    analysis = {
        "source": source_name,
        "duration_sec": round(total_duration, 1),
        "sample_rate": args.sample_rate,
        "window_sec": args.window,
        "energy_data": [round(e, 4) for e in energy],
        "peaks": peaks,
        "recommended_clip": clip,
    }
    with open(json_path, "w") as f:
        json.dump(analysis, f, indent=2)
    print(f"\n  JSON: {json_path}")

    # Step 6: Generate HTML
    html_path = output_dir / "waveform.html"
    generate_html(energy, peaks, clip, args.window, source_name, total_duration, str(html_path))
    print(f"  HTML: {html_path}")

    print(f"\nDone!")


if __name__ == "__main__":
    main()
