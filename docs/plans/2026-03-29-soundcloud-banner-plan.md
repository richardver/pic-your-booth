# SoundCloud Banner Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Build and export the DJ Gianni SoundCloud profile header banner (2480x520px), then update all knowledge files with banner specs and mobile optimization rules.

**Architecture:** Standalone HTML template with inline CSS (no external deps except Google Fonts). Playwright exports to PNG. Knowledge updates across 3 files.

**Tech Stack:** HTML/CSS, Google Fonts (Bebas Neue + Space Grotesk), Playwright for export, CSS gradients + pseudo-elements for abstract motifs.

**Design doc:** `docs/plans/2026-03-29-soundcloud-banner-design.md`

---

### Task 1: Create output directory

**Files:**
- Create: `images/dj-gianni/soundcloud/` (directory)

**Step 1: Create the directory**

Run: `mkdir -p /Users/richardversluis/code/pic-your-booth/images/dj-gianni/soundcloud`

**Step 2: Verify**

Run: `ls -la /Users/richardversluis/code/pic-your-booth/images/dj-gianni/soundcloud/`
Expected: Empty directory exists

---

### Task 2: Build the banner HTML template

**Files:**
- Create: `/tmp/dj-gianni-soundcloud-banner.html`

**Step 1: Write the HTML template**

Create a standalone HTML file at `/tmp/dj-gianni-soundcloud-banner.html` with these exact specs:

