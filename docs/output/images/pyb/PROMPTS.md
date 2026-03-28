# PYB - Gegenereerde Assets & Prompts

Alle AI-gegenereerde en verwerkte afbeeldingen voor PicYourBooth. Assets gegenereerd met Gemini AI via de asset-generator pipeline.

---

## Generatie Pipeline

**Script:** `.claude/agents/designer/scripts/asset-generator/asset-generator.py`
**Prompts:** `.claude/agents/designer/scripts/asset-generator/prompts.py`
**Gids:** `.claude/agents/designer/scripts/asset-generator/PROMPTS-GUIDE.md`

**Modes:**
- `enhance` — Real foto als referentie + Gemini AI styling (ALTIJD gebruiken als product zichtbaar is)
- `generate` — Alleen tekst prompt, Gemini maakt alles from scratch (alleen voor mood/concept images)
- `resize` — Geen AI, alleen resize/crop + brand color grading + WebP conversie

---

## Magic Mirror XL (`magic-mirror/`)

| Bestand | Mode | Bronbestand |
|---------|------|-------------|
| `magic-mirror-hero-meta-wedding.png` | enhance | `photos-source/magicmirror/photobooth/magic-mirror-photobooth-5.jpg` |
| `magic-mirror-hero-our-mirror.png` | enhance | `photos-source/magicmirror/photobooth/magic-mirror-vip-venue-wide.png` |
| `magic-mirror-usp-fotos-inlijsten-generated.png` | enhance | `photos-source/magicmirror/usp - fotos die je wilt inlijsten/` |
| `magic-mirror-usp-gasten-ster-generated.png` | enhance | `photos-source/magicmirror/usp - gasten voelen zich een ster/` |
| `magic-mirror-usp-iedereen-geweldig-generated.png` | enhance | `photos-source/magicmirror/usp - iedereen ziet er geweldig uit/` |
| `magic-mirror-usp-meenemen-generated.png` | enhance | `photos-source/magicmirror/usp - meenemen niet vergeten/` |
| `magic-mirror-modal-live-dj-gianni-v1.png` | enhance | DJ setup reference |
| `magic-mirror-cutout.png` | resize | Product cutout, no AI |
| `magic-mirror-cutout-portrait.png` | resize | Product cutout portrait, no AI |

**Brand color grade:** Dark cinematic, warm amber/gold, high contrast (1.22), crushed blues, editorial vignette.

---

## Party Booth (`party-booth/`)

| Bestand | Mode | Bronbestand |
|---------|------|-------------|
| `party-booth-hero-neon-modern-v4.png` | enhance | `photos-source/partybooth/product/party-booth-venue-setup-stringlights.png` |
| `party-booth-hero-meta-wedding.png` | enhance | `photos-source/partybooth/product/party-booth-party-atmosphere-hero.jpg` |
| `party-booth-usp-direct-delen-v2.png` | enhance | `photos-source/partybooth/usp - direct delen/` |
| `party-booth-usp-past-overal-v1.png` | enhance | `photos-source/partybooth/usp - past overal/` |
| `party-booth-usp-zelf-opzetten-v3.png` | enhance | `photos-source/partybooth/product/` |
| `party-booth-modal-bezorging-v1.png` | enhance | Delivery/setup reference |
| `party-booth-modal-live-dj-milo-v1.png` | enhance | DJ setup reference |
| `party-booth-modal-premium-design-v1.png` | enhance | Template design reference |
| `party-booth-cutout.png` | resize | Product cutout, no AI |

**Brand color grade:** Warm festive, gentle contrast (1.06), soft Fujifilm look, airy brightness.

---

## Homepage (`homepage/`)

| Bestand | Mode |
|---------|------|
| `homepage-hero-generated.png` | generate |
| `djs-hero-generated.png` | generate |

---

## Logo (`logo/`)

| Bestand | Methode |
|---------|---------|
| `logo-3000x3000.png` | Playwright export |
| `logo-3000x3000.svg` | Playwright export |
| `logo-3000x3000-dark.png` | Playwright export (dark variant) |
| `logo-3000x3000-transparent.png` | Playwright export (transparent bg) |
| `logo-navbar-dark.png` | Playwright export (navbar size) |
| `logo-navbar-transparent.png` | Playwright export (navbar transparent) |

**Export bron:** `docs/images/logo-export.html` en `docs/images/logo-export-3000.html`

---

## WebP Pipeline

Gegenereerde PNGs worden via de asset-generator resize mode omgezet naar WebP:
- **Output:** `docs/images/website/` (pipeline output) en `docs/website/deployment/assets/images/` (live website)
- **Quality:** 85
- **Responsive breakpoints:** hero 1920x1080, 1280x720, 768x432 | usp 400x400 | modal 800x600 | og 1200x630
