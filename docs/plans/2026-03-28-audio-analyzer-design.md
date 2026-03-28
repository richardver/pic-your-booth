# Audio Analyzer Tool - Design Document

**Date:** 2026-03-28
**Status:** Approved

---

## What We're Building

A reusable audio analysis tool at `video/tools/audio-analyzer/` that takes any video/audio file, extracts audio via ffmpeg, analyzes energy using numpy RMS, and outputs a JSON report + HTML waveform visualization with recommended clip windows. Used by the video-editor agent to find the best moments in DJ set recordings.

## Pipeline

```
Input: video file (MOV/MP4)
  |
  v
ffmpeg → extract PCM audio (mono, 44100Hz)
  |
  v
numpy → RMS energy per 0.5s window
  |
  v
Peak detection → find top energy moments (drops)
  |
  v
Clip window selection → best N-second window centered on the drop
  |
  v
Output:
  ├── analysis.json (timestamps, energy data, recommended windows)
  └── waveform.html (visual energy chart with highlighted clip window)
```

## Usage

```bash
.venv/bin/python video/tools/audio-analyzer/analyze.py \
  --input "path/to/video.mov" \
  --clip-duration 25 \
  --output video/dj-gianni/tiktok/release-clip/
```

## JSON Output

```json
{
  "source": "DJ Gianni - POC.mov",
  "duration_sec": 35.0,
  "sample_rate": 44100,
  "window_sec": 0.5,
  "energy_data": [0.12, 0.15, 0.18, ...],
  "peaks": [
    { "time_sec": 18.5, "energy": 0.92, "label": "drop" },
    { "time_sec": 12.0, "energy": 0.78, "label": "build-up" }
  ],
  "recommended_clip": {
    "start_sec": 8.0,
    "end_sec": 33.0,
    "drop_at_sec": 18.5,
    "drop_at_frame_30fps": 240,
    "reason": "Highest energy peak at 18.5s, clip window provides 10.5s build-up before drop"
  }
}
```

## HTML Visualization

Waveform bar chart with:
- Energy bars per 0.5s window
- Green highlighted = recommended clip window
- Red marker = detected drop
- DJ Gianni coral accent (#f0654a)
- Source file info and timestamps

## Dependencies

- ffmpeg (system, already installed)
- numpy (pip install)

## Integration with Remotion

The video-editor agent reads `recommended_clip.start_sec` and converts to frames:
```
startFrom = Math.round(start_sec * sourceFps)
```
Then passes to `<OffthreadVideo startFrom={startFrom}>`.

## Reusability

The tool is generic — works with any video/audio file, any clip duration. Not DJ-Gianni-specific. Lives at `video/tools/audio-analyzer/` for use across all video projects.
