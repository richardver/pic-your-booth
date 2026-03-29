# Remotion Knowledge

Remotion API reference, patterns, and PYB video production standards. Use the Remotion MCP server for detailed docs.

---

## Core Concepts

| Concept | What it does |
|---|---|
| `<Composition>` | Defines a video (width, height, fps, duration, component, defaultProps) |
| `<AbsoluteFill>` | Full-size absolute-positioned container |
| `<Sequence>` | Time-shifts children — `from` delays start, `durationInFrames` limits duration |
| `<Series>` | Display contents after another (auto-sequencing) |
| `<Freeze>` | Holds a frame in place (time stops effect) |
| `<Audio>` | Plays audio independently from video (use for audio-through-end-card) |
| `useCurrentFrame()` | Returns current frame number (drives all animations) |
| `useVideoConfig()` | Returns { fps, durationInFrames, width, height } |
| `interpolate()` | Maps frame ranges to value ranges (e.g. frame 0-30 -> opacity 0-1) |
| `spring()` | Physics-based animation (0 to 1), configurable damping/stiffness |
| `<OffthreadVideo>` | Renders video without blocking main thread |
| `<Img>` | Renders image and waits for load |
| `staticFile()` | References files in public/ folder |

## Font Loading

**CRITICAL:** Remotion cannot use CSS font-family strings directly. Fonts MUST be loaded via `@remotion/google-fonts`:

```typescript
import { loadFont as loadBebasNeue } from '@remotion/google-fonts/BebasNeue';
import { loadFont as loadSpaceGrotesk } from '@remotion/google-fonts/SpaceGrotesk';

const bebasNeue = loadBebasNeue();
const spaceGrotesk = loadSpaceGrotesk();

// Use bebasNeue.fontFamily and spaceGrotesk.fontFamily in styles
```

Never use `'Bebas Neue', Impact, sans-serif` as a raw string — it won't load the font.

---

## TikTok Safe Zones

**All overlays must respect these zones. TikTok UI covers these areas:**

| Zone | Pixels | Rule |
|---|---|---|
| Top | 150px | No essential text. Status bar + Following/For You tabs. |
| Bottom | 270px | No overlays. Caption, music bar, buttons. |
| Right | 100px | No overlays. Like/comment/share sidebar. |
| **Safe** | **830x1500** | All content here. |

**Remotion padding constant:**
```typescript
export const SAFE = { top: 160, right: 110, bottom: 280, left: 40 };
const safePad = `${SAFE.top}px ${SAFE.right}px ${SAFE.bottom}px ${SAFE.left}px`;
```

Apply to every overlay `<AbsoluteFill>` that contains text or interactive elements.

---

## TikTok Specs

| Attribute | Value |
|---|---|
| Aspect ratio | 9:16 |
| Resolution | 1080x1920 |
| FPS | 30 |
| Duration | 15-60 sec |
| Codec | H.264 (MP4) |

---

## DJ Gianni Design Tokens

```typescript
import { loadFont as loadBebasNeue } from '@remotion/google-fonts/BebasNeue';
import { loadFont as loadSpaceGrotesk } from '@remotion/google-fonts/SpaceGrotesk';

const bebasNeue = loadBebasNeue();
const spaceGrotesk = loadSpaceGrotesk();

const GENRE_TOKENS = {
  afro:      { accent: '#f0654a', dim: 'rgba(240,101,74,0.10)', name: 'Afro Beats' },
  caribbean: { accent: '#f5b731', dim: 'rgba(245,183,49,0.10)', name: 'Caribbean' },
  urban:     { accent: '#c084fc', dim: 'rgba(192,132,252,0.10)', name: 'NL Urban' },
};

const TOKENS = {
  void: '#050508',
  white: '#ededf0',
  muted: 'rgba(237,237,240,0.45)',
  fontDisplay: bebasNeue.fontFamily,   // Bebas Neue — titles, hooks, DJ name
  fontBody: spaceGrotesk.fontFamily,    // Space Grotesk — body, pills, CTA, sub-text
};
```

**Rules:**
- Bebas Neue for ALL titles, hooks, and DJ name
- Space Grotesk for ALL body text, genre pills, CTA, sub-hooks
- Genre accent color from `GENRE_TOKENS[genre]`
- Never use cool tones (cyan/blue/green) for DJ Gianni

---

## Premium Video Effects Library

### Available Effects (src/components/effects/)

