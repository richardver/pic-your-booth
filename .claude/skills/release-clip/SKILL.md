---
name: release-clip
description: Interactive TikTok release clip production — analyze audio, auto-cut two angles, render via Remotion for DJ Gianni or Milø
---

# Release Clip Production

Produce a TikTok release clip from raw DJ set recordings.

## When to use

When the user wants to create a TikTok/Reels release clip for a new mixtape or set. User provides two video files (different camera angles of the same set).

## Interactive Flow

Ask these questions one at a time:

### Step 1: Which DJ?
Ask: "Which DJ is this for?"
- DJ Gianni (Luca) — coral, Afro Beats/Caribbean/NL Urban
- Milø (Milo) — cyan, Tech House/House/Deep

### Step 2: Video files
Ask: "Path to angle 1 video? (main shot)"
Then: "Path to angle 2 video? (alternate angle)"

Verify both files exist before proceeding.

### Step 3: Genre
Ask based on DJ:
- Gianni: "Genre? Afro Beats / Caribbean / Nederlands Urban"
- Milø: "Genre? Tech House / House / Deep"

### Step 4: Series name
Ask: "Series name? (e.g. 'Tech House Sessions Vol 1')"

### Step 5: Hook text
Ask: "Hook text? (press enter for default: '[default from profile]')"

## Pipeline Execution

After gathering all inputs, execute these steps:

### 1. Create output directory
```bash
mkdir -p video/output/<dj>/tiktok/release-clip/<series-slug>/
```
Where `<dj>` is `dj-gianni` or `dj-milo` and `<series-slug>` is the kebab-case series name.

### 2. Audio check & normalize

Always check volume levels first and normalize to broadcast standards.

```bash
# Check current levels
ffmpeg -i "<angle1-path>" -af "volumedetect" -vn -f null /dev/null 2>&1 | grep -E "mean_volume|max_volume"
```

**Target levels:** mean_volume around -14 dB, max_volume around -1.5 dB.

| Measured mean | Action |
|---|---|
| Above -10 dB | Too loud — reduce with `volume=-XdB` |
| -10 to -16 dB | Good — minor adjustment or leave as-is |
| -16 to -25 dB | Quiet — boost with `volume=+XdB` |
| Below -25 dB | Very quiet — boost + loudnorm |

```bash
# Normalize audio to broadcast standard (adjust volume=+XdB based on measurement)
ffmpeg -y -i "<angle1-path>" \
  -af "volume=<BOOST>dB,loudnorm=I=-14:TP=-1.5:LRA=11" \
  -c:v copy \
  video/output/<dj>/tiktok/release-clip/<series-slug>/angle1-normalized.<ext>
```

Use the normalized file for all subsequent steps (analysis, clip extraction, audio export).

Verify after normalization:
```bash
ffmpeg -i "<normalized-file>" -af "volumedetect" -vn -f null /dev/null 2>&1 | grep -E "mean_volume|max_volume"
```

### 3. Analyze audio
```bash
source .venv/bin/activate
python video/tools/audio-analyzer/analyze.py \
  --input "<normalized-angle1>" \
  --clip-duration 25 \
  --output video/output/<dj>/tiktok/release-clip/<series-slug>/
```

Check that `analysis.json` and `waveform.html` are created.
Report the detected drop time and recommended clip window.

### 4. Sync angles (if started at different times)

If the two video files were not started simultaneously, find the time offset:

```bash
# Extract audio fingerprints and cross-correlate
# Use the analyzer's drop timestamp as the reference point
# Search a wide window in angle 2 to find the matching moment
```

Use numpy cross-correlation on audio from both files. The offset tells you how to align angle 2's extraction timestamp with angle 1.

### 5. Extract clips around drop

Extract ~35s clips (5s buffer around the 25s window) instead of copying full files:

```bash
# Angle 1 (has audio)
ffmpeg -y -ss <start-5s> -t 35 -i "<normalized-angle1>" \
  -c:v libx264 -preset fast -crf 18 -c:a aac -b:a 192k \
  video/templates/tiktok/release-clip/public/footage/angle1.mp4

# Angle 2 (adjust timestamp by sync offset)
ffmpeg -y -ss <start-5s-adjusted> -t 35 -i "<angle2-path>" \
  -c:v libx264 -preset fast -crf 18 -an \
  video/templates/tiktok/release-clip/public/footage/angle2.mp4
```

