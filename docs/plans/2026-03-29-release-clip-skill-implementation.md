# Release Clip Skill Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Build a `/release-clip` skill that interactively gathers inputs, analyzes audio, and renders a TikTok release clip for either DJ Gianni or Milo.

**Architecture:** The skill is a SKILL.md workflow that orchestrates existing tools (audio analyzer + Remotion template). Implementation requires: (1) the skill file itself, (2) Remotion template updates to support two video sources and DJ-specific effect profiles, (3) a props generator script that bridges analyzer output to Remotion input.

**Tech Stack:** SKILL.md (Claude skill), Python (audio analyzer), TypeScript/React (Remotion), ffmpeg, Node.js

**Design doc:** `docs/plans/2026-03-29-release-clip-skill-design.md`

---

### Task 1: Update ReleaseClipProps to support two video sources

**Files:**
- Modify: `video/templates/tiktok/release-clip/src/lib/types.ts`

**Step 1: Update the types**

Add second video source and DJ profile to props:

```typescript
export type Genre = 'afro' | 'caribbean' | 'urban' | 'house' | 'techno' | 'deep';

export type DJProfile = 'gianni' | 'milo';

export interface ReleaseClipProps {
  // Brand
  genre: Genre;
  djProfile: DJProfile;
  djName: string;
  serieName: string;
  genreTags: string[];

  // Hook
  hookText: string;

  // Footage — two angles
  videoSrc1: string;       // angle 1: hook, build-up, vibe
  videoSrc2: string;       // angle 2: pre-drop, drop
  videoStartSec: number;   // audio-analyzed start offset
  dropTimestamp: number;    // frame of the drop

  // Energy data from analyzer
  energyData: number[];    // RMS energy per 0.5s window

  // Assets
  coverArtSrc: string;

  // Duration
  durationSec: number;
}
```

**Step 2: Verify TypeScript compiles**

Run: `cd video/templates/tiktok/release-clip && npx tsc --noEmit`
Expected: No errors (may have warnings from unused vars temporarily)

**Step 3: Commit**

```bash
git add video/templates/tiktok/release-clip/src/lib/types.ts
git commit -m "feat: update ReleaseClipProps for two video sources + energy data"
```

---

### Task 2: Make BeatPulse read energy from props instead of hardcoded array

**Files:**
- Modify: `video/templates/tiktok/release-clip/src/components/effects/BeatPulse.tsx`

**Step 1: Update BeatPulse to accept energy data and DJ profile as props**

```typescript
import React, { createContext, useContext } from 'react';
import { AbsoluteFill, useCurrentFrame } from 'remotion';

// Default energy (silence) if none provided
const DEFAULT_ENERGY = new Array(50).fill(0.5);

interface BeatPulseContextValue {
  energyData: number[];
  scaleMult: number;     // 0.08 for gianni, 0.06 for milo
  brightnessMult: number; // 0.20 for gianni, 0.15 for milo
}

const BeatPulseContext = createContext<BeatPulseContextValue>({
  energyData: DEFAULT_ENERGY,
  scaleMult: 0.08,
  brightnessMult: 0.20,
});

interface BeatPulseProps {
  children: React.ReactNode;
  energyData?: number[];
  djProfile?: 'gianni' | 'milo';
}

export const BeatPulse: React.FC<BeatPulseProps> = ({
  children,
  energyData = DEFAULT_ENERGY,
  djProfile = 'gianni',
}) => {
  const frame = useCurrentFrame();
  const energy = energyData;

  const scaleMult = djProfile === 'milo' ? 0.06 : 0.08;
  const brightnessMult = djProfile === 'milo' ? 0.15 : 0.20;

  const windowIndex = Math.floor(frame / 15);
  const e = energy[Math.min(windowIndex, energy.length - 1)] || 0.5;
  const next = energy[Math.min(windowIndex + 1, energy.length - 1)] || 0.5;
  const pos = (frame % 15) / 15;
  const smooth = e + (next - e) * pos;

  const beatBounce = Math.sin(frame * 0.38) * 0.5 + 0.5;
  const scale = 1.0 + smooth * scaleMult * beatBounce;
  const brightness = (1.0 - brightnessMult / 2) + smooth * brightnessMult;
  const contrast = 1.0 + smooth * 0.08;

  return (
    <AbsoluteFill style={{
      transform: `scale(${scale})`,
      filter: `brightness(${brightness}) contrast(${contrast})`,
    }}>
      {children}
    </AbsoluteFill>
  );
};
```