| Effect | File | What | When to Use |
|---|---|---|---|
| **SlamIn** | `SlamIn.tsx` | Scale 1.3x → 1x with spring bounce | Text entrances — punchy first impression |
| **BassFlash** | `BassFlash.tsx` | Full-screen accent color flash, overlay blend | Drop moment — physical impact |
| **ZoomPunch** | `ZoomPunch.tsx` | Video zoom 1.3x → 1x with spring | Drop moment — combined with shake |
| **ParticleBurst** | `ParticleBurst.tsx` | 10 accent-colored particles explode from center | Drop moment — visual explosion |
| **WipeReveal** | `WipeReveal.tsx` | Left-to-right clip-path reveal | Genre pills, staggered text entrances |
| **CoralVignette** | `CoralVignette.tsx` | Dark vignette that builds intensity over time | Build-up — creates tension |
| **FilmGrain** | `FilmGrain.tsx` | Animated SVG noise at 4% opacity, overlay blend | Always on — premium texture |
| **ScreenShake** | `ScreenShake.tsx` | Random xy offset with decay (8px intensity) | Drop moment — bass impact |
| **LightLeak** | `LightLeak.tsx` | Accent gradient sweep left-to-right, screen blend | Scene transitions — cinematic |
| **SlowZoomDrift** | `SlowZoomDrift.tsx` | Subtle zoom 1.0x→1.06x over time | Hook + build-up (kills static camera) |
| **SlowPan** | `SlowPan.tsx` | Horizontal drift + slight scale | Vibe section (visual variety) |
| **DeckHits** | `DeckHits.tsx` | 5 repeating zoom punches 1.12x + flash per hit | Deck action moments (16-20s) |
| **BeatPulse** | `BeatPulse.tsx` | Rhythmic scale pulse synced to beat | Hook + build-up + vibe (subtle energy) |
| **PreDropBuild** | `PreDropBuild.tsx` | Shake 0-4px + brightness dip + vignette | Pre-drop tension build (6-8s) |
| **PostDropDecay** | `PostDropDecay.tsx` | Aftershock shake + scale settle | Post-drop release (10-12s) |
| **GlitchText** | `GlitchText.tsx` | RGB split + offset glitch on text | Available but NOT used in current clips |

### Cinematic Color Grade

Applied on `<OffthreadVideo>` via CSS filter:
```tsx
style={{
  filter: 'contrast(1.15) saturate(1.1) brightness(0.95)',
}}
```

Plus teal shadow overlay:
```tsx
<AbsoluteFill style={{
  background: 'linear-gradient(180deg, rgba(0,20,30,0.15) 0%, transparent 40%, rgba(0,20,30,0.2) 100%)',
  mixBlendMode: 'multiply',
}} />
```

### Ken Burns Zoom (End Card)

Slow zoom on cover art for living feel:
```tsx
const kenBurns = interpolate(frame, [0, 150], [0.95, 1.05], { extrapolateRight: 'clamp' });
// Apply: transform: `scale(${enter * kenBurns})`
```

### Audio Handling

**Audio must play through the end card.** Use separate `<Audio>` component at the composition root, NOT the video's built-in audio:
```tsx
<Audio src={staticFile(videoSrc)} startFrom={Math.round(videoStartSec * 24)} />
<OffthreadVideo ... volume={0} />  // Mute the video
```

---

## Release Clip Components

| Component | Purpose | Key Props |
|---|---|---|
| `VideoBackground` | OffthreadVideo + gradient overlay + color grade | src, startFromSec |
| `TextHook` | Centered, no GlitchText, supports *word* accent syntax | text, genre |
| `GenrePills` | Centered, staggered genre pills with WipeReveal | tags, genre |
| `HookSection` | Wrapper for hook + pills, staggered internal timing, no sub-hook text | text, tags, genre |
| `DropMoment` | Single block slam (DJ name + serie together), 180px, 4s on screen, fade out | serieName, genre |
| `CTABar` | Booking CTA: BOEK DJ [NAME] + scarcity hook + coral button | genre |
| `EndCard` | Cover art (680px) with Ken Burns zoom + title + CTA | serieName, genre, coverArtSrc |

---

## Release Clip Timeline

