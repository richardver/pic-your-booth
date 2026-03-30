---
name: release-clip
description: Interactive TikTok release clip production — analyze audio, auto-cut two angles, render via Remotion for DJ Gianni or Milø
---

# Release Clip Production

Produce a TikTok release clip from raw DJ set recordings.

## When to use

When the user wants to create a TikTok/Reels release clip for a new mixtape or set. User provides video files from a recording session — typically angle 1 (main shot with best audio), angle 2 (alternate angle, often GoPro), and optional extra clips (close-ups, B-roll, additional angles).

## Interactive Flow

Ask these questions one at a time:

### Step 1: Which DJ?
Ask: "Which DJ is this for?"
- DJ Gianni (Luca) — coral, Afro Beats/Caribbean/NL Urban
- Milø (Milo) — cyan, Tech House/House/Deep

### Step 2: Video files
Ask: "What files do you have and where are they?"

Expect:
- **Angle 1** — main camera, best audio (1 file)
- **Angle 2** — alternate angle, may be multiple parts (1+ files)
- **Extra clips** — close-ups, B-roll, additional angles (0+ files)

Organize all files into the raw directory structure:
```
raw/angle1/    <- main camera
raw/angle2/    <- GoPro / secondary (concat if multiple parts)
raw/extra-clips/ <- all additional clips
```

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

Use **two-pass loudnorm** for clean normalization without clipping:

```bash
# Pass 1: Measure audio characteristics
ffmpeg -i "<angle1-path>" \
  -af "loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json" \
  -vn -f null /dev/null 2>&1 | tail -14

# Pass 2: Apply precise normalization using measured values
ffmpeg -y -i "<angle1-path>" \
  -af "loudnorm=I=-14:TP=-1.5:LRA=11:measured_I=<input_i>:measured_TP=<input_tp>:measured_LRA=<input_lra>:measured_thresh=<input_thresh>:offset=<target_offset>:linear=true" \
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

### 4. Sync all clips to timeline

Sync angle 2 and all extra clips to angle 1's timeline using audio envelope correlation.

**Angle 2 sync:**
Use energy envelope matching — compute RMS energy in 2s windows for both recordings, normalize, and slide the shorter against the longer to find the best correlation. GoPro audio is too different from the main camera for raw cross-correlation, but the energy envelope (loud/quiet patterns) matches well.

Save offset to `sync.json`.

**Extra clips sync:**
For each extra clip in `raw/extra-clips/`:
1. Extract audio (bandpass 40-4000Hz)
2. Compute energy envelope (0.25s windows)
3. Slide against angle 1's full envelope
4. Record the best-match position and correlation strength

Save all sync data to `extra-clips-sync.json` with fields:
- `duration`, `timeline_start`, `timeline_end`, `timeline_display`, `correlation`, `content`

### 4b. Build session timeline

Generate `timeline.html` — an interactive visual showing all clips mapped to the set timeline:
- Angle 1 as the full reference bar
- Angle 2 positioned at its sync offset
- Each extra clip as a colored block at its synced position
- Energy peaks marked as vertical lines
- Thumbnails extracted from each clip's midpoint

Also generate `peak-previews.html` and `peak-previews/` with thumbnail frames (see step 4c).

### 4c. Visual peak check (REQUIRED)

**Always do this step.** Audio energy alone doesn't guarantee a good visual moment.

1. Extract thumbnail frames at the **top 10 energy peaks** from angle 1 — 3 frames each (2s before, at peak, 2s after):
```bash
ffmpeg -y -ss <time> -i "<angle1>" -vframes 1 -q:v 3 -vf "scale=540:960" <output.jpg>
```

2. Generate `peak-previews.html` — an HTML contact sheet with all 30 frames, organized by peak, showing energy level and timestamp.

3. **Review the frames** and recommend the peak where the DJ is doing something visually interesting (hands up, looking at camera, vibing, mixing move) rather than just the loudest moment.

4. **Ask the user to confirm or pick** a different peak before proceeding to extraction.

The chosen peak replaces the audio-only recommendation for all subsequent steps.

### 5. Extract clips around drop

Extract ~35s clips (5s buffer around the 25s window). Two stages: first extract raw quality, then resize for TikTok.

**Stage 1: Extract raw clips** (preserved for future use):
```bash
mkdir -p video/output/<dj>/tiktok/release-clip/<series-slug>/raw-clips/

