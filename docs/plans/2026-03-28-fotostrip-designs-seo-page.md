# Fotostrip Designs SEO Page — Design Doc

**Date:** 2026-03-28
**Status:** Parked — ready to build

## Opportunity

No Dutch photobooth competitor offers a public template gallery. PYB has 100+ premium designs via TemplatesBooth. A public, SEO-indexed page captures organic traffic and positions template selection as a USP.

## What to Build

### 1. Public SEO page: `/fotostrip-designs`
- Curated visual grid of template previews (NOT the live widget)
- Category sections: Bruiloft, Verjaardag, Bedrijf, Kerst, etc.
- H1: "Photobooth Fotostrip Designs — Kies Je Eigen Stijl"
- Per-category H2s for SEO
- How it works section (boek, kies, personaliseer, klaar)
- CTA: "Wil je deze designs op jouw feest? Check beschikbaarheid"
- FAQ with schema markup

### 2. Product page integration
- Party Booth: add template USP at position #3, show 6-8 preview thumbnails
- Magic Mirror XL: add in experience section, 3-4 premium previews
- Both link to /fotostrip-designs

### 3. Knowledge updates
- Add template USP to strategist/knowledge-usps.md
- Add keywords to seo/knowledge-keywords.md
- Add hooks to strategist/knowledge-hooks.md

## Target Keywords

| Keyword | Competition | Intent |
|---------|------------|--------|
| photobooth templates | Laag (NL) | Informatief/Commercieel |
| fotostrip ontwerp photobooth | Zeer laag | Commercieel |
| photobooth fotostrip designs | Zeer laag | Commercieel |
| fotostrip design bruiloft | Laag | Commercieel |
| photobooth huren met eigen design | Laag | Commercieel |

## USP Positioning

- **Party Booth:** "Kies uit 100+ premium designs — jouw feest, jouw stijl" (position #3)
- **Magic Mirror XL:** "Personaliseer jullie fotostrip — kies uit 100+ designs" (supporting)

## Hook Copy (Dutch)

**Bruiloft:** "100+ fotostrip designs voor jullie bruiloft — kies het ontwerp dat bij jullie past"
**Verjaardag:** "Van tropical tot minimalist — 100+ premium fotostrip designs, jij kiest"
**Bedrijf:** "Fotostrips in jullie huisstijl — kies een design, wij passen jullie branding toe"

## Architecture

- `/fotostrip-designs` = public SEO page with static previews + CTA to offerte
- `/yourdesign.html` = private post-booking portal (stays noindex, unchanged)
- Product pages link to /fotostrip-designs

## Risks

- Operator traffic: mitigate with event-focused language
- Template expectations: public page shows curated previews only, not interactive widget
- TemplatesBooth dependency: use static preview images, not live widget
