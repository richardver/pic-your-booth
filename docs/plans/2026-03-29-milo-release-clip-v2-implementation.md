# Milø Release Clip v2 Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Build a separate Remotion composition for Milø with clean & bright aesthetic — beat-synced cuts, light teal color grade (near-original colors), big hook text, clean end card. Gianni's pipeline untouched.

**Architecture:** New `ReleaseClipMilo.tsx` composition alongside existing `ReleaseClip.tsx`. New effect components for Milø-specific visuals. Transient detection added to audio analyzer. Props generator extended with cut points.

**Tech Stack:** TypeScript/React (Remotion), Python (audio analyzer), ffmpeg

**Design doc:** `docs/plans/2026-03-29-milo-release-clip-v2-design.md`

---

### Task 1: Add transient detection to audio analyzer

**Files:**
- Modify: `video/tools/audio-analyzer/analyze.py`

**Step 1: Add transient detection function**

After the existing `find_peaks` function (~line 136), add:

```python
def detect_transients(samples: np.ndarray, sample_rate: int, threshold: float = 0.3) -> list:
    """Detect transients (kick drums, sharp attacks) using spectral flux."""
    hop = int(sample_rate * 0.01)  # 10ms hops
    window = int(sample_rate * 0.02)  # 20ms analysis window

    transients = []
    prev_energy = 0
    min_distance = int(sample_rate * 0.2)  # minimum 200ms between transients
    last_transient = -min_distance

    for i in range(0, len(samples) - window, hop):
        chunk = samples[i:i + window]
        energy = np.sqrt(np.mean(chunk ** 2))
        flux = max(0, energy - prev_energy)

        if flux > threshold and (i - last_transient) > min_distance:
            time_sec = round(i / sample_rate, 3)
            transients.append(time_sec)
            last_transient = i

        prev_energy = energy

    return transients
```

**Step 2: Call it in main() and add to JSON output**

After the peaks detection step, add:

```python
print("5. Detecting transients (kicks)...")
transients = detect_transients(samples, args.sample_rate)
print(f"  {len(transients)} transients detected")
```

Add `"transients": transients` to the `analysis` dict before writing JSON.

**Step 3: Test**

```bash
source .venv/bin/activate
python video/tools/audio-analyzer/analyze.py \
  --input video/output/dj-milo/tiktok/release-clip/tech-house-sessions-vol-1/full-set-audio.mp3 \
  --clip-duration 25 --output /tmp/test-analysis/
cat /tmp/test-analysis/analysis.json | python3 -c "import json,sys;d=json.load(sys.stdin);print(f'Transients: {len(d.get(\"transients\",[]))}')"
```

Expected: hundreds of transients detected.

**Step 4: Commit**

```bash
git add video/tools/audio-analyzer/analyze.py
git commit -m "feat: add transient detection to audio analyzer for beat-synced cuts"
```

---

### Task 2: Extend props generator with cut points

**Files:**
- Modify: `video/tools/generate-props.py`
- Modify: `video/templates/tiktok/release-clip/src/lib/types.ts`

**Step 1: Update types.ts**

Add to `ReleaseClipProps`:

```typescript
  // Beat-synced cut points (Milø v2)
  cutPoints?: number[];      // frame numbers for angle switches
```

**Step 2: Update generate-props.py**

After loading the analysis, add cut point calculation for Milø:

```python
# Calculate beat-synced cut points for Milø
cut_points = []
if args.dj == 'milo':
    transients = analysis.get('transients', [])
    clip_start = analysis['recommended_clip']['start_sec']
    clip_end = clip_start + 25

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
```

Add `"cutPoints": cut_points` to the props output.

**Step 3: Test**

```bash
python video/tools/generate-props.py \
  --analysis video/output/dj-milo/tiktok/release-clip/tech-house-sessions-vol-1/analysis.json \
  --dj milo --genre house --series "Test" \
  --video1 footage/a1.mp4 --video2 footage/a2.mp4 --cover covers/c.png \
  --output /tmp/test-props.json
cat /tmp/test-props.json | python3 -c "import json,sys;d=json.load(sys.stdin);print(f'Cut points: {d.get(\"cutPoints\",[])}')
"
```

**Step 4: Commit**

```bash
git add video/tools/generate-props.py video/templates/tiktok/release-clip/src/lib/types.ts
git commit -m "feat: add cut points to props generator for Milø beat-synced cuts"
```

---

### Task 3: CleanGrade (inline in ReleaseClipMilo.tsx)