**Important:** `videoStartSec` in props.json must be relative to the extracted clip (typically ~5.8s), NOT the absolute timestamp in the original recording.

### 6. Copy cover art
```bash
cp "<angle1-path>" video/templates/tiktok/release-clip/public/footage/angle1.mp4
cp "<angle2-path>" video/templates/tiktok/release-clip/public/footage/angle2.mp4
```

### 6. Copy cover art
Find the appropriate cover art:
- Gianni: `images/dj-gianni/mixtape/<genre>-mixtape-cover.png`
- Milø: `images/dj-milo/mixtape/<genre>-mixtape-cover.png` or `*-gemini.png`

```bash
cp "<cover-path>" video/templates/tiktok/release-clip/public/covers/cover.png
```

### 7. Generate props
```bash
python video/tools/generate-props.py \
  --analysis video/output/<dj>/tiktok/release-clip/<series-slug>/analysis.json \
  --dj <dj-key> \
  --genre <genre> \
  --series "<series-name>" \
  --video1 footage/angle1.mp4 \
  --video2 footage/angle2.mp4 \
  --cover covers/cover.png \
  --hook "<hook-text>" \
  --output video/output/<dj>/tiktok/release-clip/<series-slug>/props.json
```

### 8. Render

Route to the correct Remotion composition:

**For DJ Gianni:**
```bash
cd video/templates/tiktok/release-clip
npx remotion render src/index.ts ReleaseClip \
  --props="$(cat ../../../../video/output/<dj>/tiktok/release-clip/<series-slug>/props.json)" \
  ../../../../video/output/<dj>/tiktok/release-clip/<series-slug>/release-clip.mp4
```

**For Milø:**
```bash
cd video/templates/tiktok/release-clip
npx remotion render src/index.ts ReleaseClipMilo \
  --props="$(cat ../../../../video/output/<dj>/tiktok/release-clip/<series-slug>/props.json)" \
  ../../../../video/output/<dj>/tiktok/release-clip/<series-slug>/release-clip.mp4
```

Gianni uses `ReleaseClip` (effects-heavy, Dutch text, CTAs).
Milø uses `ReleaseClipMilo` (clean, beat-synced cuts, no mid-clip effects).

### 9. Export full set audio for SoundCloud

Always export the full normalized set as a standalone audio file (320kbps MP3).
Trim silence from start/end and add a clean fade out.

```bash
# Detect silence at start and end
ffmpeg -i "<normalized-angle1>" -af "silencedetect=n=-30dB:d=3" -f null /dev/null 2>&1 | grep -E "silence_start|silence_end"

# Export with trim + 3-second fade out (adjust -t and afade:st based on silence detection)
ffmpeg -y -i "<normalized-angle1>" \
  -ss <silence-end-at-start> \
  -t <last-silence-start> \
  -vn -c:a libmp3lame -b:a 320k \
  -af "afade=t=in:st=0:d=1,afade=t=out:st=<fade-start>:d=3" \
  video/output/<dj>/tiktok/release-clip/<series-slug>/full-set-audio.mp3
```

If no silence detected at start, omit `-ss`. Always add fade out at the end for a clean finish.

### 10. Report results
Show the user:
- Output path and all files
- File sizes
- Audio levels (before/after normalization)
- Detected drop time
- Clip window used
- Sync offset between angles (if applicable)
- Link to waveform.html for review

## Agents & Knowledge Used
- **video-editor** — Remotion template, effects library
- **dj-promoter** — DJ identity, brand, genre
- **strategist** — hook text alternatives if user wants options
- **designer** — cover art, visual tokens

## Genre Mappings

| DJ | Genre key | Display | Tags |
|---|---|---|---|
| Gianni | afro | Afro Beats | Afro Beats, Amapiano, Afro House |
| Gianni | caribbean | Caribbean | Caribbean, Reggaeton, Dancehall |
| Gianni | urban | Nederlands Urban | Nederlands, Urban, Hits |
| Milø | house | Tech House | Tech House, House, Deep |
| Milø | techno | Tech House | Tech House, House, Deep |
| Milø | deep | Deep | Deep, House, Atmospheric |

## Output Structure
```
video/output/<dj>/tiktok/release-clip/<series-slug>/
  analysis.json          <- Energy analysis (reusable)
  waveform.html          <- Interactive energy visualization
  props.json             <- Remotion render props
  release-clip.mp4       <- 25s TikTok clip
  full-set-audio.mp3     <- Full set 320kbps (SoundCloud upload)
```
