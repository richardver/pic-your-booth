# Website Page Templates — Design Document

**Date:** 2026-03-23
**Status:** Approved
**Author:** Richard + Claude

---

## Overview

Build 5 standalone HTML page templates for picyourbooth.nl. Each page is a self-contained, browser-viewable HTML file with inline CSS + Google Fonts + Unsplash imagery. These serve as the definitive visual spec before converting to Next.js + Shadcn/ui.

## Output

5 files in `docs/templates/website/`:

| File | Route | Primary Segment | Visual Mode |
|---|---|---|---|
| `homepage.html` | `/` | All segments | Gold accent |
| `magic-mirror.html` | `/magic-mirror` | Perfectionist + Zakelijk | Gold accent, premium |
| `party-booth.html` | `/party-booth` | Slimme Feestganger | Gold accent, accessible |
| `djs.html` | `/djs` | Alles-in-één | Violet accent (coral/cyan profiles) |
| `offerte.html` | `/offerte` | All (conversion) | Gold accent |

## Shared Elements

- PYB design tokens (dark base #08080b, gold #f59e42, violet #8b5cf6)
- Bebas Neue (headings) + Space Grotesk (body) from Google Fonts
- Nav: PICYOURBOOTH | Party Booth | Magic Mirror XL | DJs | "BOEK JE ERVARING" (gold pill, black text)
- Footer: minimal
- Unsplash placeholder images (event/party/DJ photography)
- All copy in Dutch — from strategist hooks + product specs
- Current pricing: €199 / €599 / €149 / €25 / €35 / €49 / €499
- Standalone HTML — no external deps except Google Fonts + Unsplash

## Build Process Per Page

1. Load strategist: segment pain points + USPs + hooks
2. Load product-specialist: specs, upgrades, pricing
3. Load designer: tokens, components, CRO
4. Build with `/impeccable:frontend-design`
5. QA: `/impeccable:audit` → `/impeccable:typeset` → `/impeccable:arrange` → `/impeccable:polish`
6. CRO checklist score (target 85+)
7. Brand check via strategist voice rules

## Page Specs

### 1. Homepage (`/`)

**Purpose:** First impression. Show what PYB offers, build trust, drive to product pages or form.

**Sections:**
1. Nav
2. Hero — "JOUW EVENT VERDIENT DIT MOMENT" (gold gradient), event photo bg (0.15 opacity), dark gradient overlay. No buttons in hero.
3. Social Proof Bar — 237+ Events Verzorgd | 4.9★ Google Reviews | Randstad & Omgeving
4. Service Cards (3 columns) — Party Booth €199, Magic Mirror XL €599 (MEEST GEKOZEN badge), DJs €149
5. Testimonial — gold dividers, italic quote
6. Footer

**Conversion psychology:** Anchoring (Magic Mirror in middle as MEEST GEKOZEN), social proof first, page flow drives to product pages.

### 2. Magic Mirror XL (`/magic-mirror`)

**Purpose:** Convince and convert. Package builder drives upsells.

**Sections:**
1. Nav
2. Product Hero — "MAGIC MIRROR XL" (gold gradient). Subtitle: DSLR kwaliteit, geen tijdslimiet, bezorging/installatie/ophalen inbegrepen.
3. USPs (4 items, gold left border) — Foto's Die Je Wilt Inlijsten, Iedereen Ziet Er Geweldig Uit, Meenemen Niet Vergeten, Gasten Voelen Zich Een Ster
4. Package Builder — "BOUW JOUW PERFECTE AVOND"
   - Base: Magic Mirror XL €599 (locked, gold tint)
   - Toggles: VIP (+€149), Wedding Keychain Station (+€499), On-Site Host (+€149), AI Photo Experience (+€499), Live DJ Set (+€149)
   - Running total incl. BTW
   - CTA: "CHECK BESCHIKBAARHEID"
5. Footer

**Key messaging:** "Geen tijdslimiet", "Wij bezorgen, installeren en halen op", DSLR quality. AI Photo Experience prominent for zakelijk segment.

### 3. Party Booth (`/party-booth`)

**Purpose:** Accessible entry point. Low friction, fun.

**Sections:**
1. Nav
2. Product Hero — "PARTY BOOTH" (gold gradient). Subtitle: fotoplezier voor elk feest, vanaf €199, klaar in 5 minuten.
3. USPs (4 items) — Direct Delen Op Socials, Geen Monteur Geen Stress, Past Op Elke Locatie, Klaar In 5 Minuten
4. AI Achtergrond callout — "Lelijke achtergrond? wij fixen het" + beautify filter. Visual before/after suggestion.
5. Package Builder — "BOUW JOUW FEESTPAKKET"
   - Base: Party Booth €199
   - Toggles: Premium Fotostrip Design (+€25), Bezorging Installatie & Ophalen (+€49), AI Achtergrond + Beautify (+€35), Live DJ Set (+€149)
   - Running total incl. BTW
   - CTA: "CHECK BESCHIKBAARHEID"
6. Footer

**Key messaging:** Easiest, cheapest, fun. AI Achtergrond as differentiator. DJ as surprise upgrade.

### 4. DJs (`/djs`)

**Purpose:** Showcase DJ Gianni + Milo. Spotify playlist-optimalisatie as USP. Drive DJ bookings (organic, not via ads in Fase 1).

**Sections:**
1. Nav (DJs link active)
2. Hero — gradient text (coral → violet → cyan) "JOUW FEEST, ONZE DJS". Subtitle: vanaf €149, Spotify playlist-optimalisatie. Waveform decoration.
3. DJ Gianni Profile — real photo (profiel.jpeg), coral accent, "Elke set een feest", genre tags, socials
4. Milo Profile — placeholder photo, cyan accent, "Je voelt de bass, je vergeet de tijd", genre tags
5. Spotify Section — "ALLEEN BIJ PICYOURBOOTH" badge (violet). "STUUR JE PLAYLIST, KRIJG EEN PROFESSIONELE SET"
6. How It Works — 3 steps (violet): Kies Je Vibe → Stuur Je Spotify → Wij Komen, Jij Geniet
7. Booking Wizard — base €149 + extra hours radio (4/5/6 uur)
8. Footer

**Key messaging:** Spotify optimization (nobody else offers this), €149 vs €600+ bij bureaus, twee stijlen.

### 5. Offerte (`/offerte`)

**Purpose:** The conversion point. Minimal friction.

**Sections:**
1. Nav
2. Form Header — "IS JOUW DATUM NOG VRIJ?" (scarcity hook). Subtitle: "Vul 6 velden in... Geen verplichtingen, geen kleine lettertjes."
3. Form Card — dark surface, gold focus states
   - Naam (text), E-mail (email), Telefoon (tel), Datum Event (date + "populaire data gaan snel"), Type Event (select), Bericht (textarea, optional, pre-filled from builder)
4. CTA: "VRAAG VRIJBLIJVEND VOORSTEL AAN" (gold, black text)
5. Trust line: "Reactie binnen 24 uur · 100% vrijblijvend · Geen spam, beloofd"
6. Footer

**Key messaging:** Scarcity, zero risk, fast response. Pre-fill from package builders.

## What Changes After Build

- `pyb-design-system-photobooth.html` keeps only design system foundations (colors, typography, components, principles)
- Page mockups removed from it — replaced by 5 individual page templates
- `pyb-design-system-dj.html` keeps as DJ design system reference — `djs.html` becomes the actual page template

## Success Criteria

- Each page scores 85+ on CRO 55-item checklist
- All pricing matches current specs (€199/€599/€149/€25/€35/€49/€499)
- All copy in native Dutch (not translated)
- Brand voice check passes
- Mobile-responsive (70%+ traffic is mobile)
- WCAG AA contrast
- Impeccable audit passes
