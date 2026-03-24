# Export Guide - Design Assets

## Method: Playwright (always)

We use Playwright for all design asset exports. Never use Chrome headless directly - Playwright gives pixel-perfect output with proper font rendering and timing.

## Setup

```bash
cd /tmp && npm install playwright
```

## Export Script Template

Save as `/tmp/export.mjs` and adapt per asset:

```javascript
import { chromium } from 'playwright';

const browser = await chromium.launch();
const page = await browser.newPage();

// Set exact dimensions
await page.setViewportSize({ width: WIDTH, height: HEIGHT });

// Load the HTML file
await page.goto('file:///path/to/template.html', { waitUntil: 'networkidle' });

// Wait for fonts and rendering
await page.waitForTimeout(2000);

// Screenshot at exact dimensions
await page.screenshot({
  path: '/path/to/output.png',
  fullPage: false,
  clip: { x: 0, y: 0, width: WIDTH, height: HEIGHT }
});

await browser.close();
```

Run with:
```bash
cd /tmp && node export.mjs
```

## Current Assets

### DJ Gianni

| Asset | Dimensions | Source HTML | Output |
|-------|-----------|------------|--------|
| SoundCloud Banner | 2480 x 520 | `/tmp/gianni-banner-export.html` | `docs/website/djs/dj-gianni/social/soundcloud-banner.png` |
| Afro Mixtape Cover | 1400 x 1400 | `/tmp/gianni-cover-export.html` | `docs/website/djs/dj-gianni/social/afro-mixtape-cover.png` |

### Standard Sizes

| Platform | Asset | Dimensions |
|----------|-------|-----------|
| SoundCloud | Profile banner | 2480 x 520 |
| SoundCloud | Track/set cover | 1400 x 1400 |
| Instagram | Post (square) | 1080 x 1080 |
| Instagram | Post (portrait) | 1080 x 1350 |
| Instagram | Stories/Reels | 1080 x 1920 |
| TikTok | Video overlay | 1080 x 1920 |
| Facebook | Post | 1200 x 630 |

## Rules

- Always use `waitUntil: 'networkidle'` for Google Fonts loading
- Always add `waitForTimeout(2000)` after page load for font rendering
- Always use `clip` with exact dimensions - never `fullPage: true`
- Export as PNG (no compression artifacts)
- Source HTML files stay in `/tmp/` (not committed)
- Exported PNGs go in the relevant `docs/` subfolder (e.g. `docs/website/djs/`)
- Each export HTML is a standalone file with inline CSS, no external deps except Google Fonts
