---
name: generate-asset
description: "Generate or enhance image assets for PYB website pages. Uses Gemini AI for styling and Python for resize/WebP conversion. Use /generate-asset to create hero backgrounds, USP images, or modal visuals."
user-invocable: true
---

# Generate Asset

Create web-ready image assets for PicYourBooth pages using AI generation or photo enhancement.

## Prerequisites

- Python 3.9+ installed
- `pip install Pillow google-generativeai python-dotenv`
- `GOOGLE_AI_API_KEY` set in `.env` (get from aistudio.google.com)

## CRITICAL: Always Use Enhance Mode

**ALWAYS use enhance mode** when our product (Party Booth or Magic Mirror) should be visible in the image. Generate mode invents fake hardware that doesn't match our real products.

- **Enhance mode** = Gemini keeps our real product, transforms the environment. **USE THIS.**
- **Generate mode** = Gemini invents everything including fake equipment. **ONLY** for concept images with zero PYB products in frame.

## Photo Reference Library

**Before generating, check `images/photos-source/INDEX.md`** for the best source photos per product/USP.

Best source photos for enhance mode (ALWAYS use venue shots for correct product scale):
- **Party Booth:** `partybooth/product/party-booth-venue-setup-stringlights.png` (PREFERRED — correct floor-standing scale)
- **Party Booth alt:** `partybooth/product/party-booth-party-atmosphere-hero.jpg` (product in context with bokeh)
- **Magic Mirror:** `magicmirror/photobooth/magic-mirror-photobooth-5.jpg` (PREFERRED — real event, correct scale)
- **Magic Mirror alt:** `magicmirror/photobooth/magic-mirror-vip-venue-wide.png` (wide venue composition)
- **VIP setup:** `magicmirror/upgrade - vip/magic-mirror-upgrade-vip-15.jpg` (red carpet + stanchions)
- **AVOID** studio/isolated shots — Gemini loses product scale without room context

## Visual Identity System

| Product | Style | Camera Vibe | Colors |
|---------|-------|-------------|--------|
| Party Booth | Neon Modern Party / Fujifilm Instax | Fujifilm X-T5, 23mm f/2 | Bright + neon pink/blue accents, gold ring light only |
| Magic Mirror XL | Black & Gold Editorial / Luxury Portrait | Canon R5, 85mm f/1.2 | Deep blacks + warm gold + cyan LED accent |
| DJs | Concert Photography / Stage Lighting | Sony A7S III, 35mm f/1.4 | Dark + colored stage lighting |

## Modes

### 1. Enhance (real photo + AI styling) — DEFAULT, use this
Takes a source photo and enhances environment/lighting while keeping the product authentic.

```bash
python3 .claude/agents/designer/scripts/asset-generator/asset-generator.py enhance \
  --source images/photos-source/partybooth/product/party-booth-product-clean-studio.png \
  --page party-booth \
  --usage usp \
  --name "direct-delen"
```

### 2. Generate (text prompt only) — ONLY for no-product concept images
Creates a scene from scratch using Gemini AI. Product hardware will be invented/inaccurate.

```bash
python .claude/agents/designer/scripts/asset-generator/asset-generator.py generate \
  --page magic-mirror \
  --usage hero \
  --scene "Optional custom scene description"
```

### 3. Resize (no AI, just process)
Resizes an existing image to all needed web dimensions.

```bash
python .claude/agents/designer/scripts/asset-generator/asset-generator.py resize \
  --input path/to/image.png \
  --page magic-mirror \
  --usage hero
```

## Steps

1. User specifies: mode + page + usage type + source photo (if enhance)
2. Script builds PYB-branded prompt from `prompts.py`
3. Gemini generates/enhances the image
4. Raw output saved to `images/pyb/`
5. Python resizes to all needed dimensions
6. WebP files saved to `docs/pyb/website/deployment/assets/images/`
7. Report file paths for use in HTML

## Pages

`homepage`, `magic-mirror`, `party-booth`, `djs`, `offerte`

## Usage Types

| Type | Sizes | For |
|---|---|---|
| `hero` | 1920x1080, 1280x720, 768x432 | Page hero backgrounds |
| `usp` | 400x400 | USP thumbnail images |
| `card` | 600x400 | Service cards on homepage |
| `modal` | 800x600 | Upgrade info modals |
| `og` | 1200x630 | Social share images (PNG + WebP) |

## Output

```
images/
├── pyb/                           ← Raw AI output + PYB brand assets
│   ├── INDEX.md                  ← Generated photos catalogue with approval status
│   ├── heroes/
│   ├── usps/
│   └── modals/
docs/pyb/website/deployment/
└── assets/images/                 ← Web-ready approved files (served by website)
    ├── magic-mirror-hero-1920x1080.webp
    ├── magic-mirror-hero-1280x720.webp
    └── magic-mirror-hero-768x432.webp
```

## Post-Generation Workflow

1. **Save** raw output to the correct subfolder in `images/pyb/`
2. **Update** `images/pyb/INDEX.md` — add a row with status `pending`
3. **Review** with Richard — show the generated image for approval
4. **Approve/Reject** — update status in INDEX.md to `approved` or `rejected`
5. **If approved** — resize to web dimensions and save to `docs/pyb/website/deployment/assets/images/`

## Brand Style

All generated images follow PYB brand: dark cinematic, warm orange lighting (#f59e42), premium event atmosphere. See `prompts.py` for full brand context, per-page scene descriptions, and photo reference library.
