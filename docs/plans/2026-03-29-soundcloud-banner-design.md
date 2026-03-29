# SoundCloud Profile Banner — Tri-Genre Gradient Flow

**Date:** 2026-03-29
**Status:** Approved
**Asset:** DJ Gianni SoundCloud profile header banner

---

## Overview

Brand statement banner for DJ Gianni's SoundCloud profile. Abstract design matching the mixtape cover visual system. Tri-genre gradient flow across the ultra-wide format with mobile-first safe zones.

## Dimensions & Safe Zones

```
┌──────────────────────────────────────────────────────────┐
│  2480 x 520px (full banner)                              │
│                                                          │
│  ┌─ Avatar zone ─┐  ┌─── Mobile safe zone ───────┐      │
│  │  (avoid)      │  │   ~1400x520px center        │      │
│  │  0-280px left │  │   All critical content here │      │
│  └───────────────┘  └────────────────────────────-┘      │
│                                                          │
│  Left 540px          Center 1400px          Right 540px  │
│  (desktop only)      (always visible)       (desktop only)│
└──────────────────────────────────────────────────────────┘
```

- **Mobile safe zone** (center 1400x520px): Name, tagline, EQ bars — always visible
- **Avatar dead zone** (bottom-left ~280px): SoundCloud overlays round profile photo — decorative only
- **Desktop wings** (left/right 540px each): Extended gradient atmosphere, expendable on mobile

## Visual Composition

### Background

Void black (#050508) base across full width.

### Tri-Genre Gradient Flow (left → right)

| Zone | Position | Accent Color | Abstract Motif |
|------|----------|-------------|----------------|
| Left wing | 0-700px | Coral #f0654a | Concentric circular rings, tribal-inspired hexagons, ember particles rising |
| Center-left | 700-1240px | Coral → Amber blend | Motifs dissolve, particle scatter transitions |
| Center | ~1240px | Golden Amber #f5b731 | Flowing wave forms, palm frond silhouettes at ~15% opacity |
| Center-right | 1240-1780px | Amber → Purple blend | Wave forms sharpen into angular geometry |
| Right wing | 1780-2480px | Warm Purple #c084fc | Sharp diagonal slashes, trapezoid geometry, purple smoke rising |

All motifs at **15-25% opacity** — atmospheric, never competing with typography. Subtle radial gradient glow from center-bottom.

### Typography (center safe zone)

- **"DJ GIANNI"** — Bebas Neue, ~120px, #ededf0, letter-spacing 0.04em, centered
- **"PURE VIBES"** — Space Grotesk italic, ~24px, rgba(237,237,240,0.40), directly below name
- **Genre pills** — 3 pill-shaped tags below tagline:
  - "AFRO BEATS" — coral (#f0654a) background at 10%, coral border at 15%
  - "CARIBBEAN" — golden amber (#f5b731) background at 10%, amber border at 15%
  - "NL URBAN" — warm purple (#c084fc) background at 10%, purple border at 15%
  - Pill style: 11px uppercase, 600 weight, Space Grotesk, 0.08em letter-spacing, 999px border-radius

### Brand Elements

- **EQ bars** — 12 thin vertical bars (4px wide, 3px gap), spanning ~600px width behind/below text, varying heights (6-40px), coral with amber/purple accents mixed in, ~20% opacity
- **Hexagon G logo** — top-right of safe zone, 48px, coral fill, ~30% opacity

### Constraints

- No realistic faces, photographs, musical notes, neon, cool tones, busy textures
- No red (#ff494a) or pink (#e839a0)
- Warm palette only (coral, amber, warm purple)

## Mobile Rendering

On mobile, only center ~1400px visible:

```
┌────────────────────────┐
│                        │
│      DJ GIANNI         │
│      PURE VIBES        │
│  AFRO · CARIBBEAN ·   │
│       NL URBAN         │
│    [EQ bars behind]    │
│                        │
└────────────────────────┘
```

## Implementation Method

**HTML template → Playwright export at 2480x520px.** CSS handles gradients, motifs, typography. Pixel-perfect control over safe zones.

Output: `docs/images/dj-gianni/soundcloud/banner-2480x520.png`

## Knowledge Updates

1. **PROMPTS.md** — Add banner section with specs, safe zones, and Gemini prompt variant
2. **knowledge-soundcloud.md** — Add banner specs, mobile crop rules, update cadence
3. **SoundCloud strategie HTML** — Add safe zone visual reference and mobile optimization

## Design Tokens

```css
--void: #050508;
--white: #ededf0;
--muted: rgba(237,237,240,0.40);
--coral: #f0654a;
--coral-dim: rgba(240,101,74,0.10);
--amber: #f5b731;
--amber-dim: rgba(245,183,49,0.10);
--purple: #c084fc;
--purple-dim: rgba(192,132,252,0.10);
--font-display: 'Bebas Neue', Impact, sans-serif;
--font-body: 'Space Grotesk', system-ui, sans-serif;
```