```html
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Space+Grotesk:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<style>
  /* --- RESET & BASE --- */
  * { margin: 0; padding: 0; box-sizing: border-box; }

  :root {
    --void: #050508;
    --white: #ededf0;
    --muted: rgba(237,237,240,0.40);
    --subtle: rgba(237,237,240,0.10);
    --coral: #f0654a;
    --coral-dim: rgba(240,101,74,0.10);
    --coral-glow: rgba(240,101,74,0.12);
    --amber: #f5b731;
    --amber-dim: rgba(245,183,49,0.10);
    --amber-glow: rgba(245,183,49,0.12);
    --purple: #c084fc;
    --purple-dim: rgba(192,132,252,0.10);
    --purple-glow: rgba(192,132,252,0.12);
    --font-display: 'Bebas Neue', Impact, sans-serif;
    --font-body: 'Space Grotesk', system-ui, sans-serif;
  }

  body {
    width: 2480px;
    height: 520px;
    overflow: hidden;
    background: var(--void);
    font-family: var(--font-body);
  }

  /* --- BANNER CONTAINER --- */
  .banner {
    position: relative;
    width: 2480px;
    height: 520px;
    overflow: hidden;
  }

  /* --- TRI-GENRE GRADIENT BACKGROUND --- */
  .gradient-layer {
    position: absolute;
    inset: 0;
    /* Three-point gradient: coral left, amber center, purple right */
    background:
      radial-gradient(ellipse 600px 400px at 350px 380px, rgba(240,101,74,0.15) 0%, transparent 70%),
      radial-gradient(ellipse 600px 400px at 1240px 400px, rgba(245,183,49,0.12) 0%, transparent 70%),
      radial-gradient(ellipse 600px 400px at 2130px 380px, rgba(192,132,252,0.15) 0%, transparent 70%),
      radial-gradient(ellipse 1200px 300px at 1240px 520px, rgba(245,183,49,0.06) 0%, transparent 60%);
  }

  /* --- ABSTRACT MOTIFS --- */

  /* Left wing: Concentric rings (Afro Beats) */
  .motif-rings {
    position: absolute;
    left: 120px;
    top: 50%;
    transform: translateY(-50%);
    width: 400px;
    height: 400px;
  }
  .motif-rings .ring {
    position: absolute;
    border-radius: 50%;
    border: 1.5px solid rgba(240,101,74,0.12);
  }
  .motif-rings .ring:nth-child(1) { inset: 0; }
  .motif-rings .ring:nth-child(2) { inset: 40px; }
  .motif-rings .ring:nth-child(3) { inset: 80px; }
  .motif-rings .ring:nth-child(4) { inset: 120px; }
  .motif-rings .ring:nth-child(5) { inset: 160px; border-color: rgba(240,101,74,0.18); }

  /* Left wing: Hexagon shapes */
  .motif-hex {
    position: absolute;
    left: 80px;
    top: 60px;
    width: 60px;
    height: 52px;
    background: rgba(240,101,74,0.06);
    clip-path: polygon(50% 0%, 100% 25%, 100% 75%, 50% 100%, 0% 75%, 0% 25%);
  }
  .motif-hex:nth-child(2) {
    left: 460px;
    top: 380px;
    width: 40px;
    height: 35px;
    background: rgba(240,101,74,0.08);
  }

  /* Center: Wave forms (Caribbean) */
  .motif-waves {
    position: absolute;
    left: 800px;
    top: 0;
    width: 880px;
    height: 520px;
    overflow: hidden;
  }
  .wave {
    position: absolute;
    width: 100%;
    height: 200px;
    border-radius: 50%;
    border: 1px solid rgba(245,183,49,0.08);
  }
  .wave:nth-child(1) { top: 320px; left: -100px; width: 1000px; height: 300px; }
  .wave:nth-child(2) { top: 360px; left: 50px; width: 800px; height: 250px; border-color: rgba(245,183,49,0.06); }
  .wave:nth-child(3) { top: 280px; left: -200px; width: 1200px; height: 350px; border-color: rgba(245,183,49,0.05); }

  /* Palm frond silhouettes */
  .motif-frond {
    position: absolute;
    width: 120px;
    height: 200px;
    border-right: 1px solid rgba(245,183,49,0.06);
    border-radius: 0 80% 0 0;
    transform: rotate(-20deg);
  }
  .motif-frond:nth-child(1) { left: 900px; top: -40px; }
  .motif-frond:nth-child(2) { left: 1500px; top: -60px; width: 100px; height: 180px; transform: rotate(-35deg); border-color: rgba(245,183,49,0.04); }

  /* Right wing: Angular geometry (NL Urban) */
  .motif-angles {
    position: absolute;
    right: 0;
    top: 0;
    width: 700px;
    height: 520px;
    overflow: hidden;
  }
  .slash {
    position: absolute;
    background: rgba(192,132,252,0.06);
    transform-origin: center;
  }
  .slash:nth-child(1) { right: 100px; top: -40px; width: 3px; height: 300px; transform: rotate(25deg); background: rgba(192,132,252,0.10); }
  .slash:nth-child(2) { right: 200px; top: 50px; width: 2px; height: 400px; transform: rotate(20deg); background: rgba(192,132,252,0.07); }
  .slash:nth-child(3) { right: 350px; top: -20px; width: 2px; height: 350px; transform: rotate(30deg); background: rgba(192,132,252,0.05); }
  .slash:nth-child(4) { right: 60px; top: 200px; width: 120px; height: 80px; transform: skewX(-15deg); background: rgba(192,132,252,0.04); }
  .slash:nth-child(5) { right: 250px; top: 350px; width: 80px; height: 60px; transform: skewX(-20deg); background: rgba(192,132,252,0.05); }

  /* Purple smoke effect */
  .motif-smoke {
    position: absolute;
    right: 150px;
    bottom: 0;
    width: 400px;
    height: 300px;
    background: radial-gradient(ellipse at 50% 100%, rgba(192,132,252,0.08) 0%, transparent 70%);
  }

  /* --- PARTICLE SCATTER --- */
  .particles {
    position: absolute;
    inset: 0;
  }
  .particle {
    position: absolute;
    width: 3px;
    height: 3px;
    border-radius: 50%;
    opacity: 0.3;
  }
  /* Coral particles - left */
  .particle:nth-child(1) { left: 200px; top: 120px; background: var(--coral); width: 2px; height: 2px; }
  .particle:nth-child(2) { left: 350px; top: 280px; background: var(--coral); opacity: 0.2; }
  .particle:nth-child(3) { left: 150px; top: 400px; background: var(--coral); width: 2px; height: 2px; opacity: 0.15; }
  .particle:nth-child(4) { left: 500px; top: 180px; background: var(--coral); width: 2px; height: 2px; opacity: 0.2; }
  /* Amber particles - center */
  .particle:nth-child(5) { left: 1000px; top: 100px; background: var(--amber); width: 2px; height: 2px; opacity: 0.2; }
  .particle:nth-child(6) { left: 1300px; top: 380px; background: var(--amber); opacity: 0.15; }
  .particle:nth-child(7) { left: 1150px; top: 450px; background: var(--amber); width: 2px; height: 2px; opacity: 0.18; }
  /* Purple particles - right */
  .particle:nth-child(8) { left: 1900px; top: 150px; background: var(--purple); opacity: 0.25; }
  .particle:nth-child(9) { left: 2100px; top: 320px; background: var(--purple); width: 2px; height: 2px; opacity: 0.2; }
  .particle:nth-child(10) { left: 2300px; top: 200px; background: var(--purple); width: 2px; height: 2px; opacity: 0.15; }
  .particle:nth-child(11) { left: 2050px; top: 440px; background: var(--purple); opacity: 0.18; }
  /* Transition particles */
  .particle:nth-child(12) { left: 700px; top: 350px; background: var(--coral); width: 2px; height: 2px; opacity: 0.12; }
  .particle:nth-child(13) { left: 1700px; top: 140px; background: var(--amber); width: 2px; height: 2px; opacity: 0.12; }

  /* --- EQ BARS --- */
  .eq-bars {
    position: absolute;
    left: 50%;
    bottom: 60px;
    transform: translateX(-50%);
    display: flex;
    gap: 3px;
    align-items: flex-end;
    opacity: 0.18;
  }
  .eq-bar {
    width: 4px;
    border-radius: 2px;
  }
  /* Coral bars */
  .eq-bar:nth-child(1)  { height: 12px; background: var(--coral); }
  .eq-bar:nth-child(2)  { height: 24px; background: var(--coral); }
  .eq-bar:nth-child(3)  { height: 18px; background: var(--coral); }
  .eq-bar:nth-child(4)  { height: 36px; background: var(--coral); }
  /* Transition to amber */
  .eq-bar:nth-child(5)  { height: 28px; background: var(--amber); }
  .eq-bar:nth-child(6)  { height: 40px; background: var(--amber); }
  .eq-bar:nth-child(7)  { height: 20px; background: var(--amber); }
  .eq-bar:nth-child(8)  { height: 32px; background: var(--amber); }
  /* Transition to purple */
  .eq-bar:nth-child(9)  { height: 22px; background: var(--purple); }
  .eq-bar:nth-child(10) { height: 38px; background: var(--purple); }
  .eq-bar:nth-child(11) { height: 16px; background: var(--purple); }
  .eq-bar:nth-child(12) { height: 30px; background: var(--purple); }

  /* --- HEXAGON G LOGO --- */
  .hex-logo {
    position: absolute;
    top: 40px;
    right: 580px; /* Inside safe zone, top-right */
    width: 48px;
    height: 42px;
    background: rgba(240,101,74,0.25);
    clip-path: polygon(50% 0%, 100% 25%, 100% 75%, 50% 100%, 0% 75%, 0% 25%);
    display: flex;
    align-items: center;
    justify-content: center;
  }
  .hex-logo span {
    font-family: var(--font-display);
    font-size: 22px;
    letter-spacing: 0.04em;
    color: var(--white);
    opacity: 0.7;
  }

  /* --- TYPOGRAPHY (CENTER SAFE ZONE) --- */
  .content {
    position: absolute;
    inset: 0;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    z-index: 10;
    padding-top: 10px; /* Slight upward shift to leave room for EQ bars below */
  }

  .name {
    font-family: var(--font-display);
    font-size: 120px;
    letter-spacing: 0.04em;
    line-height: 1;
    color: var(--white);
    text-transform: uppercase;
  }

  .tagline {
    font-family: var(--font-body);
    font-size: 24px;
    font-style: italic;
    font-weight: 300;
    color: var(--muted);
    margin-top: 8px;
    letter-spacing: 0.12em;
  }

  .genre-pills {
    display: flex;
    gap: 12px;
    margin-top: 20px;
  }

  .pill {
    padding: 5px 16px;
    border-radius: 999px;
    font-family: var(--font-body);
    font-size: 11px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.08em;
  }
  .pill--coral {
    background: var(--coral-dim);
    border: 1px solid rgba(240,101,74,0.15);
    color: var(--coral);
  }
  .pill--amber {
    background: var(--amber-dim);
    border: 1px solid rgba(245,183,49,0.15);
    color: var(--amber);
  }
  .pill--purple {
    background: var(--purple-dim);
    border: 1px solid rgba(192,132,252,0.15);
    color: var(--purple);
  }
</style>
</head>
<body>
  <div class="banner">
    <!-- Gradient background -->
    <div class="gradient-layer"></div>

    <!-- Motif: Concentric rings (left - Afro Beats) -->
    <div class="motif-rings">
      <div class="ring"></div>
      <div class="ring"></div>
      <div class="ring"></div>
      <div class="ring"></div>
      <div class="ring"></div>
    </div>

    <!-- Motif: Hexagon shapes (left) -->
    <div class="motif-hex"></div>
    <div class="motif-hex"></div>

    <!-- Motif: Wave forms (center - Caribbean) -->
    <div class="motif-waves">
      <div class="wave"></div>
      <div class="wave"></div>
      <div class="wave"></div>
    </div>

    <!-- Motif: Palm fronds -->
    <div class="motif-frond"></div>
    <div class="motif-frond"></div>

    <!-- Motif: Angular geometry (right - NL Urban) -->
    <div class="motif-angles">
      <div class="slash"></div>
      <div class="slash"></div>
      <div class="slash"></div>
      <div class="slash"></div>
      <div class="slash"></div>
    </div>

    <!-- Purple smoke (right) -->
    <div class="motif-smoke"></div>

    <!-- Particle scatter -->
    <div class="particles">
      <div class="particle"></div>
      <div class="particle"></div>
      <div class="particle"></div>
      <div class="particle"></div>
      <div class="particle"></div>
      <div class="particle"></div>
      <div class="particle"></div>
      <div class="particle"></div>
      <div class="particle"></div>
      <div class="particle"></div>
      <div class="particle"></div>
      <div class="particle"></div>
      <div class="particle"></div>
    </div>

    <!-- EQ bars -->
    <div class="eq-bars">
      <div class="eq-bar"></div>
      <div class="eq-bar"></div>
      <div class="eq-bar"></div>
      <div class="eq-bar"></div>
      <div class="eq-bar"></div>
      <div class="eq-bar"></div>
      <div class="eq-bar"></div>
      <div class="eq-bar"></div>
      <div class="eq-bar"></div>
      <div class="eq-bar"></div>
      <div class="eq-bar"></div>
      <div class="eq-bar"></div>
    </div>

    <!-- Hexagon G logo -->
    <div class="hex-logo"><span>G</span></div>

    <!-- Typography -->
    <div class="content">
      <div class="name">DJ GIANNI</div>
      <div class="tagline">Pure Vibes</div>
      <div class="genre-pills">
        <span class="pill pill--coral">Afro Beats</span>
        <span class="pill pill--amber">Caribbean</span>
        <span class="pill pill--purple">NL Urban</span>
      </div>
    </div>
  </div>
</body>
</html>
```