**Note (2026-03-30):** ColorGradeFilter was replaced by an inline `CleanGrade` component in `ReleaseClipMilo.tsx`. The Clean & Bright approach uses:

```tsx
/** Clean & Bright grade: light teal tint, gentle contrast, near-original colors */
const CleanGrade: React.FC<{ children: React.ReactNode }> = ({ children }) => (
  <AbsoluteFill>
    <AbsoluteFill style={{
      filter: 'brightness(0.95) contrast(1.12) saturate(0.85)',
    }}>
      {children}
    </AbsoluteFill>
    <AbsoluteFill style={{
      background: 'rgba(52,211,153,0.06)',
      mixBlendMode: 'overlay',
      pointerEvents: 'none',
    }} />
  </AbsoluteFill>
);
```

No tunnel gradients, no vignettes, no crush-blacks overlay. `ColorGradeFilter.tsx` still exists (shared, used by Gianni genres) but is no longer used by Milø's main composition.

---

### Task 4: Create BlackoutLumaTransition component

**Files:**
- Create: `video/templates/tiktok/release-clip/src/components/effects/BlackoutLumaTransition.tsx`

**Step 1: Create the component**

```tsx
import React from 'react';
import { AbsoluteFill, useCurrentFrame, interpolate } from 'remotion';
import { TOKENS } from '../../lib/tokens';

/**
 * BlackoutLumaTransition — 2 frames black, then 3 frames luma fade.
 * Darks hold, lights transition first. Underground club visual feel.
 * Duration: 5 frames total.
 */
export const BlackoutLumaTransition: React.FC<{
  startFrame: number;
}> = ({ startFrame }) => {
  const frame = useCurrentFrame();
  const relFrame = frame - startFrame;

  if (relFrame < 0 || relFrame > 5) return null;

  // Frames 0-1: full black
  if (relFrame < 2) {
    return (
      <AbsoluteFill style={{
        backgroundColor: TOKENS.void,
        zIndex: 50,
      }} />
    );
  }

  // Frames 2-4: luma fade (darks hold, lights come through)
  const lumaOpacity = interpolate(relFrame, [2, 5], [0.9, 0], {
    extrapolateRight: 'clamp',
  });

  return (
    <AbsoluteFill style={{
      backgroundColor: TOKENS.void,
      opacity: lumaOpacity,
      mixBlendMode: 'multiply',
      zIndex: 50,
    }} />
  );
};
```

**Step 2: Commit**

```bash
git add video/templates/tiktok/release-clip/src/components/effects/BlackoutLumaTransition.tsx
git commit -m "feat: add BlackoutLumaTransition — 2-frame black + 3-frame luma fade"
```

---

### Task 5: Create LumaRevealText component

**Files:**
- Create: `video/templates/tiktok/release-clip/src/components/effects/LumaRevealText.tsx`

**Step 1: Create the component**

```tsx
import React from 'react';
import { AbsoluteFill, useCurrentFrame, interpolate } from 'remotion';
import { TOKENS, SAFE } from '../../lib/tokens';

/**
 * LumaRevealText — Big text with gradient, emerges with opacity animation.
 * Milø hook: large Bebas Neue, cyan-to-violet gradient, minimal.
 */
export const LumaRevealText: React.FC<{
  text: string;
  genreTags: string[];
}> = ({ text, genreTags }) => {
  const frame = useCurrentFrame();

  // Text fades in over 15 frames, holds, fades out last 15 frames
  const opacity = interpolate(frame, [0, 15, 70, 90], [0, 1, 1, 0], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  // Subtle scale from 1.02 to 1.0 (settling in)
  const scale = interpolate(frame, [0, 20], [1.02, 1.0], {
    extrapolateRight: 'clamp',
  });

  // Genre pills fade in with delay
  const pillsOpacity = interpolate(frame, [25, 40], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  return (
    <AbsoluteFill style={{
      padding: `${SAFE.top}px ${SAFE.right}px ${SAFE.bottom}px ${SAFE.left}px`,
      zIndex: 10,
      display: 'flex',
      flexDirection: 'column',
      justifyContent: 'center',
      alignItems: 'center',
      opacity,
    }}>
      {/* Main hook text — big, gradient */}
      <div style={{
        fontFamily: TOKENS.fontDisplay,
        fontSize: 140,
        letterSpacing: '0.04em',
        lineHeight: 1,
        textAlign: 'center',
        background: 'linear-gradient(135deg, #34d399 0%, #8b5cf6 100%)',
        WebkitBackgroundClip: 'text',
        WebkitTextFillColor: 'transparent',
        backgroundClip: 'text',
        transform: `scale(${scale})`,
        textShadow: '0 0 80px rgba(52,211,153,0.3)',
      }}>
        {text.toUpperCase()}
      </div>

      {/* Genre pills */}
      <div style={{
        display: 'flex',
        gap: 12,
        marginTop: 32,
        opacity: pillsOpacity,
      }}>
        {genreTags.map((tag, i) => (
          <div key={i} style={{
            fontFamily: TOKENS.fontBody,
            fontSize: 22,
            fontWeight: 600,
            letterSpacing: '0.08em',
            textTransform: 'uppercase',
            padding: '8px 20px',
            borderRadius: 999,
            background: 'rgba(52,211,153,0.10)',
            color: '#5ae0f0',
            border: '1px solid rgba(52,211,153,0.15)',
          }}>
            {tag}
          </div>
        ))}
      </div>
    </AbsoluteFill>
  );
};
```