# Angle 1 raw (has audio) — keep original resolution
ffmpeg -y -ss <start-5s> -t 35 -i "<normalized-angle1>" \
  -c:v libx264 -preset fast -crf 18 -c:a aac -b:a 192k -movflags +faststart \
  video/output/<dj>/tiktok/release-clip/<series-slug>/raw-clips/angle1-raw.mp4

# Angle 2 raw (adjust timestamp by sync offset)
ffmpeg -y -ss <start-5s-adjusted> -t 35 -i "<angle2-path>" \
  -c:v libx264 -preset fast -crf 18 -movflags +faststart -an \
  video/output/<dj>/tiktok/release-clip/<series-slug>/raw-clips/angle2-raw.mp4
```

**Stage 2: Resize to TikTok-optimized 1080x1920** (for Remotion):
```bash
# Angle 1 — resize + crop to 9:16
ffmpeg -y -ss <start-5s> -t 35 -i "<normalized-angle1>" \
  -vf "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920" \
  -c:v libx264 -preset fast -crf 20 -pix_fmt yuv420p -movflags +faststart \
  -c:a aac -b:a 192k \
  video/templates/tiktok/release-clip/public/footage/angle1.mp4

# Angle 2 — resize + crop to 9:16
ffmpeg -y -ss <start-5s-adjusted> -t 35 -i "<angle2-path>" \
  -vf "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920" \
  -c:v libx264 -preset fast -crf 20 -pix_fmt yuv420p -movflags +faststart \
  -an \
  video/templates/tiktok/release-clip/public/footage/angle2.mp4
```

**Why two stages:**
- Raw clips preserve full resolution (4K) for future reuse (different crops, landscape edits, etc.)
- TikTok clips are 1080x1920 8-bit yuv420p for Remotion compatibility and fast rendering
- Always use `-movflags +faststart` and `-pix_fmt yuv420p` — Remotion's compositor needs standard MP4 with moov atom at start

**Important:** `videoStartSec` in props.json must be relative to the extracted clip (typically ~5.0s), NOT the absolute timestamp in the original recording.

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

### 10. Generate SoundCloud upload metadata

Create a publish-ready SoundCloud metadata file in the soundcloud output folder:

```bash
mkdir -p video/output/<dj>/soundcloud/
```

Write `video/output/<dj>/soundcloud/<series-slug>.md` with:
- Title: `Milø - <Series Name>` or `DJ Gianni - <Series Name>` (always use ø for Milø)
- Artist name with correct characters
- Genre: `House` (SoundCloud has no "Tech House" option — use tags for sub-genres)
- Tags: minimum 10 — genre + "mix" + "set" + year + artist name variants + tagline + vibe words
- Description: simple language, repeat key search terms naturally, end with bookings email + hashtags
- Reference to cover art path
- Reference to audio file: `video/output/<dj>/tiktok/release-clip/<series-slug>/full-set-audio.mp3`

Also copy the full-set audio to the soundcloud folder for easy access:
```bash
cp video/output/<dj>/tiktok/release-clip/<series-slug>/full-set-audio.mp3 \
   video/output/<dj>/soundcloud/<series-slug>.mp3
```

### 11. Report results
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
video/output/<dj>/
  tiktok/release-clip/<series-slug>/
    raw/                     <- Original source files (preserved)
      angle1/               <- Main camera (best audio)
      angle2/               <- GoPro / secondary angle
      extra-clips/          <- Additional clips from session
    raw-clips/               <- Full-res extracted clips around drop (4K)
      angle1-raw.mp4        <- Angle 1 original resolution
      angle2-raw.mp4        <- Angle 2 original resolution
    angle1-normalized.MOV    <- Full set with normalized audio
    analysis.json            <- Energy analysis (reusable)
    waveform.html            <- Interactive energy visualization (drop marked)
    sync.json                <- Angle sync offset data
    extra-clips-sync.json    <- All extra clips synced to main timeline
    timeline.html            <- Interactive session timeline (all clips mapped)
    peak-previews.html       <- Visual peak selection contact sheet
    peak-previews/           <- Thumbnail frames at top 10 energy peaks
    extra-previews/          <- Thumbnail frames from each extra clip
    props.json               <- Remotion render props
    release-clip.mp4         <- 25s TikTok clip (1080x1920)
    full-set-audio.mp3       <- Full set 320kbps (source audio)
  soundcloud/
    <series-slug>.md         <- Publish-ready upload metadata (title, tags, description)
    <series-slug>.mp3        <- Audio file ready for SoundCloud upload
```
