# Export Guide - Design Assets

## Two Methods

### Method 1: Playwright (HTML template exports)

We use Playwright for all HTML-based design asset exports. Never use Chrome headless directly - Playwright gives pixel-perfect output with proper font rendering and timing. Best for: typography-heavy designs where pixel-perfect control matters (mixtape covers, banners, social templates).

### Method 2: Gemini Imagen (AI-generated)

Use `imagen-4.0-generate-001` via the Google GenAI SDK for AI-generated cover art. Best for: creative variations, exploring visual concepts, generating multiple options quickly. Prompt templates in each DJ's `*-mixtape-gemini-prompt.md` file.

```python
from google import genai
from google.genai import types

client = genai.Client(api_key=os.getenv('GOOGLE_AI_API_KEY'))
response = client.models.generate_images(
    model='imagen-4.0-generate-001',
    prompt=prompt,
    config=types.GenerateImagesConfig(number_of_images=1, aspect_ratio='1:1')
)
response.generated_images[0].image.save('output.png')
```

**Both methods produce valid covers.** Playwright gives exact brand-system compliance. Gemini gives creative AI interpretations. Use both and pick the best result.

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
| Afro Mixtape Cover | 1400 x 1400 | `/tmp/gianni-cover-export.html` | `docs/images/dj-gianni/mixtape/afro-mixtape-cover.png` |
| SoundCloud Banner | 2480 x 520 | `/tmp/dj-gianni-soundcloud-banner.html` | `docs/images/dj-gianni/soundcloud/banner-2480x520.png` |

### Milø

| Asset | Dimensions | Method | Source | Output |
|-------|-----------|--------|--------|--------|
| Tech House Mixtape Cover | 1400 x 1400 | Playwright | `/tmp/milo-cover-export.html?series=...&accent=34d399` | `docs/images/dj-milo/mixtape/tech-house-mixtape-cover.png` |
| House Mixtape Cover | 1400 x 1400 | Playwright | `/tmp/milo-cover-export.html?series=...&accent=38bdf8` | `docs/images/dj-milo/mixtape/house-mixtape-cover.png` |
| Deep Mixtape Cover | 1400 x 1400 | Playwright | `/tmp/milo-cover-export.html?series=...&accent=8b5cf6` | `docs/images/dj-milo/mixtape/deep-mixtape-cover.png` |
Milø's Playwright template accepts query params: `?series=SERIES+NAME&genre=GENRE&accent=hexcolor`

**Note:** Imagen 4.0 cannot reliably render the "ø" character or precise typography. Use Playwright for all mixtape cover exports. Gemini prompt template (`.claude/agents/dj-promoter/dj-milo-mixtape-gemini-prompt.md`) kept for reference but Playwright is the production method.

### Standard Sizes

| Platform | Asset | Dimensions |
|----------|-------|-----------|
| SoundCloud | Track/set cover | 1400 x 1400 |
| SoundCloud | Profile banner | 2480 x 520 |
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
- Exported PNGs go in the relevant `docs/images/` subfolder (e.g. `docs/images/dj-gianni/mixtape/`)
- Each export HTML is a standalone file with inline CSS, no external deps except Google Fonts