**Step 2: Commit**

```bash
git add video/templates/tiktok/release-clip/src/components/effects/LumaRevealText.tsx
git commit -m "feat: add LumaRevealText — big gradient hook text for Milø"
```

---

### Task 6: Create SpeedRamp component

**Files:**
- Create: `video/templates/tiktok/release-clip/src/components/effects/SpeedRamp.tsx`

**Step 1: Create the component**

```tsx
import React from 'react';
import { AbsoluteFill, useCurrentFrame, interpolate } from 'remotion';

/**
 * SpeedRamp — Wraps video content and applies time stretch.
 * Used before end card for "moment suspended" effect.
 * Remotion doesn't have native speed control on OffthreadVideo,
 * so we simulate with a progressive brightness dim + slight scale.
 */
export const SpeedRamp: React.FC<{
  children: React.ReactNode;
  durationFrames: number;
}> = ({ children, durationFrames }) => {
  const frame = useCurrentFrame();

  // Progressive dim to black
  const brightness = interpolate(frame, [0, durationFrames], [1.0, 0.0], {
    extrapolateRight: 'clamp',
  });

  // Subtle zoom in (1.0 to 1.03)
  const scale = interpolate(frame, [0, durationFrames], [1.0, 1.03], {
    extrapolateRight: 'clamp',
  });

  return (
    <AbsoluteFill style={{
      filter: `brightness(${brightness})`,
      transform: `scale(${scale})`,
    }}>
      {children}
    </AbsoluteFill>
  );
};
```

**Step 2: Commit**

```bash
git add video/templates/tiktok/release-clip/src/components/effects/SpeedRamp.tsx
git commit -m "feat: add SpeedRamp — dim-to-black with scale before end card"
```

---

### Task 7: Create ReleaseClipMilo composition

**Files:**
- Create: `video/templates/tiktok/release-clip/src/ReleaseClipMilo.tsx`

**Step 1: Read existing components for reference**

Read: `ReleaseClip.tsx`, `VideoBackground.tsx`, `EndCard.tsx`, `FilmGrain.tsx`

**Step 2: Create the composition**

The composition structure:

```
0-150 (0-5s):     Hook — LumaRevealText over CleanGrade video (angle 1) + soft bottom fade
150-570 (5-19s):  Set — Beat-synced angle cuts, clean bright grade, hard cuts
570-630 (19-21s): Ramp — SpeedRamp (dim to black) on last angle
630-750 (21-25s): End — EndCard (reuse EndCard with no CTA text)
0-750:            FilmGrain at 4%
```

Key implementation details:

- The set section iterates over `cutPoints` to create `<Sequence>` blocks for each angle segment
- Each cut point gets a `<BlackoutLumaTransition>` overlay
- Both angles wrapped in `<CleanGrade>` for uniform clean & bright look
- VideoBackground uses `startFromSec` offset correctly (relative to extracted clip)
- Audio from angle 1, using `videoStartSec` prop
- `startFrom` in OffthreadVideo uses 30fps (fix the 24fps bug from v1)
- No BeatPulse, no BassFlash, no ScreenShake, no SlowZoomDrift — clean static footage

The EndCard is reused but with Milø-specific text:
- "MILØ" + series name + "deep in the groove"
- No "LINK IN BIO" or "Volledige set op SoundCloud"
- Use a wrapper or pass a `minimal` prop

**Step 3: Verify TypeScript compiles**

