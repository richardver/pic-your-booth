# Design System

Tokens, colors, typography, and component specs. Full reference in `.claude/agents/designer/knowledge-design-system-full.md`.

---

## Colors

| Token | Value | Usage |
|---|---|---|
| Background | #08080b | Page background |
| Surface | #111116 | Cards, elevated elements |
| Elevated | #18181e | Modals, dropdowns |
| Text | #ededf0 | Primary text |
| Text muted | rgba(237,237,240,0.60) | Descriptions, secondary |
| Border | rgba(255,255,255,0.06) | Subtle borders |
| Gold | #f59e42 | Photobooth accent, CTAs, prices |
| Violet | #8b5cf6 | DJ Hub accent, DJ CTAs |
| Coral | #f0654a | DJ Gianni (profile only) |
| Cyan | #34d399 | Milo (profile only) |

**Removed colors:** No red (#ff494a), no pink (#e839a0).

## Typography

| Usage | Font | Weight |
|---|---|---|
| Headings, nav, prices, labels | Bebas Neue | 400 (uppercase) |
| Body, descriptions, forms | Space Grotesk | 300-700 |

Type scale: Major Third (1.25), 16px base, max 65ch line length.

## Visual Modes (Product Visual Identity System)

Each product has its own photography-driven visual DNA. See `prompts.py` for Gemini prompt implementation.

### Magic Mirror XL — Black & Gold Editorial
- **Camera vibe:** Canon R5 + 85mm f/1.2 — luxury portrait lens
- **Colors:** Deep true blacks + warm gold (#f59e42) environment + cyan/teal LED frame accent
- **Lighting:** Directional portrait lighting (Rembrandt), golden bokeh from chandeliers
- **People:** Formal/semi-formal, cocktail dresses, tailored blazers, jewelry
- **Venue:** Dark textured walls, velvet, chandeliers, candles, gold hardware
- **Mood:** "I can't believe this came from a photobooth" — editorial quality
- **Color grade:** High contrast, deep blacks, warm gold push, blue crush, editorial vignette

### Party Booth — Neon Modern / Fujifilm Instax
- **Camera vibe:** Fujifilm X-T5 + 23mm f/2, Classic Chrome film simulation
- **Colors:** Bright base + neon pink/blue LED accents. Gold ONLY on ring light (PYB anchor)
- **Lighting:** Bright daylight + neon accent strips creating colorful highlights
- **People:** Trendy casual (20-35), streetwear, sneakers, denim, gold jewelry
- **Venue:** Modern living room/loft, LED strips, string lights, neon signs
- **Mood:** "The party everyone's posting about" — Instagram-worthy house party
- **Color grade:** Soft, lifted blacks, gentle contrast, mild saturation (Instax feel)

### DJs — Concert Photography
- **Camera vibe:** Sony A7S III + 35mm f/1.4, high ISO grain
- **DJ Gianni:** Coral accent lighting, warm/Caribbean energy
- **DJ Milø:** Mint/cyan accent lighting, minimal underground feel
- **Venue:** Dark with colored stage lighting, fog/haze
- **Mood:** Immersive, energetic — "you can feel the bass"
- **Profile photos:** 8mm film aesthetic, cropped from real portraits, brand color graded

## Responsive Breakpoints

Three tiers — desktop first, then override down:

| Tier | Breakpoint | Devices | Padding |
|------|-----------|---------|---------|
| Desktop | > 768px | Laptops, desktops, large tablets | 32px side |
| Tablet | ≤ 768px | iPads, small tablets, large phones landscape | 20px side |
| Phone | ≤ 600px | All phones portrait | 20px side |

### Desktop (> 768px) — Base styles

| Element | Size | Notes |
|---------|------|-------|
| Body font | 15px, line-height 1.7 | Space Grotesk |
| Hero title | clamp(2.5rem, 6vw, 3.5rem) | Bebas Neue |
| Hero subtitle | 15px | Light weight (300) |
| Hero label | 10px uppercase | Gold, letter-spacing 0.15em |
| Hero padding | 120px top/bottom | |
| Hero min-height | 70vh | |
| Section title | 2rem | Bebas Neue |
| Section padding | 120px top/bottom | |
| USP grid | 2 columns | |
| Upgrade row name | inherit | |
| Upgrade row desc | inherit | |
| FAQ summary | inherit | |
| Nav logo | 1.75rem | With camera + headphone icons |

### Tablet (≤ 768px) — `@media (max-width: 768px)`

| Element | Size | Change |
|---------|------|--------|
| Body font | **16px**, line-height **1.75** | Bumped for readability |
| Hero title | **2rem** | Smaller, tighter letter-spacing 0.05em |
| Hero subtitle | **16px**, line-height 1.6 | Bumped from 15px |
| Hero label | **11px** | Slightly larger |
| Hero padding | **60px top, 48px bottom** | Less empty space |
| Hero min-height | **50vh** | Shorter |
| Section title | **1.6rem** | Slightly smaller |
| Section label | **12px** | |
| Section padding | **48px** | Reduced |
| USP grid | 2 columns (kept) | |
| USP card title | **1.3rem** | Bumped |
| USP card desc | **15px** | Bumped |
| Upgrade row name | **16px** | Bumped with letter-spacing |
| Upgrade row desc | **14px** | |
| Upgrade row price | **1.1rem** | |
| FAQ summary | **16px** | |
| FAQ answer | **15px** | |
| Builder features | **15px** | |
| Builder title | **1.6rem** | |
| Builder product name | **1.4rem** | |
| Builder price | **2rem** | |
| Nav: hamburger menu | visible | Links hidden, hamburger shown |

### Phone (≤ 600px) — `@media (max-width: 600px)`

| Element | Size | Change |
|---------|------|--------|
| USP grid | **1 column** | Stacked |
| USP image | **1:1 aspect ratio** | Square |

### Key Learnings (from production testing)

1. **Mobile text was too small** — 15px body on phone screens is hard to read. Always use 16px+ for mobile body text.
2. **Hero titles need aggressive scaling** — clamp() values that work on desktop are too large on mobile. Use fixed 2rem for phones.
3. **Subtitles need bumping not shrinking** — subtitle should be 16px on mobile (same as body), not smaller.
4. **Hero padding creates dead space** — 120px padding is too much on mobile. Use 60px max.
5. **Modal backdrop-filter can block touches** — after modal close, force pointer-events reset to prevent touch blocking on mobile Safari.

## Logo Specification

**Nav + Footer logo:** Camera icon (white) + "PicYour" (white) + "Booth" (gold gradient) + Headphone icon (gold)

| Element | Specs |
|---------|-------|
| Camera icon | White (#ededf0), 1em, viewBox 0 0 24 24, margin-right 7px |
| Headphone icon | Gold (#f59e42), 1em, viewBox 0 2 24 22 (cropped top), margin-left 1px |
| Container | inline-flex, align-items: center |
| "Booth" text | Gold gradient (gold → gold-light) |
| Entrance animation | Camera: shutter flash (0.8s, 0.5s delay). Headphone: bounce (0.8s, 1.0s delay). One-time only. |

## Footer Specification

```
PicYourBooth (with camera + headphone icons, same as nav)
© 2026 PicYourBooth B.V. (onderdeel van PYM) · info@picyourbooth.nl
KVK 59400080
```

- PYM links to https://www.pymapp.com (target="_blank")
- Footer gap: 6px between elements
- Footer-brand: 1.75rem, inline-flex, centered
- Footer-copy: 13px, muted text (0.35 opacity)

## Component States

default → hover (150ms) → active → focus (2px ring) → disabled

## Design Principles

- Color: 60/30/10 rule
- Spacing: 4px base unit, consistent scale
- Gold buttons: always black (#000) text
- Performance: LCP under 2.5s, WebP images, deferred scripts
- Mobile-first mindset: 70%+ traffic from Meta Ads is mobile

For full token definitions: `.claude/agents/designer/knowledge-design-system-full.md`
For HTML design system: `docs/website/design-system/pyb-design-system-web.html`
