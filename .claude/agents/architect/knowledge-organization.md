# Docs Organization

How PYB's `docs/` folder is structured and what goes where. All reference material lives in `docs/` — there is no separate `knowledge/` folder.

---

## Project Root Files

| File | Owner | Purpose |
|---|---|---|
| `CLAUDE.md` | Architect | Claude Code project instructions — agent routing, project structure, quick commands |
| `README.md` | Architect | Human-readable repo overview — services, agents, structure, design system |

Both files must be updated when agents, skills, or repo structure changes.

## Folder Structure

> **Note:** `docs/templates/` has been removed — content moved to `docs/pyb/website/`, `images/`, and `.claude/agents/dj-promoter/` (DJ docs).
> **Note:** Website not yet deployed to picyourbooth.nl — HTML pages exist in `docs/pyb/website/deployment/`.

```
docs/
  plans/                         Brainstorm sessions, design documents, implementation plans
  images/                        All image assets
    pyb/                         PYB brand (logo, heroes, USPs, modals, meta-ads, screenshots)
    dj-gianni/                   DJ Gianni (profile, social, mixtape covers + PROMPTS.md)
    dj-milo/                     Milø (profile)
    photos-source/               Original photos (by product/category) — INDEX.md has full catalogue + Gemini picks
    web/                         Optimized WebP for website
  pyb/website/                   Website pages & design systems
    deployment/                  Live HTML pages served by TransIP (DO NOT MOVE)
      assets/images/             Optimized images for website
    homepage/                    Homepage design system
    magic-mirror/                Magic Mirror page design system
    party-booth/                 Party Booth page design system
    djs/                         DJs page design system
    offerte/                     Offerte page design system
  kpi/                           Historical KPI Excel reports (Vizibooth 2025, 2026)
  funnel/                        Funnel strategy & campaign management
    campaigns/                   Campaign specs per month
    tracking/                    Pixel setup, KPIs, conversion tracking
    results/                     Test results, optimization logs
video/                           Video production (Remotion) — at project root, NOT in docs/
  templates/tiktok/release-clip/ Shared Release Clip template (React)
  output/<dj>/tiktok/...         Per-DJ rendered output (MP4 + analysis)
  tools/audio-analyzer/          Audio analysis tool (ffmpeg + numpy)
```

---

## Naming Conventions

- Folders: lowercase, hyphenated (`dj-gianni/`, not `DJ_Gianni/`)
- Files: lowercase, hyphenated, descriptive (`marketing-psychology-pricing.md`)
- HTML design systems: `pyb-design-system-<scope>.html` (web, photobooth, dj, meta-ads)
- DJ brand docs: `.claude/agents/dj-promoter/dj-<name>-*.md` (profiles, voice tags, bios)
- DJ design assets: `.claude/agents/designer/dj-<name>-*.html` (brand guides, component refs)
- DJ images: `images/dj-<name>/` (profile photos, mixtape covers, social assets)

---

## What Goes Where

| Content Type | Location | Example |
|---|---|---|
| Brainstorm sessions | `docs/plans/` | `brainstorm-homepage-2026-03.md` |
| Design documents | `docs/plans/` | `design-doc-package-builder.md` |
| Implementation plans | `docs/plans/` | `plan-website-phase-1.md` |
| HTML design systems | `docs/pyb/website/` | `pyb-design-system-web.html` |
| Website HTML pages | `docs/pyb/website/deployment/` | `index.html`, `magic-mirror.html`, `party-booth.html`, `djs.html`, `offerte.html` |
| Website images | `docs/pyb/website/deployment/assets/images/` | `homepage-hero-1920x1080.webp` |
| DJ templates & assets | `.claude/agents/dj-promoter/dj-gianni-` | `brand-guide.html` |
| Ad creative templates | `images/pyb/meta-ads/` | `pyb-design-system-meta-ads.html` |
| Source photos | `images/photos-source/` | `magicmirror/`, `partybooth/`, `dj/` — see `INDEX.md` for catalogue + Gemini picks |
| Output images (PYB) | `images/pyb/` | Generated heroes, USPs, modals, logos, screenshots |
| Output images (DJ Gianni) | `images/dj-gianni/` | Profile, social, mixtape covers + PROMPTS.md |
| Output images (Milø) | `images/dj-milo/` | Profile photos |
| KPI reports | `docs/kpi/` | Vizibooth 2025/2026 Excel reports |
| Funnel campaigns | `docs/funnel/campaigns/` | Campaign specs per month |
| Creative briefs | `docs/funnel/` | HTML mockups, creative briefs |
| Tracking & pixels | `docs/funnel/tracking/` | Pixel setup, KPIs, conversion tracking |
| Test results | `docs/funnel/results/` | Optimization logs |

---

## Python Virtual Environment (`.venv`)

Project-root `.venv/` provides tooling for image processing and AI automation. No application code -- this is a knowledge-base repo, but the venv supports scripts.

- **Python:** 3.14
- **Activate:** `source /Users/richardversluis/code/pic-your-booth/.venv/bin/activate` or run directly via `.venv/bin/python3`

| Package | Version | Purpose |
|---|---|---|
| Pillow | 12.1.1 | Image processing (resize, convert, WebP export) |
| google-generativeai | 0.8.6 | Gemini AI API (image enhance, generate) |
| google-genai | 1.68.0 | Gemini AI client |
| google-api-python-client | 2.193.0 | Google APIs |
| python-dotenv | 1.2.2 | Environment variable management (`.env`) |
| httpx | 0.28.1 | HTTP client |
| requests | 2.32.5 | HTTP requests |
| pydantic | 2.12.5 | Data validation |
| cryptography | 46.0.5 | Crypto utilities |
| websockets | 16.0 | WebSocket support |

---

## Rules

1. **Everything in `docs/`** — no separate `knowledge/` folder
2. **One topic per file** — don't merge unrelated topics
3. **Docs are reference material** — not workflows (those go in `.claude/skills/`)
4. **HTML design systems are visual references** — exportable via Playwright
5. **Markdown for text, HTML for visual design systems**
6. **DJ brand docs live with dj-promoter** — `.claude/agents/dj-promoter/dj-<name>-*`
7. **`pyb-design-tokens.json` is PYM mobile, not PYB web** — see knowledge-design-systems.md
8. **`docs/templates/` is deprecated** — all content moved to `docs/pyb/website/` and `images/`
9. **Video production lives at project root** — `video/`, not `docs/video/`
