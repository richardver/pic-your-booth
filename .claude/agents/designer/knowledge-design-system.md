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

## Visual Modes

### Magic Mirror XL (Premium)
- Dark backgrounds, warm gold/amber accents, high contrast
- Cinematic event photography, bokeh effects
- Glass morphism, premium card components

### Party Booth (Accessible)
- Bright backgrounds, vibrant accents, fun energy
- Casual celebrations, friends laughing, colorful
- Clean cards, bright CTAs

### DJ + Photobooth Combo
- High-energy dark with neon accents
- Dance floors, DJ action shots, crowd energy
- Dynamic layouts, bold typography

## Component States

default → hover (150ms) → active → focus (2px ring) → disabled

## Design Principles

- Color: 60/30/10 rule
- Spacing: 4px base unit, consistent scale
- Gold buttons: always black (#000) text
- Performance: LCP under 2.5s, WebP images, deferred scripts

For full token definitions: `.claude/agents/designer/knowledge-design-system-full.md`
For HTML design system: `docs/templates/design-system/pyb-design-system-web.html`
