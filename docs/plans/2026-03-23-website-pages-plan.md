# Website Page Templates — Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Build 5 standalone HTML page templates for picyourbooth.nl — viewable in browser, definitive visual spec.

**Architecture:** Each page is a self-contained HTML file with inline CSS, Google Fonts (Bebas Neue + Space Grotesk), and Unsplash imagery. PYB design tokens from `pyb-design-system-web.html`. All copy in Dutch from strategist hooks + product specs.

**Tech Stack:** HTML + CSS (inline), Google Fonts, Unsplash images, Playwright for review screenshots.

---

## Pre-Build: Load Strategy Context

Before building ANY page, load these knowledge files to have the full picture:

**Strategist:**
- `.claude/agents/strategist/knowledge-brand.md` — mission, vision, tone
- `.claude/agents/strategist/knowledge-segments.md` — buyer profiles, pain points, JTBD
- `.claude/agents/strategist/knowledge-usps.md` — USPs per product/segment
- `.claude/agents/strategist/knowledge-hooks.md` — Dutch hooks per segment/platform
- `.claude/agents/strategist/knowledge-pricing-strategy.md` — charm pricing, anchoring

**Product Specialist:**
- `.claude/agents/product-specialist/knowledge-magic-mirror.md` — Magic Mirror specs, upgrades
- `.claude/agents/product-specialist/knowledge-party-booth.md` — Party Booth specs, upgrades, AI
- `.claude/agents/product-specialist/knowledge-dj-services.md` — DJ specs, Spotify optimization
- `.claude/agents/product-specialist/knowledge-pricing.md` — all prices

**Designer:**
- `.claude/agents/designer/knowledge-design-system.md` — tokens, colors, visual modes
- `.claude/agents/designer/knowledge-components.md` — Shadcn component mapping
- `.claude/agents/designer/knowledge-website.md` — PYB page templates, form spec
- `.claude/agents/designer/knowledge-cro-checklist.md` — 55-item CRO checklist
- `.impeccable.md` — Impeccable design context

**Design system reference:**
- `docs/templates/design-system/pyb-design-system-web.html` — CSS tokens to copy
- `docs/plans/prd-website.md` — canonical page spec (sections, copy, interactions)

---

### Task 1: Homepage (`docs/templates/website/homepage.html`)

**Files:**
- Create: `docs/templates/website/homepage.html`

**Step 1: Load context**
- Read strategist `knowledge-hooks.md` → Magic Mirror XL Algemeen + Party Booth + DJ hooks
- Read strategist `knowledge-segments.md` → all 4 segments (homepage serves all)
- Read PRD `docs/plans/prd-website.md` lines 84-97 → homepage spec

**Step 2: Build page with `/impeccable:frontend-design`**

Sections to build:
1. **Nav** — PICYOURBOOTH logo | Party Booth | Magic Mirror XL | DJs | "BOEK JE ERVARING" (gold pill, black text)
2. **Hero** — Unsplash event photo (0.15 opacity), dark gradient overlay. Gold gradient headline: "JOUW EVENT VERDIENT DIT MOMENT". Subtitle: "Premium photobooths & DJ entertainment in de Randstad." No CTA button in hero.
3. **Social Proof Bar** — "237+" | "Events Verzorgd" · "4.9★" | "Google Reviews" · "Randstad" | "& Omgeving". Gold numbers, muted labels, gold dividers.
4. **Service Cards** (3 columns):
   - Party Booth — "Foto plezier voor elk feest" — €199 gold pill — "Meer info →"
   - Magic Mirror XL — "Niet zomaar een booth — een ervaring" — €599 gold pill — "MEEST GEKOZEN" badge — "Meer info →"
   - DJs — "De perfecte soundtrack voor je event" — €149 violet pill — "Meer info →"
5. **Testimonial** — Gold divider lines. Italic quote. Author + event type.
6. **Footer** — PicYourBooth · Pic Your Moment BV · info@picyourbooth.nl · Instagram · TikTok

