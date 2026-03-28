# Design System Hierarchy

How PYB's design systems are layered and which inherits from which.

---

## Three-Layer Hierarchy

```
.claude/agents/designer/pyb-design-system-web.html          <- Layer 1: Parent
  |
  +-- .claude/agents/designer/pyb-design-system-photobooth.html   <- Layer 2: Photobooth pages
  +-- .claude/agents/designer/pyb-design-system-dj.html           <- Layer 2: DJ Hub page
  +-- .claude/agents/ad-specialist/pyb-design-system-meta-ads.html                  <- Layer 2: Meta Ads
      |
      +-- .claude/agents/designer/dj-gianni-brand-guide.html               <- Layer 3: DJ Gianni
      +-- .claude/agents/designer/dj-milo-brand-guide.html                     <- Layer 3: Milo
```

---

## Layer Details

### Layer 1: Web Parent (`pyb-design-system-web.html`)
- General design tokens: colors, typography, spacing, radii
- Shared components: buttons, cards, forms, navigation
- All other design systems inherit from this

### Layer 2: Page-Specific Systems
- **Photobooth** — Homepage hero, Magic Mirror premium dark mode, Party Booth bright mode, proposal form
- **DJ Hub** — Combined DJ page layout, dual-profile display
- **Meta Ads** — Ad creative templates, 8 variations for testing

### Layer 3: Individual Brand Guides
- **DJ Gianni** — Coral accent (#FF6B35), Bebas Neue + Space Grotesk, hexagon motif, split-energy system
- **DJ Milø** — Cyan accent, diamond motif, house/techno aesthetic

---

## Asset Templates (Separate from Hierarchy)

- These are export-ready HTML files, not design systems — they consume tokens from their DJ's brand guide

---

## Token JSON — PYM, Not PYB

`.claude/agents/designer/pyb-design-tokens.json` is actually a **Pic Your Moment mobile app** token file (Poppins font, `pym.color.*` namespace, Flutter references, navy/muted-red palette). It does NOT contain PYB web tokens.

**PYB web tokens** live in:
- `brand.md` — canonical colors (gold #f59e42, violet #8b5cf6, coral #f0654a, cyan #34d399, bg #08080b)
- `.claude/agents/designer/pyb-design-system-web.html` — rendered design system with all web tokens
- `prd-website.md` — design tokens section with exact hex values

---

## Rules

1. **Changes cascade down** — updating Layer 1 affects all children
2. **Individual brand guides override parent tokens** — DJ Gianni's coral overrides the default accent
3. **Each DJ gets their own brand guide** — never mix DJ identities in one file
4. **Social templates live with their DJ profile** — `docs/images/dj-gianni/social/`
5. **Do not treat `pyb-design-tokens.json` as PYB web source** — it's PYM mobile tokens, kept for reference only