Key design decisions in the template:
- All motifs at 15-25% opacity via rgba — atmospheric, never fighting typography
- Gradient layer uses 4 radial-gradients positioned at left (coral), center (amber), right (purple), plus a subtle bottom glow
- Content (name, tagline, pills) is centered and z-indexed above everything
- EQ bars at bottom, below text, with tri-color progression
- Hex logo inside safe zone top-right
- All abstract motifs done in pure CSS (borders, clip-paths, gradients) — no images needed
- Left: concentric rings + hexagon shapes (Afro Beats motif from mixtape cover)
- Center: wave forms + frond silhouettes (Caribbean motif)
- Right: diagonal slashes + trapezoid shapes + smoke gradient (NL Urban motif)

**Step 2: Open in browser to visually inspect**

Run: `open /tmp/dj-gianni-soundcloud-banner.html`

Verify:
- "DJ GIANNI" text is centered, massive, readable
- Tri-genre gradient flows left (coral) → center (amber) → right (purple)
- EQ bars visible below text
- Abstract motifs are subtle atmospheric textures, not competing with text
- Genre pills are below tagline in their respective colors

---

### Task 3: Export banner with Playwright

**Files:**
- Create: `/tmp/export-banner.mjs`
- Create: `images/dj-gianni/soundcloud/banner-2480x520.png`