Design tokens: dark bg #08080b, surface #111116, text #ededf0, gold #d4b14e, violet #8b5cf6.
Typography: Bebas Neue headings (uppercase, 0.06em spacing), Space Grotesk body.
Mobile-first: responsive grid, 44px touch targets, sticky nav.

**Step 3: QA pipeline**
- Run `/impeccable:audit` — fix all issues
- Run `/impeccable:typeset` — verify Bebas Neue + Space Grotesk
- Run `/impeccable:arrange` — fix layout/spacing
- Run `/impeccable:polish` — final pass

**Step 4: Brand check**
- [ ] All Dutch copy sounds native
- [ ] Charm pricing (€199, €599, €149)
- [ ] Gold buttons = black text
- [ ] No red or pink colors
- [ ] "MEEST GEKOZEN" on Magic Mirror XL
- [ ] Party Booth (not iPad Photobooth)

**Step 5: Commit**
```bash
git add docs/templates/website/homepage.html
git commit -m "feat: homepage template — hero, social proof, service cards, testimonial"
```

---

### Task 2: Magic Mirror XL (`docs/templates/website/magic-mirror.html`)

**Files:**
- Create: `docs/templates/website/magic-mirror.html`

**Step 1: Load context**
- Read strategist `knowledge-hooks.md` → Magic Mirror Algemeen + Bruiloft + Zakelijk + AI hooks
- Read strategist `knowledge-segments.md` → Perfectionist + Zakelijk segments
- Read product-specialist `knowledge-magic-mirror.md` → full specs, upgrades, AI Photo Experience
- Read PRD lines 99-125 → Magic Mirror spec

**Step 2: Build page with `/impeccable:frontend-design`**

Sections:
1. **Nav** (same as homepage)
2. **Product Hero** — "MAGIC MIRROR XL" (gold gradient). Subtitle: "DSLR kwaliteit · Geen tijdslimiet · Bezorging, installatie & ophalen inbegrepen". Unsplash event/photobooth image.
3. **USPs** (4 items, vertical, gold left border):
   - "FOTO'S DIE JE WILT INLIJSTEN" — DSLR camera met professionele studiobelichting
   - "IEDEREEN ZIET ER GEWELDIG UIT" — Professionele belichting die iedereen flatteert
   - "MEENEMEN, NIET VERGETEN" — Direct geprinte foto's als aandenken
   - "GASTEN VOELEN ZICH EEN STER" — VIP ervaring met rode loper en stijlvolle props
