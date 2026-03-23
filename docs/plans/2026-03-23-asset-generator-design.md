# Asset Generator — Design Document

**Date:** 2026-03-23
**Status:** Approved
**Author:** Richard + Claude

---

## Overview

Python-based asset generation pipeline: source photos + Gemini AI styling + automated resize/crop/WebP conversion. Two modes: enhance (real photo as reference) and generate (text prompt only).

## Workflow

```
Source Photo → Gemini AI (style/enhance) → Master Image → Python Script (resize/crop/WebP) → Web-ready files
```

## Folder Structure

```
docs/assets/
├── source-photos/       ← Real booth/DJ photos (input)
│   ├── magicmirror/
│   ├── partybooth/
│   └── dj/
├── generated/           ← Raw AI output (PNG, full res)
└── web/                 ← Final optimized (WebP, multiple sizes)
```

## Script Location

`.claude/agents/designer/scripts/asset-generator/`

## Components

1. `asset-generator.py` — main script (resize, crop, WebP convert)
2. `prompts.py` — Gemini prompt templates per page/usage
3. `requirements.txt` — Pillow, google-generativeai

## Dimensions

| Usage | Sizes | Format |
|---|---|---|
| Hero (responsive) | 1920x1080, 1280x720, 768x432 | WebP |
| USP thumbnails | 400x400 | WebP |
| Service cards | 600x400 | WebP |
| Modal images | 800x600 | WebP |
| OG share | 1200x630 | PNG |

## Gemini Integration

- Model: Gemini 3 Pro (Google AI Studio)
- API key: `GOOGLE_AI_API_KEY` env var
- Brand prompt: dark cinematic, warm lighting, premium event atmosphere
- Source photo mode: keeps product authentic, enhances environment

## New Skill

`/generate-asset` — provides source photo + scene description + target page, outputs web-ready files.