```bash
cd video/templates/tiktok/release-clip && npx tsc --noEmit
```

**Step 4: Commit**

```bash
git add video/templates/tiktok/release-clip/src/ReleaseClipMilo.tsx
git commit -m "feat: add ReleaseClipMilo composition — clean & bright aesthetic"
```

---

### Task 8: Register composition in Root.tsx

**Files:**
- Modify: `video/templates/tiktok/release-clip/src/Root.tsx`

**Step 1: Add ReleaseClipMilo composition**

Import `ReleaseClipMilo` and register it as a second `<Composition>` with id `ReleaseClipMilo`, same dimensions (1080x1920, 30fps, 750 frames), Milø-specific default props:

```typescript
defaultProps: {
  genre: 'house',
  djProfile: 'milo',
  djName: 'MILØ',
  serieName: 'TECH HOUSE SESSIONS VOL 1',
  hookText: 'deep in the groove.',
  genreTags: ['Tech House', 'House', 'Deep'],
  videoSrc1: 'footage/angle1.mp4',
  videoSrc2: 'footage/angle2.mp4',
  videoStartSec: 5.8,
  dropTimestamp: 261,
  energyData: [...], // same test data
  cutPoints: [120, 210, 330, 450],  // test cut points
  coverArtSrc: 'covers/cover.png',
  durationSec: 25,
}
```

**Step 2: Test preview**

```bash
cd video/templates/tiktok/release-clip && npx remotion preview
```

Both compositions should appear in the sidebar.

**Step 3: Commit**

```bash
git add video/templates/tiktok/release-clip/src/Root.tsx
git commit -m "feat: register ReleaseClipMilo composition in Root.tsx"
```

---

### Task 9: Update /release-clip skill routing

**Files:**
- Modify: `.claude/skills/release-clip/SKILL.md`

**Step 1: Update render step**

Change step 8 (Render) to route by DJ:

```
For Gianni: npx remotion render src/index.ts ReleaseClip --props=...
For Milø:   npx remotion render src/index.ts ReleaseClipMilo --props=...
```

**Step 2: Commit**

```bash
git add .claude/skills/release-clip/SKILL.md
git commit -m "feat: route /release-clip to correct composition per DJ"
```

---

### Task 10: Test render with existing Milø footage

**Step 1: Re-run analyzer with transient detection**

```bash
source .venv/bin/activate
python video/tools/audio-analyzer/analyze.py \
  --input ~/Downloads/milo-iphone-boosted.mov \
  --clip-duration 25 \
  --output video/output/dj-milo/tiktok/release-clip/tech-house-sessions-vol-1/
```

**Step 2: Re-generate props with cut points**

```bash
python video/tools/generate-props.py \
  --analysis video/output/dj-milo/tiktok/release-clip/tech-house-sessions-vol-1/analysis.json \
  --dj milo --genre house --series "Tech House Sessions Vol 1" \
  --video1 footage/angle1.mp4 --video2 footage/angle2.mp4 \
  --cover covers/cover.png \
  --output video/output/dj-milo/tiktok/release-clip/tech-house-sessions-vol-1/props.json
```

Fix `videoStartSec` to 5.8 (relative to extracted clip).

**Step 3: Render with Milø composition**

```bash
cd video/templates/tiktok/release-clip
npx remotion render src/index.ts ReleaseClipMilo \
  --props="$(cat /abs/path/to/props.json)" \
  /abs/path/to/release-clip-v2.mp4
```

**Step 4: Verify**

- Video plays with consistent clean & bright color grade (light teal tint)
- Hook text appears big with gradient at start
- Angle switches happen on beats with blackout transitions
- No mid-clip effects (no bounce, flash, shake)
- Speed ramp dims to black before end card
- End card shows vinyl cover
- Film grain visible throughout
- Audio is present and in sync

**Step 5: Commit**

```bash
git commit -m "test: verify Milø v2 release clip renders correctly"
```

---

### Task 11: Update design-v3-milo.html

**Files:**
- Modify: `video/templates/tiktok/release-clip/design-v3-milo.html`

Update the design reference to match v2 specs:
- Remove all mid-clip effect references
- Update timeline to hook/set/ramp/endcard structure
- Document beat-synced blackout+luma transitions
- Update hook text to big gradient version
- Note: no CTA, no booking text
- Document the color grade filter

**Step 1: Commit**

```bash
git add video/templates/tiktok/release-clip/design-v3-milo.html
git commit -m "docs: update Milø design reference to v2 specs"
```