4. **Package Builder** — "BOUW JOUW PERFECTE AVOND"
   - Base: Magic Mirror XL — €599 (locked, gold tint card)
   - Toggle: VIP Upgrade — +€149 (backdrop, rode loper, afzetpalen, luxe props)
   - Toggle: Wedding Keychain Station — +€499 (onbeperkt gepersonaliseerde sleutelhangers — geen apart bedankje meer kopen)
   - Toggle: On-Site Host — +€149 (PYB teamlid begeleidt gasten de hele avond)
   - Toggle: AI Photo Experience — +€499 (AI genereert unieke branded foto's — ideaal voor productlanceringen)
   - Toggle: Live DJ Set — +€149 (DJ met speakers, licht, rookmachine — 3 uur)
   - Each toggle: ? info button
   - Running total (incl. 21% BTW)
   - CTA: "CHECK BESCHIKBAARHEID" (gold, black text)
5. **Footer**

Interactive: toggles update running total. CTA links to offerte with pre-fill.

**Step 3: QA pipeline** (same as Task 1)

**Step 4: Brand check + CRO check**
- Score against CRO checklist — target 85+
- Verify "geen tijdslimiet" is prominent
- Verify "bezorging, installatie & ophalen inbegrepen" is visible
- AI Photo Experience clearly explains the AI process

**Step 5: Commit**
```bash
git add docs/templates/website/magic-mirror.html
git commit -m "feat: magic mirror template — hero, USPs, package builder with 5 upgrades"
```

---

### Task 3: Party Booth (`docs/templates/website/party-booth.html`)

**Files:**
- Create: `docs/templates/website/party-booth.html`

**Step 1: Load context**
- Read strategist `knowledge-hooks.md` → Party Booth + AI Achtergrond hooks
- Read strategist `knowledge-segments.md` → Slimme Feestganger segment
- Read product-specialist `knowledge-party-booth.md` → full specs, AI Achtergrond + Beautify
- Read PRD lines 127-149 → Party Booth spec

**Step 2: Build page with `/impeccable:frontend-design`**

Sections:
1. **Nav** (same)
2. **Product Hero** — "PARTY BOOTH" (gold gradient). Subtitle: "Fotoplezier voor elk feest · Vanaf €199 · Klaar in 5 minuten". Unsplash party photo.
3. **USPs** (4 items):
   - "DIRECT DELEN OP SOCIALS" — Gasten delen foto's direct via QR code
   - "GEEN MONTEUR, GEEN STRESS" — Zelf ophalen, 5 minuten opzetten, klaar
   - "PAST OP ELKE LOCATIE" — Compact, werkt overal
   - "KLAAR IN 5 MINUTEN" — Simpel, snel, zonder gedoe
4. **AI Achtergrond Callout** — "LELIJKE ACHTERGROND? AI FIXT HET" + before/after visual suggestion. "Inclusief beautify filter voor super strakke resultaten." Price: +€35.
5. **Package Builder** — "BOUW JOUW FEESTPAKKET"
   - Base: Party Booth — €199
   - Toggle: Premium Fotostrip Design — +€25
   - Toggle: Bezorging, Installatie & Ophalen — +€49
   - Toggle: AI Achtergrond + Beautify — +€35
   - Toggle: Live DJ Set — +€149
   - Running total, CTA
6. **Footer**

Tone: fun, accessible, easy. Not premium — celebratory.

**Step 3-5:** QA + brand check + commit (same pattern)
```bash
git commit -m "feat: party booth template — hero, USPs, AI callout, package builder"
```

---

### Task 4: DJs (`docs/templates/website/djs.html`)

**Files:**
- Create: `docs/templates/website/djs.html`

**Step 1: Load context**
- Read strategist `knowledge-hooks.md` → DJ hooks + Combo hooks
- Read strategist `knowledge-segments.md` → Alles-in-één Zoeker
- Read product-specialist `knowledge-dj-services.md` → DJ Gianni, Milo, Spotify, pricing
- Read social-media `knowledge-dj-gianni.md` + `knowledge-dj-milo.md` → profiles, bios
- Read PRD lines 151-175 → DJs spec

**Step 2: Build page with `/impeccable:frontend-design`**

Sections:
1. **Nav** (DJs link active state)
2. **Hero** — Unsplash DJ photo (blurred, 0.15 opacity). Gradient text (coral → violet → cyan): "JOUW FEEST, ONZE DJS". Subtitle: "Vanaf €149 per avond · Spotify playlist-optimalisatie · Speakers, licht & rookmachine inbegrepen". Waveform decoration (subtle CSS animated bars).
3. **DJ Gianni Profile** — Real photo (`docs/templates/djs/dj-gianni/photos/profiel.jpeg`), coral accent (#f0654a). Name: "DJ GIANNI". Tagline: "Elke set een feest, elk feest een herinnering". Bio. Genre tags (coral): Afro Beats, Caribbean, Nederlands, Hits. Social links: IG, TikTok, SoundCloud.
4. **Milo Profile** — Unsplash placeholder, cyan accent (#22d3ee). Name: "MILO". Tagline: "Je voelt de bass, je vergeet de tijd". Bio. Genre tags (cyan): House, Techno, Deep. Social links.
5. **Spotify Section** — "ALLEEN BIJ PICYOURBOOTH" badge (violet). "STUUR JE PLAYLIST, KRIJG EEN PROFESSIONELE SET". Explain: stuur playlist → DJ analyseert → professionele set op maat. Playlist visual. CTA: "PLAN JE FEEST MET ONS" (violet).
6. **How It Works** — "IN 3 STAPPEN GEREGELD" (violet left border):
   - 01 KIES JE VIBE — Afro Beats met DJ Gianni of House met Milo
   - 02 STUUR JE SPOTIFY — Wij bouwen er een professionele set van
   - 03 WIJ KOMEN, JIJ GENIET — Speakers, licht, rookmachine — alles geregeld
7. **Booking Wizard** — "BOEK JE DJ"
   - Base: DJ Set 3 uur — €149 (violet)
   - Radio: +1 uur (+€49), +2 uren (+€98), +3 uren (+€147)
   - Running total incl. BTW
   - CTA: "CHECK BESCHIKBAARHEID" (violet)
   - Subtitle: "Een DJ-bureau rekent €600+. Bij ons vanaf €149 inclusief alles."
8. **Footer**

Visual mode: violet primary, coral for Gianni elements, cyan for Milo elements.

**Step 3-5:** QA + brand check + commit
```bash
git commit -m "feat: djs template — profiles, Spotify section, booking wizard"
```

---

### Task 5: Offerte (`docs/templates/website/offerte.html`)

**Files:**
- Create: `docs/templates/website/offerte.html`

**Step 1: Load context**
- Read strategist `knowledge-segments.md` → all segments (form serves all)
- Read designer `knowledge-website.md` → form spec, personalization, email sequences
- Read designer `knowledge-forms.md` → form UX frameworks
- Read PRD lines 177-195 → Offerte spec

**Step 2: Build page with `/impeccable:frontend-design`**

Sections:
1. **Nav** (same)
2. **Form Header** — "IS JOUW DATUM NOG VRIJ?" (gold gradient, scarcity hook). Subtitle: "Vul 6 velden in en ontvang binnen 24 uur een vrijblijvend voorstel op maat. Geen verplichtingen, geen kleine lettertjes."
3. **Form Card** — dark surface (#111116), rounded corners
   - Naam (text input, gold focus ring)
   - E-mail (email input)
   - Telefoon (tel input — numpad on mobile)
   - Datum Event (date input + "(populaire data gaan snel)" label)
   - Type Event (select: Bruiloft, Bedrijfsfeest, Verjaardag, Festival/Club, Anders)
   - Bericht (textarea, optional — pre-filled when coming from package builder)
4. **CTA:** "VRAAG VRIJBLIJVEND VOORSTEL AAN" (gold, black text, full-width)
5. **Trust line:** "Reactie binnen 24 uur · 100% vrijblijvend · Geen spam, beloofd"
6. **Footer**

Form has no navigation distractions. Single purpose: convert.

**Step 3-5:** QA + brand check + commit
```bash
git commit -m "feat: offerte template — 6-field form, scarcity hook, trust signals"
```

---

### Task 6: Clean Up Old Monolithic File

**Files:**
- Modify: `docs/templates/design-system/pyb-design-system-photobooth.html`

**Step 1:** Remove page mockup sections (Homepage, Magic Mirror, Party Booth, Offerte) from the file
**Step 2:** Keep only: How This Works + Color Palette + Typography + Components + Design Principles
**Step 3:** Update title to "PicYourBooth — Design System Foundations (Photobooth)"
**Step 4:** Add links to new individual page templates

**Step 5: Commit**
```bash
git commit -m "refactor: split page mockups from design system — pages now in docs/templates/website/"
```

---

### Task 7: Update References

**Files:**
- Modify: `CLAUDE.md` — add `docs/templates/website/` to project structure
- Modify: `README.md` — add website templates to repo structure
- Modify: `.claude/agents/architect/knowledge-organization.md` — add website templates location

**Step 1:** Update all three files
**Step 2: Commit**
```bash
git commit -m "docs: update CLAUDE.md, README, architect to reference website page templates"
```