Remove the hardcoded ENERGY array entirely.

**Step 2: Update all BeatPulse usages in ReleaseClip.tsx**

Every `<BeatPulse>` needs `energyData` and `djProfile` props passed through. This will be done in Task 4 when we rewrite ReleaseClip.

**Step 3: Commit**

```bash
git add video/templates/tiktok/release-clip/src/components/effects/BeatPulse.tsx
git commit -m "feat: BeatPulse reads energy from props, supports DJ profiles"
```

---

### Task 3: Create DJ profile configs

**Files:**
- Create: `video/templates/tiktok/release-clip/src/lib/dj-profiles.ts`

**Step 1: Create the profile config file**

This centralizes all DJ-specific settings referenced in design-v3-gianni.html and design-v3-milo.html:

```typescript
import { DJProfile, Genre } from './types';

interface EffectProfile {
  // Text entrances
  textEntrance: 'slam' | 'fade';
  textEntranceDuration: number; // frames

  // BeatPulse
  beatScaleMult: number;
  beatBrightnessMult: number;

  // Drop
  bassFlashOpacity: number;
  useParticles: boolean;
  screenShakeIntensity: number;
  screenShakeDuration: number;

  // Camera
  hookZoom: [number, number];      // [from, to]
  buildUpZoom: [number, number];
  useSlowPan: boolean;

  // Pre-drop
  preDropShake: number;           // max px
  preDropBrightnessDip: number;   // 0-1

  // Post-drop
  postDropShake: number;
  postDropSettleScale: number;
  postDropDuration: number;

  // Hits section
  hitCount: number;
  hitZoomScale: number;
  hitInterval: number;

  // Vignette & color
  vignetteMaxOpacity: number;
  warmVibeSection: boolean;

  // Light leak
  lightLeakOpacity: number;

  // Ken Burns (end card)
  kenBurnsRange: [number, number];

  // CTA
  ctaText: string;
  ctaSubtext: string;
  ctaStyle: 'bold' | 'understated';

  // Hook defaults per genre
  defaultHooks: Record<string, string>;
}

const GIANNI_PROFILE: EffectProfile = {
  textEntrance: 'slam',
  textEntranceDuration: 8,
  beatScaleMult: 0.08,
  beatBrightnessMult: 0.20,
  bassFlashOpacity: 0.50,
  useParticles: true,
  screenShakeIntensity: 18,
  screenShakeDuration: 18,
  hookZoom: [1.0, 1.04],
  buildUpZoom: [1.0, 1.06],
  useSlowPan: true,
  preDropShake: 4,
  preDropBrightnessDip: 0.30,
  postDropShake: 6,
  postDropSettleScale: 1.03,
  postDropDuration: 45,
  hitCount: 5,
  hitZoomScale: 1.12,
  hitInterval: 28,
  vignetteMaxOpacity: 0.25,
  warmVibeSection: true,
  lightLeakOpacity: 0.30,
  kenBurnsRange: [0.95, 1.05],
  ctaText: 'BOEK DJ GIANNI',
  ctaSubtext: 'Populaire data gaan snel',
  ctaStyle: 'bold',
  defaultHooks: {
    afro: 'POV: *DIT* IS HOE\nJOUW FEEST KLINKT',
    caribbean: 'POV: *DIT* IS HOE\nJOUW FEEST KLINKT',
    urban: 'POV: *DIT* IS HOE\nJOUW FEEST KLINKT',
  },
};

const MILO_PROFILE: EffectProfile = {
  textEntrance: 'fade',
  textEntranceDuration: 12,
  beatScaleMult: 0.06,
  beatBrightnessMult: 0.15,
  bassFlashOpacity: 0.30,
  useParticles: false,
  screenShakeIntensity: 8,
  screenShakeDuration: 12,
  hookZoom: [1.0, 1.03],
  buildUpZoom: [1.0, 1.04],
  useSlowPan: false,
  preDropShake: 2,
  preDropBrightnessDip: 0.15,
  postDropShake: 3,
  postDropSettleScale: 1.02,
  postDropDuration: 30,
  hitCount: 3,
  hitZoomScale: 1.06,
  hitInterval: 40,
  vignetteMaxOpacity: 0.20,
  warmVibeSection: false,
  lightLeakOpacity: 0.25,
  kenBurnsRange: [0.97, 1.03],
  ctaText: 'MILØ',
  ctaSubtext: 'bookings: link in bio',
  ctaStyle: 'understated',
  defaultHooks: {
    house: 'deep in the groove.',
    techno: 'deep in the groove.',
    deep: 'deep in the groove.',
  },
};

export const DJ_PROFILES: Record<DJProfile, EffectProfile> = {
  gianni: GIANNI_PROFILE,
  milo: MILO_PROFILE,
};

export type { EffectProfile };
```