| Sec | Frames | Scene | Camera | Effects | Overlays |
|---|---|---|---|---|---|
| 0-3 | 0-90 | Hook | SlowZoomDrift 1.0→1.04 | SlamIn 1.3x, BeatPulse, FilmGrain | Hook text (centered, *accent*) + genre pills |
| 3-6 | 90-180 | Build-up | SlowZoomDrift 1.0→1.06 | CoralVignette, BeatPulse, LightLeak, FilmGrain | Clean footage |
| 6-8 | 180-240 | Pre-drop | Static | PreDropBuild (shake 0→4px, brightness dip, vignette), FilmGrain | None |
| 8-8.3 | 240-250 | Drop | — | BassFlash 50%, ParticleBurst, double flash | — |
| 8.1-12 | 244-360 | DJ Name | — | SlamIn 1.3x, pulsing glow, fade out last 20f | DJ NAME + SERIE NAME (single block) |
| 10-12 | 300-360 | Post-drop | — | PostDropDecay (aftershock shake, scale settle), LightLeak | — |
| 10-20 | 300-600 | Vibe | SlowPan (drift right), warmer color | BeatPulse, DeckHits (16-20s, 5 hits), FilmGrain | Booking CTA (from 12s) |
| 20-25 | 600-750 | End card | — | Ken Burns 0.95→1.05, LightLeak, FilmGrain | Cover art 680px + title + CTA |

---

## Audio Analyzer Integration

The audio analyzer tool at `video/tools/audio-analyzer/analyze.py` provides:
- `recommended_clip.start_sec` → maps to `videoStartSec` prop
- `recommended_clip.drop_at_frame_30fps` → maps to `dropTimestamp` prop

```bash
python3 video/tools/audio-analyzer/analyze.py \
  --input "path/to/footage.mov" \
  --clip-duration 25 \
  --output video/dj-gianni/tiktok/release-clip/
```

---

## Rendering

| Command | Use |
|---|---|
| `npx remotion studio` | Preview in browser with live reload |
| `npx remotion still [entry] [id] [output] --frame=N` | Render single frame as PNG |
| `npx remotion render [entry] [id] [output]` | Render full video as MP4 |
| `npx remotion compositions [entry]` | List all compositions |
| `--props='{"key":"value"}'` | Pass custom inputProps |

---

## MANDATORY: Visual Review Before Delivery

**Every video MUST go through visual review before delivery.** This is not optional.

### Process

1. **Render 15-20 still frames** across the entire clip at key moments:
   - Frame 1 (first frame — is it impactful?)
   - Every scene transition (hook→build-up→pre-drop→drop→post-drop→vibe→end card)
   - Mid-scene frames (is the scene boring/static?)
   - Effects frames (are effects visible and working?)

2. **Review each frame** against this checklist:
   - Text readable? Within safe zones?
   - Effects visible? Not too strong/weak?
   - Video static? (Same angle for too long → add zoom drift or pan)
   - Color consistent? (Unwanted dark/orange tint?)
   - Transitions smooth? (No empty frames between scenes)
   - Any duplicate/ghost elements? (Multiple renders of same component)

3. **Report issues** with specific frame numbers and fixes

4. **Fix and re-render** before delivering

### Key Frames to Always Check

| Frame | What to Check |
|---|---|
| 1 | First impression — is text readable immediately? |
| Hook mid-point | Is the layout clean? No overlap? |
| Build-up mid | Is it static/boring? Need zoom drift? |
| Pre-drop peak | Is tension building visually? |
| Drop + 2 frames | Is the DJ name visible? No empty gap? |
| Drop + 30 frames | Is the name still on screen? |
| Vibe + CTA | Is the CTA readable and in safe zone? |
| End card entry | Is the transition smooth? |
| End card mid | Is cover art centered and clear? |

### Red Flags

- Same exact frame composition for >3 seconds → add movement (zoom drift, pan)
- Text appears and disappears in <1 second → extend duration
- Multiple copies of same text → check for overlapping Sequences with same component
- Dark wash over entire video → reduce gradient/vignette opacity
- Empty frames between scenes → reduce delays

---

## Scene Brief Format

Clips are briefed by other agents, not created by the video-editor:

```json
{
  "clip_type": "release",
  "genre": "afro",
  "serie": "AFRO BEATS VOL. 2",
  "hook": {
    "text": "STUUR JE PLAYLIST\nIK MAAK ER *DIT* VAN",
    "psychology": "curiosity + USP"
  },
  "brand": {
    "accent": "#f0654a",
    "genre_tags": ["Afro Beats", "Amapiano", "Afro House"],
    "cover_art": "covers/afro-mixtape-cover.png"
  },
  "footage": {
    "src": "footage/dj-gianni-set-recording.mov",
    "start_sec": 10.0,
    "drop_at_sec": 18.0
  }
}
```

**Who delivers what:**
- **Strategist:** hook text, psychology type
- **DJ-promoter:** accent color, genre tags, cover art
- **Audio analyzer:** footage path, start offset, drop timestamp
- **Video-editor:** renders everything, owns only animation timing and safe zone layout
