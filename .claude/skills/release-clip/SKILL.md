---
name: release-clip
description: Interactive TikTok release clip production — analyze audio, auto-cut two angles, render via Remotion for DJ Gianni or Milo
---

# Release Clip Production

Produce a TikTok release clip from raw DJ set recordings.

## When to use

When the user wants to create a TikTok/Reels release clip for a new mixtape or set. User provides two video files (different camera angles of the same set).

## Interactive Flow

Ask these questions one at a time:

### Step 1: Which DJ?
Ask: "Which DJ is this for?"
- DJ Gianni (Luca) — coral, Afro Beats/Caribbean/Nederlands
- Milo (Milo) — cyan, Tech House/House/Deep

### Step 2: Video files
Ask: "Path to angle 1 video? (main shot)"
Then: "Path to angle 2 video? (alternate angle)"

Verify both files exist before proceeding.

### Step 3: Genre
Ask based on DJ:
- Gianni: "Genre? Afro Beats / Caribbean / Nederlands Urban"
- Milo: "Genre? Tech House / House / Deep"

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

### 2. Analyze audio
```bash
source .venv/bin/activate
python video/tools/audio-analyzer/analyze.py \
  --input "<angle1-path>" \
  --clip-duration 25 \
  --output video/output/<dj>/tiktok/release-clip/<series-slug>/
```

Check that `analysis.json` and `waveform.html` are created.
Report the detected drop time and recommended clip window.

### 3. Copy footage to Remotion public
```bash
cp "<angle1-path>" video/templates/tiktok/release-clip/public/footage/angle1.mp4
cp "<angle2-path>" video/templates/tiktok/release-clip/public/footage/angle2.mp4
```

### 4. Copy cover art
Find the appropriate cover art:
- Gianni: `images/dj-gianni/mixtape/<genre>-mixtape-cover.png`
- Milo: `images/dj-milo/mixtape/<genre>-mixtape-cover.png` or `*-gemini.png`

```bash
cp "<cover-path>" video/templates/tiktok/release-clip/public/covers/cover.png
```

### 5. Generate props
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

### 6. Render
```bash
cd video/templates/tiktok/release-clip
npx remotion render src/index.ts ReleaseClip \
  --props="$(cat ../../../../video/output/<dj>/tiktok/release-clip/<series-slug>/props.json)" \
  ../../../../video/output/<dj>/tiktok/release-clip/<series-slug>/release-clip.mp4
```

### 7. Report results
Show the user:
- Output path
- File size
- Detected drop time
- Clip window used
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
| Milo | house | Tech House | Tech House, House, Deep |
| Milo | techno | Tech House | Tech House, House, Deep |
| Milo | deep | Deep | Deep, House, Atmospheric |

## Output Structure
```
video/output/<dj>/tiktok/release-clip/<series-slug>/
  analysis.json
  waveform.html
  props.json
  release-clip.mp4
```