**Step 1: Write the Playwright export script**

```javascript
import { chromium } from 'playwright';

const browser = await chromium.launch();
const page = await browser.newPage();

await page.setViewportSize({ width: 2480, height: 520 });
await page.goto('file:///tmp/dj-gianni-soundcloud-banner.html', { waitUntil: 'networkidle' });
await page.waitForTimeout(3000); // Extra time for Google Fonts

await page.screenshot({
  path: '/Users/richardversluis/code/pic-your-booth/images/dj-gianni/soundcloud/banner-2480x520.png',
  fullPage: false,
  clip: { x: 0, y: 0, width: 2480, height: 520 }
});

console.log('Banner exported: images/dj-gianni/soundcloud/banner-2480x520.png');
await browser.close();
```

**Step 2: Run the export**

Run: `cd /tmp && node export-banner.mjs`
Expected: `Banner exported: images/dj-gianni/soundcloud/banner-2480x520.png`

**Step 3: Verify the output**

Run: `ls -la /Users/richardversluis/code/pic-your-booth/images/dj-gianni/soundcloud/banner-2480x520.png`
Expected: File exists, reasonable file size (100KB-1MB range for PNG at this resolution)

**Step 4: Visual check**

Open the exported PNG and verify it matches the HTML preview. Check:
- Full 2480x520 dimensions
- Fonts rendered correctly (Bebas Neue for name, Space Grotesk for tagline/pills)
- Colors match design tokens
- Motifs visible but subtle

