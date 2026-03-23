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

## Modes

### 1. Enhance (real photo + AI styling)
Takes a source photo and enhances environment/lighting while keeping the product authentic.

```bash
python .claude/agents/designer/scripts/asset-generator/asset-generator.py enhance \
  --source docs/assets/source-photos/magicmirror/photo.jpg \
  --page magic-mirror \
  --usage hero
```

### 2. Generate (text prompt only)
Creates a scene from scratch using Gemini AI.

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
4. Raw output saved to `docs/assets/generated/`
5. Python resizes to all needed dimensions
6. WebP files saved to `docs/assets/web/`
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
docs/assets/
├── generated/                    ← Raw AI output
│   └── magic-mirror-hero-generated.png
└── web/                          ← Web-ready files
    ├── magic-mirror-hero-1920x1080.webp
    ├── magic-mirror-hero-1280x720.webp
    └── magic-mirror-hero-768x432.webp
```

## Brand Style

All generated images follow PYB brand: dark cinematic, warm orange lighting (#f59e42), premium event atmosphere. See `prompts.py` for full brand context and per-page scene descriptions.
