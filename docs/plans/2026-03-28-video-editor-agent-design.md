# Video Editor Agent - Design Document

**Date:** 2026-03-28
**Status:** Approved
**POC Scope:** Release Clip for DJ Gianni TikTok

---

## What We're Building

A new **video-editor agent** that uses Remotion (React video framework) to produce branded TikTok/Reels clips programmatically. The agent builds reusable templates AND produces specific videos on demand from briefs.

### POC: Release Clip

One clip type — the Release Clip (15-30s TikTok video announcing a new SoundCloud mixtape). Visual design approved at `video/dj-gianni/tiktok/release-clip/design.html`.

---

## Agent Architecture

### Identity

| Attribute | Value |
|---|---|
| Name | video-editor |
| Domain | Programmatic video production with Remotion |
| Keywords | video, Remotion, TikTok, Reels, clip, render, template, 9:16 |
| Tools | Read, Grep, Glob, Bash, Write, Edit |
| Collaborates with | strategist (hooks, brand voice), social-media (platform specs, hashtags, SoundCloud strategy), dj-promoter (DJ brand identity, genre accents, voice tags, cover art) |

### Scope

| In Scope | Out of Scope |
|---|---|
| Remotion project setup and templates | Filming footage (that's Luca) |
| React component creation for clips | Social media posting |
| Rendering videos via CLI | Caption writing (social-media agent) |
| Brand overlay systems (text, EQ, pills) | Ad creative design (ad-specialist) |
| Speed ramps, transitions, animations | Music mixing/editing |

---

## Remotion Project Structure

```
video/dj-gianni/tiktok/release-clip/
  src/
    Root.tsx                  Composition registry
    ReleaseClip.tsx           Main composition (orchestrates sequences)
    components/
      TextHook.tsx            Animated text overlay (0:00-0:03)
      GenrePills.tsx          Genre pill badges (Afro Beats, Amapiano, etc.)
      EQBar.tsx               Animated EQ visualizer bars
      DropMoment.tsx          DJ name flash + coral glow burst (0:08)
      CTABar.tsx              "Link in bio" call-to-action bar (0:12+)
      EndCard.tsx             Cover art + mix title + CTA (0:22-0:25)
      HexBadge.tsx            Hexagonal G logo badge
      VideoBackground.tsx     OffthreadVideo + gradient overlay
    lib/
      tokens.ts               DJ Gianni design tokens (colors, fonts)
      types.ts                 Shared prop types
  public/
    footage/                   Behind-the-decks video files
    audio/                     Audio snippets (drops)
    covers/                    Cover art PNGs
  package.json
  remotion.config.ts
  tsconfig.json
```

---

## Release Clip Composition

### Props (inputProps)

```typescript
interface ReleaseClipProps {
  genre: 'afro' | 'caribbean' | 'urban';
  serieName: string;        // "AFRO BEATS VOL. 2"
  hookText: string;         // "Nieuwe Afro Beats mix is LIVE"
  genreTags: string[];      // ["Afro Beats", "Amapiano", "Afro House"]
  videoSrc: string;         // Path to behind-the-decks footage
  dropTimestamp: number;    // Frame where the drop happens in the footage
  coverArtSrc: string;      // Path to mixtape cover PNG
  durationSec: number;      // 15-30
}
```

### Timeline (at 30fps)

| Sequence | Frames | Component | Animation |
|---|---|---|---|
| Hook | 0-90 | TextHook + GenrePills | spring fade-in, hold, fade-out |
| Build-up | 90-240 | EQBar (pulsing) | interpolate scale with beat |
| Drop | 240-270 | DropMoment | DJ name spring scale + coral glow, speed ramp on video |
| Vibe | 270-600 | CTABar | slide-up from bottom at frame 360 |
| End Card | 600-750 | EndCard | fade from footage to void + cover art spring |

### Design Tokens

```typescript
const TOKENS = {
  afro:      { accent: '#f0654a', dim: 'rgba(240,101,74,0.10)', name: 'Afro Beats' },
  caribbean: { accent: '#f5b731', dim: 'rgba(245,183,49,0.10)', name: 'Caribbean' },
  urban:     { accent: '#c084fc', dim: 'rgba(192,132,252,0.10)', name: 'NL Urban' },
  void: '#050508',
  white: '#ededf0',
  muted: 'rgba(237,237,240,0.45)',
  fontDisplay: "'Bebas Neue', Impact, sans-serif",
  fontBody: "'Space Grotesk', system-ui, sans-serif",
};
```

---

## Agent Knowledge

### Knowledge file: `knowledge-remotion.md`

Contains:
- Remotion API reference (Composition, AbsoluteFill, Sequence, interpolate, spring, OffthreadVideo, useCurrentFrame)
- TikTok template patterns (9:16, 1080x1920, 30fps)
- Rendering commands (npx remotion render, npx remotion studio)
- DJ Gianni design tokens for video
- Component patterns for text overlays, EQ bars, speed ramps

### Skill: (future, not POC)

`/render-clip` — Takes a brief and renders a clip. Not in POC scope.

---

## Collaboration Pattern

```
User: "Maak een release clip voor Caribbean Vibes Vol. 1"
  |
  v
video-editor agent
  |-- reads dj-promoter/knowledge-dj-gianni.md (genre accents, brand)
  |-- reads social-media/knowledge-soundcloud.md (SoundCloud context)
  |-- reads strategist/knowledge-hooks.md (hook copy)
  |
  v
Assembles ReleaseClip props → renders via Remotion CLI
  |
  v
Output: MP4 in video/dj-gianni/tiktok/release-clip/out/
```

---

## Render Command

```bash
cd video/dj-gianni/tiktok/release-clip
npx remotion render ReleaseClip out/release-clip.mp4 \
  --props='{"genre":"afro","serieName":"AFRO BEATS VOL. 2","hookText":"Nieuwe Afro Beats mix is LIVE","genreTags":["Afro Beats","Amapiano","Afro House"],"videoSrc":"public/footage/set-recording.mp4","dropTimestamp":240,"coverArtSrc":"public/covers/afro-mixtape-cover.png","durationSec":25}'
```

---

## Success Criteria

1. `npx remotion studio` opens and shows the Release Clip preview
2. Changing `genre` prop switches accent color (coral/amber/purple)
3. Video footage plays as background with gradient overlay
4. All 5 sequences render in order (hook → build-up → drop → vibe → end card)
5. `npx remotion render` exports a working MP4
6. The output looks like the design storyboard
