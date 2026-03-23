# PRD: PicYourBooth Website

## Overview

Build the PicYourBooth website from scratch as a modern, high-performance marketing site that converts visitors into proposal requests. Dark premium aesthetic, package builders with real-time pricing, and seamless integration with HubSpot for lead capture.

**Owner:** Richard Versluis
**Brand:** PicYourBooth (Pic Your Moment BV)
**URL:** picyourbooth.nl
**Status:** New build - no legacy site

---

## Goals

1. **Primary:** Drive proposal requests (form submissions) through the Meta Ads → Website → Form funnel
2. **Secondary:** Showcase services, build trust, differentiate from competitors
3. **Tertiary:** Promote DJ personal brands (DJ Gianni + Milo) and drive DJ bookings

### Success Metrics

| Metric | Target | How Measured |
|--------|--------|-------------|
| Form conversion rate | >5% | Google Analytics |
| Bounce rate | <40% | Google Analytics |
| Page load (LCP) | <2.5s | Core Web Vitals |
| Cost per lead | <€25 | Meta Ads + HubSpot |
| Monthly leads | 20+ | HubSpot |

---

## Tech Stack

| Layer | Choice | Why |
|-------|--------|-----|
| Framework | **Next.js 14+ (App Router)** | SSR, SEO, performance, component architecture |
| Styling | **Tailwind CSS** | Design tokens map 1:1, rapid development |
| Fonts | **Bebas Neue + Space Grotesk** (Google Fonts) | Brand fonts, already defined |
| Hosting | **Vercel** | Zero-config deploy, free tier, automatic HTTPS, CDN |
| CRM/Forms | **HubSpot** | Already in use, form embed or API submission |
| Analytics | **Google Analytics 4** | Already in use |
| Tracking | **Meta Pixel + CAPI** | Required for Meta Ads optimization |
| Domain | **picyourbooth.nl** | Existing domain |

---

## Design System

All design decisions are documented in the existing design system files:

| File | Content |
|------|---------|
| `docs/templates/design-system/pyb-design-system-web.html` | Tokens, colors, typography, components |
| `docs/templates/design-system/pyb-design-system-photobooth.html` | Homepage, Magic Mirror, Party Booth, Form mockups |
| `docs/templates/design-system/pyb-design-system-dj.html` | DJ Hub page mockup |
| `.claude/agents/strategist/knowledge-brand.md` | Brand guide, services, pricing |

### Design Tokens

```
Background:    #08080b
Surface:       #111116
Elevated:      #18181e
Text:          #ededf0
Text muted:    rgba(237,237,240,0.60)
Border:        rgba(255,255,255,0.06)
Gold:          #f59e42 (photobooth accent)
Violet:        #8b5cf6 (DJ accent)
Coral:         #f0654a (DJ Gianni)
Cyan:          #0ea5e9 (Milo)
```

### Typography

| Usage | Font | Weight |
|-------|------|--------|
| Headings, nav, prices, labels | Bebas Neue | 400 (uppercase) |
| Body, descriptions, forms | Space Grotesk | 300-700 |

---

## Pages

### 1. Homepage (`/`)

**Purpose:** First impression. Show what PicYourBooth offers, build trust, drive to product pages or form.

**Sections (top to bottom):**

1. **Nav** - Logo (PICYOURBOOTH), links: Party Booth | Magic Mirror XL | DJs, CTA: "BOEK JE ERVARING" (gold pill, black text)
2. **Hero** - Background event photo (0.15 opacity) with dark gradient overlay. Gold gradient headline: "JOUW EVENT VERDIENT DIT MOMENT". Subtitle. No buttons in hero - page flow drives conversion.
3. **Social Proof Bar** - 237+ Events Verzorgd | 4.9★ Google Reviews | Randstad & Omgeving. Gold numbers, muted labels, gold dividers.
4. **Service Cards** (3 columns) - Party Booth (€199), Magic Mirror XL (€599, MEEST GEKOZEN badge), DJs (€149). Each: gold dot, title, description, "Meer info →" link, gold price pill.
5. **Testimonial** - Gold divider lines, italic quote, author + event.
6. **Footer** - Minimal.

