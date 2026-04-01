# Offerte & Factuur Templates — Design Document

**Date:** 2026-04-01
**Status:** Approved
**Owner:** Richard

## Problem

PYB has no branded proposal or invoice system. Current templates use old branding (Visualize Events, Vizibooth, Pic Your Moment), outdated product names, KOR disclaimer (no longer applies), and plain design that doesn't match the PYB website.

## Solution

HTML templates in this repo, styled with PYB design system, exported to PDF via Playwright. HubSpot deal data fills merge fields. Future: n8n automation triggers generation on deal stage changes.

## Templates

| Template | Trigger | Pages |
|---|---|---|
| `offerte-party-booth.html` | Deal → "Offerte", service = Party Booth | 3 |
| `offerte-magic-mirror.html` | Deal → "Offerte", service = Magic Mirror XL | 3 |
| `offerte-dj.html` | Deal → "Offerte", service = DJ | 3 |
| `factuur.html` | Deal → "Akkoord" | 1 |

## File Structure

```
docs/pyb/templates/           ← HTML templates (source)
  offerte-party-booth.html
  offerte-magic-mirror.html
  offerte-dj.html
  factuur.html

docs/offerte/2026/             ← Generated proposal PDFs
  Offerte-Magic-Mirror-XL-Lisa-de-Vries-2026-06-15.pdf

docs/factuur/2026/             ← Generated invoice PDFs
  Factuur-PYB-2026-001.pdf
```

## Proposal Structure (3 pages per template)

### Page 1: Cover + Pricing
- PYB logo header
- Offerte date + reference
- Client details: naam, email
- Event details: datum, locatie, begintijd
- Service line item with base price
- Extra opties, reiskosten, korting
- Totaal incl. BTW 21%
- Scarcity hook: "cadeau" framing for fotogalerij

### Page 2: Product Showcase + Upgrades
- Product hero photo
- What's included list (service-specific)
- Social proof badge (237+ events, 5-star rating)
- Available upgrades with prices and checkboxes
- Reiskosten policy

### Page 3: Why PYB + Confirmation
- USP section: why PYB over competitors
- Easy confirmation: reply "AKKOORD" + WhatsApp option
- Payment terms: contant bij aankomst or vooraf per bank (24 uur)
- Algemene voorwaarden link
- Photo usage opt-out notice
- Signed by Richard, PicYourBooth

## Invoice Structure (1 page)

- PYB logo header
- Client: naam + bedrijfsnaam (if B2B, otherwise hidden)
- Client email
- Factuurdatum, factuurnummer (PYB-2026-XXX), betreft
- Line items: omschrijving, bedrag, totaal
- Subtotaal, BTW 21%, Totaal incl. BTW
- Betalingsinformatie:
  - 30 dagen termijn
  - IBAN: NL22RABO0142146757
  - t.n.v. PicYourBooth B.V.
  - o.v.v. factuurnummer
- Footer: Koekoekzoom 35, 2643 KP, Pijnacker, KvK: 59400080, BTW: 8534.61.776.B.01

## Merge Fields

### Proposal fields
- `{{dealdate}}` — offerte date
- `{{lastname}}` — client name
- `{{email}}` — client email
- `{{evenement_datum}}` — event date
- `{{evenement_locatie}}` — event location
- `{{evenement_startijd}}` — event start time
- `{{evenement_extraopties}}` — extra options total
- `{{evenement_reiskosten}}` — travel costs
- `{{deal_value}}` — total amount

### Invoice fields
- `{{klant_naam}}` — client name
- `{{klant_bedrijf}}` — company name (optional, hidden if empty)
- `{{email}}` — client email
- `{{factuurdatum}}` — invoice date
- `{{factuurnummer}}` — sequential: PYB-2026-XXX
- `{{betreft}}` — description (e.g. "Magic Mirror XL - Bruiloft 15 juni 2026")
- `{{line_items}}` — array of {omschrijving, bedrag, totaal}
- `{{subtotaal}}` — subtotal ex BTW
- `{{btw}}` — 21% BTW amount
- `{{totaal}}` — total incl. BTW

## Visual Design

- Dark background (#0a0a0a), white text
- Gold accent (#c8a855) for CTAs, totals, highlights
- PYB logo top-left
- Space Grotesk typography
- Product-specific hero photo on page 2
- Clean tables with subtle borders

## Conversion Tactics

| Tactic | Location | Implementation |
|---|---|---|
| Scarcity | Page 1 | "Populaire datums gaan snel" near total |
| Gift framing | Page 1 | Fotogalerij "cadeau" this month (keep existing pattern) |
| Social proof | Page 2 | "237+ events" badge, Google/Trustpilot stars |
| Anchoring | Price table | Base price first, upgrades as small add-ons |
| Urgency | Page 3 | "Bevestig binnen 7 dagen" |
| Risk removal | Page 3 | "100% vrijblijvend" |
| Easy CTA | Page 3 | Reply "AKKOORD" + WhatsApp option |

## Key Copy Updates from Old Templates

- Brand: Visualize Events / Vizibooth → PicYourBooth
- Products: "iPad Digitaal" → Party Booth, "Magische Spiegel" → Magic Mirror XL
- Tax: KOR disclaimer removed → BTW 21% included
- Company: PicYourBooth B.V. (KvK 59400080)
- Sender: Toesjka → Richard
- Pricing: charm pricing (€ 199, € 599, € 149)
- Legal entity: PicYourBooth B.V. on invoices only

## Automation Flow (future)

### Offerte
1. Richard reviews lead → moves Deal to "Offerte" in HubSpot
2. n8n detects stage change → fetches deal data via HubSpot API
3. Picks template based on `service_type` property
4. Fills HTML template with merge data
5. Playwright exports to PDF
6. Saves to `docs/offerte/2026/`
7. Emails PDF to client, notifies Richard

### Factuur
1. Deal moves to "Akkoord" in HubSpot
2. n8n detects stage change → fetches deal data
3. Auto-increments factuurnummer (PYB-2026-XXX)
4. Fills invoice template with deal data
5. Playwright exports to PDF
6. Saves to `docs/factuur/2026/`
7. Emails PDF to client + accountant

**Phase 1 (now):** Build the 4 HTML templates with merge field placeholders. Manual fill via script.
**Phase 2 (later):** Wire n8n automation to HubSpot pipeline stages.
