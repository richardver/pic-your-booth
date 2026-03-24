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

> **Note:** `docs/templates/` is deprecated — content moved to `docs/website/`, `docs/ads/`, `docs/images/`.
> **Note:** Website not yet deployed to picyourbooth.nl — HTML pages exist in `docs/website/deployment/`.

```
docs/
  plans/                         Brainstorm sessions, design documents, implementation plans
  website/                       Website & design assets
    deployment/                  Live website HTML pages (index, magic-mirror, party-booth, djs, offerte)
      assets/images/             Optimized images for website
    design-system/               HTML design systems, tokens JSON
    djs/                         DJ brand guides & assets
      dj-gianni/                 Brand guide, social/, photos/
      milo/                      Brand guide, profile
  images/                        All image assets
    photos-source/               Original photos (by product/category) — INDEX.md has full catalogue + Gemini picks
    generated/                   AI-generated & processed images
    web/                         Optimized WebP for website
    screenshots/                 Dev screenshots
  ads/                           Ad design & assets
    meta/                        Meta Ads design system HTML
  kpi/                           Historical KPI Excel reports (Vizibooth 2025, 2026)
  funnel/                        Funnel strategy & campaign management
    campaigns/                   Campaign specs per month
    creatives/                   Creative briefs, HTML mockups
    tracking/                    Pixel setup, KPIs, conversion tracking
    results/                     Test results, optimization logs
```

---

## Naming Conventions

- Folders: lowercase, hyphenated (`dj-gianni/`, not `DJ_Gianni/`)
- Files: lowercase, hyphenated, descriptive (`marketing-psychology-pricing.md`)
- HTML design systems: `pyb-design-system-<scope>.html` (web, photobooth, dj, meta-ads)
- DJ templates: `docs/website/djs/<dj-name>/` with `brand-guide.html`, `social/`, `photos/`
- Exported assets: `docs/images/` (PNGs) or `docs/website/djs/<dj-name>/social/<asset>.png`

---

## What Goes Where

| Content Type | Location | Example |
|---|---|---|
| Brainstorm sessions | `docs/plans/` | `brainstorm-homepage-2026-03.md` |
| Design documents | `docs/plans/` | `design-doc-package-builder.md` |
| Implementation plans | `docs/plans/` | `plan-website-phase-1.md` |
| HTML design systems | `docs/website/design-system/` | `pyb-design-system-web.html` |
| Website HTML pages | `docs/website/deployment/` | `index.html`, `magic-mirror.html`, `party-booth.html`, `djs.html`, `offerte.html` |
| Website images | `docs/website/deployment/assets/images/` | `homepage-hero-1920x1080.webp` |
| DJ templates & assets | `docs/website/djs/dj-gianni/` | `brand-guide.html`, `social/` |
| Ad creative templates | `docs/ads/meta/` | `pyb-design-system-meta-ads.html` |
| Source photos | `docs/images/photos-source/` | `magicmirror/`, `partybooth/`, `dj/` — see `INDEX.md` for catalogue + Gemini picks |
| Generated images | `docs/images/generated/` | AI-generated & processed images |
| Dev screenshots | `docs/images/screenshots/` | `hero-homepage.png` |
| KPI reports | `docs/kpi/` | Vizibooth 2025/2026 Excel reports |
| Funnel campaigns | `docs/funnel/campaigns/` | Campaign specs per month |
| Creative briefs | `docs/funnel/creatives/` | HTML mockups, creative briefs |
| Tracking & pixels | `docs/funnel/tracking/` | Pixel setup, KPIs, conversion tracking |
| Test results | `docs/funnel/results/` | Optimization logs |

---

## Rules

1. **Everything in `docs/`** — no separate `knowledge/` folder
2. **One topic per file** — don't merge unrelated topics
3. **Docs are reference material** — not workflows (those go in `.claude/skills/`)
4. **HTML design systems are visual references** — exportable via Playwright
5. **Markdown for text, HTML for visual design systems**
6. **Photos and exports live alongside their profile** — in `docs/website/djs/<dj-name>/`
7. **`pyb-design-tokens.json` is PYM mobile, not PYB web** — see knowledge-design-systems.md
8. **`docs/templates/` is deprecated** — all content moved to `docs/website/`, `docs/ads/`, `docs/images/`
9. **Website not yet deployed** — HTML pages in `docs/website/deployment/`, not live on picyourbooth.nl