---

### Task 4: Iterate on design quality

**This is the polish step.** After seeing the first export, make targeted CSS adjustments to the HTML template to improve:

- Gradient intensity (too subtle? too bright?)
- Motif density (too empty? too busy?)
- Typography sizing and vertical positioning
- EQ bar heights and spread
- Particle placement
- Overall balance between left/center/right zones

Re-export after each adjustment until the design is production-ready.

---

### Task 5: Update PROMPTS.md with banner section

**Files:**
- Modify: `images/dj-gianni/PROMPTS.md:119-126`

**Step 1: Replace the empty banner stub with full documentation**

Replace lines 119-126 (the current empty banner section) with:

```markdown
---

## SoundCloud Profiel Banner (`soundcloud/banner-2480x520.png`)

**Methode:** Playwright export vanuit HTML template
**Afmetingen:** 2480x520px
**Bron HTML:** `/tmp/dj-gianni-soundcloud-banner.html` (niet gecommit)

### Design: Tri-Genre Gradient Flow

Dark void achtergrond met drie genre-kleuren die van links naar rechts vloeien:
- Links (0-700px): Coral (#f0654a) — concentric rings, hexagons (Afro Beats motief)
- Midden (~1240px): Golden Amber (#f5b731) — golvende lijnen, palmblad silhouetten (Caribbean motief)
- Rechts (1780-2480px): Warm Purple (#c084fc) — diagonale lijnen, trapezoid geometry (NL Urban motief)

### Mobile Safe Zone

Alleen het midden ~1400px is zichtbaar op mobiel. Alle tekst en branding zit in deze zone:
- "DJ GIANNI" — Bebas Neue, 120px, centered
- "Pure Vibes" — Space Grotesk italic, 24px, 40% opacity
- Genre pills: AFRO BEATS (coral), CARIBBEAN (amber), NL URBAN (purple)
- EQ bars (12 stuks, tri-color) en hexagon G logo

### Avatar Dead Zone

SoundCloud plaatst het ronde profielfoto links-onder (~280px). Geen content in dat gebied.

### Gemini Prompt Variant

Voor AI-gegenereerde varianten (bijv. seizoensgebonden updates):

```
Design a premium ultra-wide DJ profile banner for "DJ GIANNI" - SoundCloud Header.

Landscape format, 2480x520px (ultra-wide, ~4.8:1 ratio).

COMPOSITION:
- "DJ GIANNI" massive centered title in Bebas Neue (heavy, condensed, uppercase)
- "Pure Vibes" subtitle in italic sans-serif, 40% opacity
- Three genre pills below: "AFRO BEATS" "CARIBBEAN" "NL URBAN"
- ALL text content must be in the center 1400px (mobile safe zone)
- Left 540px and right 540px are atmospheric only (cropped on mobile)
- Bottom-left 280px is empty (avatar overlay zone)