**Step 2: Verify TypeScript compiles**

Run: `cd video/templates/tiktok/release-clip && npx tsc --noEmit`

**Step 3: Commit**

```bash
git add video/templates/tiktok/release-clip/src/lib/dj-profiles.ts
git commit -m "feat: add DJ profile configs for Gianni and Milo effect intensities"
```

---

### Task 4: Rewrite ReleaseClip.tsx to support two angles + DJ profiles

**Files:**
- Modify: `video/templates/tiktok/release-clip/src/ReleaseClip.tsx`

**Step 1: Rewrite ReleaseClip**

Key changes from current:
- Use `videoSrc1` for hook/build-up/vibe scenes, `videoSrc2` for pre-drop/drop scenes
- Use `dropTimestamp` prop instead of hardcoded `dropFrame = 240`
- Pass `energyData` and `djProfile` to BeatPulse
- Use DJ profile to conditionally render effects (no particles for Milo, FadeIn vs SlamIn, etc.)
- Fix audio startFrom to use 30fps (was 24fps)
- Pass profile values to all effect components (shake intensity, zoom ranges, etc.)

Read the full current file, then rewrite it using `DJ_PROFILES[djProfile]` for all configurable values. The structure stays the same (same scenes, same layer stack), but every hardcoded intensity value becomes a profile lookup.

**Step 2: Verify renders**

Run: `cd video/templates/tiktok/release-clip && npx remotion render src/index.ts ReleaseClip --frames=0-30`

This renders just the first second to verify no crashes.

**Step 3: Commit**

```bash
git add video/templates/tiktok/release-clip/src/ReleaseClip.tsx
git commit -m "feat: ReleaseClip supports two angles, DJ profiles, and dynamic energy"
```

---

### Task 5: Update Root.tsx with default props for both DJs

**Files:**
- Modify: `video/templates/tiktok/release-clip/src/Root.tsx`

**Step 1: Read current Root.tsx**

**Step 2: Update default props**

Add default props that work for preview. Include both `videoSrc1`/`videoSrc2` fields, `energyData` with the existing Gianni data, and `djProfile: 'gianni'` as default.

**Step 3: Commit**

```bash
git add video/templates/tiktok/release-clip/src/Root.tsx
git commit -m "feat: update Root.tsx defaults for two-angle props"
```

---

### Task 6: Create props generator script

**Files:**
- Create: `video/tools/generate-props.py`

**Step 1: Create the script**

This Python script reads `analysis.json` + user inputs and outputs a `props.json` file that Remotion can consume.

```python
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
    --output path/to/props.json
"""
```

The script:
1. Reads analysis.json for `recommended_clip.start_sec`, `drop_at_frame_30fps`, `energy_data`
2. Slices energy_data to the 25-second clip window (50 values at 0.5s each)
3. Maps DJ name + genre to proper display names (milo → "MILØ", gianni → "DJ GIANNI")
4. Maps genre to genre tags array
5. Gets default hook text from DJ profile if not provided
6. Outputs props.json matching ReleaseClipProps interface

**Step 2: Test with existing analysis**

