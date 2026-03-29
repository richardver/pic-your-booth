# Release Clip Skill Design

**Date:** 2026-03-29
**Status:** Approved

---

## What it does

An interactive skill (`/release-clip`) that takes two raw set recordings (different angles), extracts audio, analyzes energy, finds the best 25-second clip window with a drop, auto-assigns angles to scenes, and renders a TikTok release clip via Remotion. Works for both DJ Gianni and Milo.

## Interactive Flow

```
User: /release-clip

Skill: Which DJ?
  1. DJ Gianni (Luca)
  2. Milo (Milo)

User: 2

Skill: Path to angle 1 video?
User: /path/to/angle1.mp4

Skill: Path to angle 2 video?
User: /path/to/angle2.mp4

Skill: What genre?
  Tech House / House / Deep  (for Milo)
  Afro Beats / Caribbean / Nederlands Urban  (for Gianni)

User: tech house

Skill: Series name? (e.g. "Tech House Sessions Vol. 1")
User: Tech House Sessions Vol 1

Skill: Hook text? (or press enter for default)
User: [enter]
-> Uses DJ-appropriate default from design doc

Skill: [Processing...]
```

## Pipeline Steps

| Step | Action | Tool |
|---|---|---|
| 1 | Extract audio from angle 1 video | ffmpeg (via audio analyzer) |
| 2 | Analyze energy, find drop, recommend 25s window | `video/tools/audio-analyzer/analyze.py` |
| 3 | Save analysis.json + waveform.html next to output | Audio analyzer output |
| 4 | Load DJ tokens (name, genre, colors, effects) | Design docs + `tokens.ts` |
| 5 | Load hook text from design doc | `design-v3-gianni.html` or `design-v3-milo.html` |
| 6 | Auto-assign angles to scenes | Angle 1: hook/build-up/vibe, Angle 2: pre-drop/drop |
| 7 | Generate Remotion props JSON | From analysis + DJ config |
| 8 | Render via Remotion | `npx remotion render` |
| 9 | Save to output folder | `video/output/<dj>/tiktok/release-clip/<series>/` |

## Angle Assignment (auto-cut)

| Scene | Frames | Angle |
|---|---|---|
| Hook (0-3s) | 0-90 | Angle 1 |
| Build-up (3-6s) | 90-180 | Angle 1 |
| Pre-drop (6-8s) | 180-240 | Angle 2 |
| Drop (8-12s) | 240-360 | Angle 2 |
| Vibe (12-20s) | 360-600 | Angle 1 |
| End card (20-25s) | 600-750 | Cover art (no video) |

## DJ-Specific Config

| Setting | DJ Gianni | Milo |
|---|---|---|
| Effect intensity | Full (slam, particles, 50% flash) | Reduced (fade, no particles, 30% flash) |
| Hook style | Dutch, POV, accent words | English, minimal, lowercase |
| Default hooks | From design-v3-gianni.html | From design-v3-milo.html |
| CTA | "BOEK DJ GIANNI" + scarcity | "bookings: link in bio" |
| Color grade | Warm shift in vibe section | Cool/desaturated throughout |
| Genres | afro, caribbean, urban | house, techno, deep |
| Text entrance | SlamIn (spring bounce) | FadeIn (smooth opacity) |
| Drop flash | 50% coral | 30% cyan |
| Particles | ParticleBurst on drop | None |
| Camera movement | SlowZoomDrift 6% + SlowPan | SlowZoomDrift 3% only |
| Beat hits | DeckHits (5 hits, 1.12x) | GrooveHits (3 hits, 1.06x) |

## Output Structure

```
video/output/<dj>/tiktok/release-clip/<series-slug>/
  analysis.json        <- Energy analysis (reusable by other workflows)
  waveform.html        <- Interactive energy visualization
  props.json           <- Remotion render props (for re-renders)
  release-clip.mp4     <- Final rendered clip
  thumbnail.png        <- First frame export (for upload)
```

## Known Issues to Fix During Implementation

1. **BeatPulse energy array is hardcoded** in BeatPulse.tsx (lines 12-18) -- needs to read from analysis.json dynamically
2. **dropTimestamp prop passed but not used** -- ReleaseClip.tsx hardcodes dropFrame = 240, needs to use the prop from analyzer
3. **Video startFrom uses 24fps conversion** -- should detect source fps or use 30fps consistently
4. **Milo effects not implemented** -- template only has Gianni's intensity levels. Needs: FadeIn instead of SlamIn, reduced intensities, no ParticleBurst, GrooveHits instead of DeckHits, CyanVignette instead of CoralVignette

## Skills & Knowledge Used During Process

- **dj-promoter** -- DJ name, genre, brand identity, voice tags
- **designer** -- brand guide, component CSS, visual tokens
- **video-editor** -- Remotion template, effects library, design docs
- **strategist** -- hooks, content angles, CTA psychology
- **product-specialist** -- pricing for CTA if needed

## Architecture

The skill is a SKILL.md file at `.claude/skills/release-clip/SKILL.md` that:

1. Asks interactive questions to gather inputs
2. Runs the audio analyzer Python script
3. Reads the analysis output
4. Builds the Remotion props JSON based on DJ + genre + analysis
5. Handles the Remotion render command
6. Reports the output location

The skill orchestrates existing tools -- it does not duplicate the audio analyzer or Remotion template logic. It is the glue between them.