TRI-COLOR GRADIENT (left to right):
- Left zone: Coral (#f0654a) glow with concentric ring patterns, tribal hexagons
- Center zone: Golden Amber (#f5b731) glow with flowing wave forms
- Right zone: Warm Purple (#c084fc) glow with sharp angular geometry, diagonal slashes

BRAND ELEMENTS:
- 12 thin vertical EQ-bars at bottom center, colors transition coral→amber→purple
- Hexagonal "G" logo mark, top-right of center zone, subtle (30% opacity)
- Scattered particles in genre accent colors

COLORS:
- Background: #050508 (void black), Accents: #f0654a, #f5b731, #c084fc, Text: #ededf0

MOOD: Dark, minimal, premium. Three genre identities flowing into one cohesive brand. Cinematic panorama.

DO NOT: realistic faces, photographs, musical notes, neon, cool blue/cyan tones, busy textures.
```
```

**Step 2: Verify the file**

Read `images/dj-gianni/PROMPTS.md` and confirm the banner section is complete with specs, safe zones, and Gemini prompt.

**Step 3: Commit**

```bash
git add images/dj-gianni/PROMPTS.md
git commit -m "docs: add SoundCloud banner specs and Gemini prompt to PROMPTS.md"
```

---

### Task 6: Update knowledge-soundcloud.md with banner and mobile specs

**Files:**
- Modify: `.claude/agents/social-media/knowledge-soundcloud.md`

**Step 1: Add banner section at the end of the file**

Append a new section:

```markdown
---

## SoundCloud Visuele Assets

### Profiel Banner

| Asset | Afmeting | Beschrijving |
|-------|----------|-------------|
| Track cover | 3000x3000px (min 1400x1400) | Per-track/set artwork in feed en player |
| Profiel banner | 2480x520px | Header van het SoundCloud profiel |
| Profiel foto | 1000x1000px | Ronde avatar — B&W portretfoto |

### Mobile Crop Regels

SoundCloud cropped de profiel banner op mobiel tot het **midden ~1400x520px**. Alles buiten dit gebied verdwijnt.

**Safe zone layout (2480px breed):**
- Links 540px: Desktop-only — alleen atmosfeer/gradient
- Midden 1400px: **Altijd zichtbaar** — naam, tagline, genre pills, branding
- Rechts 540px: Desktop-only — alleen atmosfeer/gradient
- Links-onder 280px: Avatar overlay zone — geen content plaatsen

**Regel:** Plaats NOOIT tekst, logo's of belangrijke branding buiten de midden 1400px zone.

### Banner Update Cadence

- Update wanneer genre-aanbod verandert (nieuwe serie toevoegen)
- Seizoensgebonden variant optioneel (zomer/winter mood)
- Minimaal 1x per 6 maanden vernieuwen voor fris profiel
- Na elke update: check op mobiel EN desktop hoe het eruit ziet
```

**Step 2: Commit**

```bash
git add .claude/agents/social-media/knowledge-soundcloud.md
git commit -m "docs: add banner specs and mobile optimization to SoundCloud knowledge"
```

---

### Task 7: Update exports guide with banner asset

**Files:**
- Modify: `.claude/agents/architect/knowledge-exports-guide.md`

**Step 1: Add the banner to the DJ Gianni assets table**

Add a new row to the "DJ Gianni" table in the Current Assets section:

```markdown
| SoundCloud Banner | 2480 x 520 | `/tmp/dj-gianni-soundcloud-banner.html` | `images/dj-gianni/soundcloud/banner-2480x520.png` |
```

Also add to the Standard Sizes table:

```markdown
| SoundCloud | Profile banner | 2480 x 520 |
```

**Step 2: Commit**

```bash
git add .claude/agents/architect/knowledge-exports-guide.md
git commit -m "docs: add SoundCloud banner to exports guide"
```

---

### Task 8: Commit the banner image and final push

**Files:**
- Stage: `images/dj-gianni/soundcloud/banner-2480x520.png`

**Step 1: Stage and commit the banner**

```bash
git add images/dj-gianni/soundcloud/banner-2480x520.png
git commit -m "feat: DJ Gianni SoundCloud profile banner — tri-genre gradient flow

2480x520px header with mobile-first safe zones.
Coral (Afro) → Amber (Caribbean) → Purple (NL Urban) gradient flow.
Matching mixtape cover visual system."
```

**Step 2: Verify all changes**

Run: `git log --oneline -5`
Expected: See commits for banner image, PROMPTS.md, knowledge-soundcloud.md, exports guide.
