# Milø Release Clip v2 — Design

**Date:** 2026-03-29
**Status:** Approved

---

## Goal

Rebuild Milø's release clip as a separate Remotion composition with a clean & bright aesthetic: no mid-clip effects, beat-synced angle cuts, clean bright color grade (near-original colors + light teal tint), bigger brand hook text, and a clean end card. Gianni's pipeline stays completely untouched.

**Visual direction update (2026-03-30):** Milø chose Clean & Bright as the primary approach — near-original colors, gentle contrast, no heavy dark grades or tunnel gradients.

## Architecture

- `ReleaseClip.tsx` stays as-is (Gianni's template — zero changes)
- New `ReleaseClipMilo.tsx` composition — purpose-built for Milø's aesthetic
- Registered as second composition in `Root.tsx`
- `/release-clip` skill routes to correct composition based on DJ
- Shared components (EndCard, FilmGrain) reused where possible

## Timeline (25 seconds)

| Phase | Frames | Time | Content |
|---|---|---|---|
| Hook | 0-90 | 0-3s | Big text, cyan-violet gradient, luma-reveal through footage |
| Set | 90-570 | 3-19s | Pure footage, beat-synced blackout+luma cuts every 4-8s, no effects |
| Slowmo | 570-630 | 19-21s | 80% speed ramp into blackout |
| End card | 630-750 | 21-25s | Vinyl cover, series name, "deep in the groove" |

## Set Section — Beat-Synced Angle Switching

1. Transient detector finds kick drum positions in the 16s set window
2. Pick every 4th-8th kick as a cut point (~every 4-8 seconds)
3. At each cut: 2 frames black, 3 frames luma fade (darks hold, lights transition first), new angle
4. Alternate angle 1 and angle 2
5. More switches than v1 (4-5 cuts vs 1)

## Color Grade — Clean & Bright (both angles)

Applied as CSS filter to all video content — both angles get identical clean treatment:

```
brightness(0.95)    — near-original brightness
contrast(1.12)      — gentle contrast boost
saturate(0.85)      — slight desaturation, natural look
+ rgba(52,211,153,0.06) overlay — very light teal wash
```

No tunnel gradients, no vignettes, no heavy dark grades. Soft bottom fade for text readability only. Solves the color mismatch between iPhone and GoPro while keeping footage bright and open.

## Hook Text (0-3s)

- "deep in the groove." in Bebas Neue, 120-140px (was 42px)
- Cyan-to-violet gradient text (brand guide: #34d399 to #8b5cf6)
- Luma reveal: text masked by bright parts of footage underneath
- Genre pills: "TECH HOUSE · HOUSE · DEEP" in cyan dim
- Smooth fade out over last 15 frames
- Film grain active

## End Card (21-25s)

- Blackout transition from set footage
- Vinyl cover art 680px, Ken Burns 0.97x to 1.03x
- "MILØ" Bebas Neue 80px
- Series name below
- "deep in the groove" italic
- No booking CTA — pure brand
- Film grain active

## Audio Enhancements

- Transient detection (kick drums) for precise cut timing — new output from analyzer
- Subtle audio duck: -3dB for 100ms on each blackout cut
- Film grain at 4% (subtle, clean default)

## Effects Comparison: Gianni vs Milø v2

| Effect | Gianni | Milø v2 |
|---|---|---|
| BeatPulse | 8% scale, 20% brightness | OFF |
| BassFlash | 50% coral | OFF |
| ScreenShake | 18px | OFF |
| ParticleBurst | Yes | OFF |
| SlowZoomDrift | 4-6% | OFF — static locked frame |
| SlowPan | Yes | OFF |
| CoralVignette | Build-up | OFF |
| PreDropBuild | Shake + darken | OFF |
| DeckHits | 5 zoom kicks | OFF |
| LightLeak | 30% at transitions | OFF |
| FilmGrain | 5% | 4% |
| Text entrance | SlamIn (spring) | LumaReveal (mask) |
| Angle switches | 1 (at scene boundary) | 4-5 (beat-synced) |
| Transitions | Hard cut | Hard cut, clean & precise |
| Color grade | Warm shift in vibe | Clean & Bright — light teal tint, near-original colors |
| CTA | "BOEK DJ GIANNI" + scarcity | None |
| Speed ramp | None | 80% before end card |
| Audio duck | None | -3dB on cuts |

## New Components

| Component | File | Purpose |
|---|---|---|
| ReleaseClipMilo | `src/ReleaseClipMilo.tsx` | Main composition |
| BlackoutLumaTransition | `src/components/effects/BlackoutLumaTransition.tsx` | 2-frame black + 3-frame luma fade |
| CleanGrade | Inline in `ReleaseClipMilo.tsx` | Clean & Bright grade — light teal tint, gentle contrast |
| LumaRevealText | `src/components/effects/LumaRevealText.tsx` | Text emerges through bright parts of video |
| SpeedRamp | `src/components/effects/SpeedRamp.tsx` | 80% slowdown before end card |

## Pre-processing (Python)

| Tool | Addition |
|---|---|
| `analyze.py` | Add transient detection: output `transients` array with kick positions |
| `generate-props.py` | Add `cutPoints: number[]` to props, calculated from transients |

## Props Interface Addition

```typescript
// Added to ReleaseClipProps or new MiloClipProps
cutPoints: number[];       // frame numbers for angle switches
colorGrade: 'gianni' | 'milo';  // which grade to apply
```

## File Impact

| File | Change |
|---|---|
| `ReleaseClip.tsx` | NO CHANGE |
| All Gianni effects | NO CHANGE |
| `Root.tsx` | Add ReleaseClipMilo composition |
| `types.ts` | Add cutPoints, colorGrade |
| `dj-profiles.ts` | Update Milø values |
| New: `ReleaseClipMilo.tsx` | ~150 lines |
| New: 4 effect components | ~250 lines total |
| `analyze.py` | Add transient detection (~30 lines) |
| `generate-props.py` | Add cut points logic (~20 lines) |
| `SKILL.md` | Route to composition per DJ |
| `design-v3-milo.html` | Update to match v2 specs |

## Output (unchanged structure)

```
video/output/dj-milo/tiktok/release-clip/<series>/
  analysis.json         <- now includes transients
  waveform.html
  props.json            <- now includes cutPoints
  release-clip.mp4
  full-set-audio.mp3
  metadata-soundcloud.md
```