**Message match:** Landing page from Meta Ads must echo the ad headline and offer.

### 2. Magic Mirror XL (`/magic-mirror`)

**Purpose:** Convince and convert. Show why Magic Mirror is worth €599. Package builder drives upsells.

**Sections:**

1. **Nav** (same as homepage)
2. **Product Hero** - Centered. Gold gradient title "MAGIC MIRROR XL". Subtitle about DSLR, no time limit, VIP experience.
3. **USPs** (4 items, vertical list) - Each: small image (80px), gold left border, title + description.
   - Foto's Die Je Wilt Inlijsten
   - Iedereen Ziet Er Geweldig Uit
   - Meenemen, Niet Vergeten
   - Gasten Voelen Zich Een Ster
4. **Package Builder** - "BOUW JOUW PERFECTE AVOND"
   - Base: Magic Mirror XL - €599 (locked, gold tint)
   - Upgrades (toggle switches):
     - VIP Upgrade (+€149)
     - Wedding Keychain Station (+€499)
     - On-Site Host (+€149)
     - AI Photo Experience (+€499)
     - Live DJ Set (+€149)
   - Each upgrade has `?` info button → opens modal with photo + description
   - Running total (incl. 21% BTW)
   - CTA: "CHECK BESCHIKBAARHEID" → pre-fills form + scrolls to form
5. **Footer**

**Interactive:** Toggle switches update total. CTA pre-fills proposal form with selected package + upgrades + total price.

### 3. Party Booth (`/party-booth`)

**Purpose:** Same structure as Magic Mirror but positioned as accessible entry point.

**Sections:**

1. **Nav** (same)
2. **Product Hero** - Gold gradient title "PARTY BOOTH". Subtitle about digital fotostrips, ophalen, 5 minuten klaar.
3. **USPs** (4 items)  -
   - Direct Delen Op Socials
   - Geen Monteur, Geen Stress
   - Past Op Elke Locatie
   - Klaar In 5 Minuten
4. **Package Builder** - "BOUW JOUW FEESTPAKKET"
   - Base: Party Booth - €199
   - Upgrades:
     - Premium Fotostrip Design (+€25)
     - Bezorging, Installatie & Ophalen (+€49)
     - AI Achtergrond (+€35)
     - Live DJ Set (+€149)
   - Running total (incl. 21% BTW)
   - CTA → pre-fills form
5. **Footer**

### 4. DJs (`/djs`)

**Purpose:** Showcase DJ Gianni and Milo. Spotify playlist optimization as USP. Drive DJ bookings.

**Sections:**

1. **Nav** (same, DJs link active)
2. **Hero** - Background DJ photo (blurred, 0.15 opacity). Gradient text (coral → violet → cyan): "JOUW FEEST, ONZE DJS". Subtitle with €149 pricing and Spotify mention. Waveform decoration (subtle animated bars).
3. **DJ Gianni Profile** - Avatar (real photo: dj-luca-profiel.jpeg) with EQ bars. Name in coral. Tagline, bio, genre tags (Afro Beats, Caribbean, Nederlands, Hits), socials (IG, TT, SC). Recent sets list with play/pause.
4. **Milo Profile** - Same structure, cyan accent. Avatar placeholder. Genre tags (House, Techno, Deep).
5. **Spotify Section** - "ALLEEN BIJ PICYOURBOOTH" badge (violet). "STUUR JE PLAYLIST, KRIJG EEN PROFESSIONELE SET". Playlist visual with track bars. CTA: "PLAN JE FEEST MET ONS" (violet).
6. **How It Works** - "IN 3 STAPPEN GEREGELD". Three steps with violet left border:
   - 01 KIES JE VIBE
   - 02 STUUR JE SPOTIFY
   - 03 WIJ KOMEN, JIJ GENIET
