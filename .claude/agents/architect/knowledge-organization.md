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

```
docs/
  plans/               Brainstorm sessions, design documents, implementation plans
  templates/           Visual templates & assets
    design-system/     HTML design systems, tokens JSON
    djs/dj-gianni/     Brand guide, social/, photos/, profile, voice-tags
    djs/milo/          Brand guide, profile
    ads/meta/          Meta Ads design system
  marketing/           Shared psychology frameworks (buyer-journey, pricing)
  website/             PRD, CRO checklist, landing page frameworks
  export-guide.md      Playwright export workflow for design assets
```

---

## Naming Conventions

- Folders: lowercase, hyphenated (`dj-gianni/`, not `DJ_Gianni/`)
- Files: lowercase, hyphenated, descriptive (`marketing-psychology-pricing.md`)
- HTML design systems: `pyb-design-system-<scope>.html` (web, photobooth, dj, meta-ads)
- DJ templates: `docs/templates/djs/<dj-name>/` with `brand-guide.html`, `social/`, `photos/`
- Exported assets: `docs/templates/djs/<dj-name>/social/<asset>.png`

---

## What Goes Where

| Content Type | Location | Example |
|---|---|---|
| Brainstorm sessions | `docs/plans/` | `brainstorm-homepage-2026-03.md` |
| Design documents | `docs/plans/` | `design-doc-package-builder.md` |
| Implementation plans | `docs/plans/` | `plan-website-phase-1.md` |
| HTML design systems | `docs/templates/design-system/` | `pyb-design-system-web.html` |
| Website page templates | `docs/templates/website/` | `homepage.html`, `magic-mirror.html`, `party-booth.html`, `djs.html`, `offerte.html` |
| DJ templates & assets | `docs/templates/djs/dj-gianni/` | `brand-guide.html`, `social/` |
| Ad creative templates | `docs/templates/ads/meta/` | `pyb-design-system-meta-ads.html` |

---

## Rules

1. **Everything in `docs/`** — no separate `knowledge/` folder
2. **One topic per file** — don't merge unrelated topics
3. **Docs are reference material** — not workflows (those go in `.claude/skills/`)
4. **HTML design systems are visual references** — exportable via Playwright
5. **Markdown for text, HTML for visual design systems**
6. **Photos and exports live alongside their profile** — in `docs/templates/djs/<dj-name>/`
7. **`pyb-design-tokens.json` is PYM mobile, not PYB web** — see knowledge-design-systems.md
8. **`website/` not `photobooth/`** — the folder is about website design, not the product