Run: `python video/tools/generate-props.py --analysis video/output/dj-gianni/tiktok/release-clip/afro-beats-vol-2/analysis.json --dj gianni --genre afro --series "Afro Beats Vol 2" --video1 footage/test.mp4 --video2 footage/test2.mp4 --cover covers/test.png --output /tmp/test-props.json`

Verify: `cat /tmp/test-props.json` shows valid JSON matching ReleaseClipProps.

**Step 3: Commit**

```bash
git add video/tools/generate-props.py
git commit -m "feat: add props generator script (analysis.json → Remotion props)"
```

---

### Task 7: Create the /release-clip skill

**Files:**
- Create: `.claude/skills/release-clip/SKILL.md`

**Step 1: Create the skill file**

The skill is an interactive workflow. It:

1. Asks which DJ (DJ Gianni / Milo)
2. Asks for angle 1 video path
3. Asks for angle 2 video path
4. Asks for genre
5. Asks for series name
6. Asks for hook text (or uses default)
7. Creates output directory
8. Runs audio analyzer on angle 1 video
9. Saves analysis.json + waveform.html to output dir
10. Copies video files to Remotion public/footage/
11. Generates cover art path (from existing mixtape covers or asks user)
12. Runs props generator script
13. Runs Remotion render
14. Reports output location and file size

The skill should reference:
- Audio analyzer: `video/tools/audio-analyzer/analyze.py`
- Props generator: `video/tools/generate-props.py`
- Remotion template: `video/templates/tiktok/release-clip/`
- DJ profiles: design-v3-gianni.html, design-v3-milo.html
- DJ promoter agent for brand details
- Strategist agent for hook text alternatives

Include the full command sequence so the engineer can execute step by step.

**Step 2: Verify skill loads**

Test: `/release-clip` in Claude Code should load the skill.

**Step 3: Commit**

```bash
git add .claude/skills/release-clip/SKILL.md
git commit -m "feat: add /release-clip skill for interactive TikTok clip production"
```

---

### Task 8: Update CLAUDE.md and agent registry

**Files:**
- Modify: `CLAUDE.md` — add `/release-clip` to Quick Commands
- Modify: `.claude/agents/video-editor/_index.md` — reference the skill
- Modify: `.claude/agents/video-editor.md` — mention the skill in scope

**Step 1: Add to Quick Commands in CLAUDE.md**

Add: `- /release-clip - Interactive TikTok release clip production pipeline`

**Step 2: Update video-editor agent docs**

Reference the new skill and the props generator.

**Step 3: Commit**

```bash
git add CLAUDE.md .claude/agents/video-editor/_index.md .claude/agents/video-editor.md
git commit -m "docs: register /release-clip skill in CLAUDE.md and video-editor agent"
```

---

### Task 9: End-to-end test with existing Gianni footage

**Step 1: Run the full pipeline manually**

Using the existing DJ Gianni POC footage:

```bash
# 1. Analyze audio
python video/tools/audio-analyzer/analyze.py \
  --input video/output/dj-gianni/tiktok/release-clip/afro-beats-vol-2/source.mov \
  --clip-duration 25 \
  --output video/output/dj-gianni/tiktok/release-clip/afro-beats-vol-2/

# 2. Generate props
python video/tools/generate-props.py \
  --analysis video/output/dj-gianni/tiktok/release-clip/afro-beats-vol-2/analysis.json \
  --dj gianni --genre afro --series "Afro Beats Vol 2" \
  --video1 footage/gianni-angle1.mp4 --video2 footage/gianni-angle1.mp4 \
  --cover covers/afro-mixtape-cover.png \
  --output video/output/dj-gianni/tiktok/release-clip/afro-beats-vol-2/props.json

# 3. Render
cd video/templates/tiktok/release-clip
npx remotion render src/index.ts ReleaseClip \
  --props=../../../../video/output/dj-gianni/tiktok/release-clip/afro-beats-vol-2/props.json \
  ../../../../video/output/dj-gianni/tiktok/release-clip/afro-beats-vol-2/release-clip.mp4
```

**Step 2: Verify output**

Check that release-clip.mp4 exists, is ~15-20MB, plays correctly, and has proper scenes.

**Step 3: Commit**

```bash
git commit -m "test: verify release-clip pipeline end-to-end with Gianni footage"
```