7. **Booking Wizard** - "BOEK JE DJ"
   - Base: DJ Set 3 uur - €149
   - Extra hours (radio-style, one at a time):
     - +1 uur (+€49) → 4 uur
     - +2 uren (+€98) → 5 uur
     - +3 uren (+€147) → 6 uur
   - Total (incl. 21% BTW)
   - CTA: "CHECK BESCHIKBAARHEID" (violet)
8. **Now Playing Bar** - Appears when user clicks play on a set. Shows set title, progress bar, EQ animation.
9. **Footer**

### 5. Offerte (`/offerte`)

**Purpose:** The conversion point. Minimal friction form.

**Sections:**

1. **Nav** (same)
2. **Form Header** - "IS JOUW DATUM NOG VRIJ?" (scarcity hook). Subtitle: "Vul 6 velden in... Geen verplichtingen, geen kleine lettertjes."
3. **Form Card** (dark surface, gold focus states)  -
   - Naam (text)
   - E-mail (email)
   - Telefoon (tel)
   - Datum Event (date) - label includes "(populaire data gaan snel)"
   - Type Event (select: Bruiloft, Bedrijfsfeest, Verjaardag, Festival/Club, Anders)
   - Bericht (textarea, optional) - pre-filled when coming from package builder
4. **CTA:** "VRAAG VRIJBLIJVEND VOORSTEL AAN" (gold, black text)
5. **Trust line:** "Reactie binnen 24 uur · 100% vrijblijvend · Geen spam, beloofd"

**Form submission:** POST to HubSpot via API or embed HubSpot form.

---

## Integrations

### HubSpot
- Form submissions create contacts + deals in HubSpot
- Include hidden fields: source (Meta Ad / organic), selected package, total price
- Trigger automated proposal email sequence

### Meta Pixel + Conversions API (CAPI)
- Track: PageView, ViewContent, Lead (form submit)
- Server-side CAPI for iOS ATT mitigation
- Event match quality target: >6.0

### Google Analytics 4
- Track: page views, form starts, form completions, package builder interactions
- Custom events: upgrade_toggle, builder_cta_click, set_play

### Zapier
- HubSpot form → Google Sheet (backup)
- HubSpot form → Slack notification (new lead alert)

---

## SEO

### Technical
- Server-side rendered (Next.js SSR)
- Sitemap.xml auto-generated
- robots.txt
- Canonical URLs
- Open Graph + Twitter Card meta tags per page
- Structured data: LocalBusiness schema

### Content
- H1 per page (one, clear)
- Meta title: "PicYourBooth - [Page] | Premium Photobooth & DJ Entertainment"
- Meta description: unique per page, includes CTA
- Alt text on all images
- Dutch language (lang="nl")

### Performance
- LCP < 2.5s
- CLS < 0.1
- Images: WebP/AVIF, lazy loaded below fold
- Fonts: preconnect, font-display: swap
- Minimal JS bundle

---

## Responsive

| Breakpoint | Target |
|------------|--------|
| 0-640px | Mobile (primary - 70%+ traffic from Meta Ads) |
| 640-1024px | Tablet |
| 1024px+ | Desktop |

Mobile-first design. All interactions (toggles, modals, builders) must work on touch.

---

## Accessibility

- WCAG AA color contrast (4.5:1 text, 3:1 UI)
- Keyboard navigation on all interactive elements
- Focus indicators visible
- Form labels linked to inputs
- Alt text on images
- `prefers-reduced-motion` respected
- Semantic HTML (nav, main, section, footer)

---

## Content

All copy is finalized and documented in the design system files. Key conversion copy:

| Page | Headline | CTA |
|------|----------|-----|
| Homepage | JOUW EVENT VERDIENT DIT MOMENT | BOEK JE ERVARING |
| Magic Mirror | MAGIC MIRROR XL | CHECK BESCHIKBAARHEID |
| Party Booth | PARTY BOOTH | CHECK BESCHIKBAARHEID |
| DJs | JOUW FEEST, ONZE DJS | CHECK BESCHIKBAARHEID |
| Form | IS JOUW DATUM NOG VRIJ? | VRAAG VRIJBLIJVEND VOORSTEL AAN |

---

## Pricing (Charm Pricing Applied)

### Party Booth
| Item | Price |
|------|-------|
| Base | €199 |
| Premium Fotostrip Design | +€25 |
| Bezorging, Installatie & Ophalen | +€49 |
| AI Achtergrond | +€35 |
| Live DJ Set | +€149 |

### Magic Mirror XL
| Item | Price |
|------|-------|
| Base | €599 |
| VIP Upgrade | +€149 |
| Wedding Keychain Station | +€499 |
| On-Site Host | +€149 |
| AI Photo Experience | +€499 |
| Live DJ Set | +€149 |

### DJs
| Item | Price |
|------|-------|
| DJ Set (3 uur) | €149 |
| Extra uur | +€49 |

All prices include 21% BTW.

---

## Project Structure

```
picyourbooth/
├── src/
│   ├── app/
│   │   ├── layout.tsx          - Root layout (fonts, meta, nav, footer)
│   │   ├── page.tsx            - Homepage
│   │   ├── magic-mirror/
│   │   │   └── page.tsx        - Magic Mirror XL
│   │   ├── party-booth/
│   │   │   └── page.tsx        - Party Booth
│   │   ├── djs/
│   │   │   └── page.tsx        - DJs hub
│   │   └── offerte/
│   │       └── page.tsx        - Proposal form
│   ├── components/
│   │   ├── Nav.tsx             - Shared navigation
│   │   ├── Footer.tsx          - Shared footer
│   │   ├── Hero.tsx            - Page hero (configurable)
│   │   ├── ServiceCard.tsx     - Homepage service card
│   │   ├── ProofBar.tsx        - Social proof numbers
│   │   ├── Testimonial.tsx     - Quote block
│   │   ├── USPList.tsx         - Vertical USP list with images
│   │   ├── PackageBuilder.tsx  - Base + upgrades + total + CTA
│   │   ├── UpgradeRow.tsx      - Toggle switch upgrade row
│   │   ├── InfoModal.tsx       - Upgrade detail modal
│   │   ├── DJProfile.tsx       - DJ profile section
│   │   ├── SetList.tsx         - Playable set list
│   │   ├── SpotifySection.tsx  - Playlist visual
│   │   ├── BookingWizard.tsx   - DJ booking with hour selector
│   │   ├── ProposalForm.tsx    - HubSpot form
│   │   └── Toggle.tsx          - Reusable toggle switch
│   ├── lib/
│   │   ├── pricing.ts          - Price constants + calculation
│   │   └── hubspot.ts          - Form submission API
│   └── styles/
│       └── globals.css         - Tailwind + custom properties
├── public/
│   ├── images/                 - Optimized event photos
│   └── fonts/                  - Self-hosted if needed
├── tailwind.config.ts          - Design tokens mapped
├── next.config.ts
├── package.json
└── vercel.json
```

---

## Milestones

| Phase | Scope | Deliverable |
|-------|-------|-------------|
| 1. Setup | Next.js + Tailwind + Vercel + domain | Deployed blank site on picyourbooth.nl |
| 2. Layout | Nav, footer, fonts, colors, dark theme | Shared layout working on all pages |
| 3. Homepage | Hero, proof bar, service cards, testimonial | Homepage live |
| 4. Product Pages | Magic Mirror + Party Booth with builders | Package builders working |
| 5. DJs | DJ hub with profiles, sets, Spotify, wizard | DJ page live |
| 6. Form | Proposal form + HubSpot integration | Leads flowing to HubSpot |
| 7. Tracking | Meta Pixel, CAPI, GA4, events | Full funnel tracking |
| 8. SEO | Meta tags, sitemap, schema, performance | Search-ready |
| 9. Launch | Final QA, mobile testing, go-live | picyourbooth.nl live |

---

## Out of Scope (v1)

- Blog / content pages
- Multi-language (English)
- User accounts / login
- Online payment / checkout
- Booking calendar integration
- Chat widget
- Custom CMS for content editing

These can be added in v2 based on traction and needs.
