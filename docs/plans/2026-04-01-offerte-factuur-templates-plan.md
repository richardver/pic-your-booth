# Offerte & Factuur Templates — Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Build 4 branded HTML templates (3 proposals + 1 invoice) with PYB design system, merge field placeholders, and Playwright PDF export.

**Architecture:** Standalone HTML files with inline CSS using PYB design tokens. Each template uses `{{merge_field}}` placeholders matching HubSpot deal properties. Playwright exports each to A4 PDF. No build step, no framework — just HTML + CSS.

**Tech Stack:** HTML, CSS (PYB design tokens), Playwright (PDF export), Google Fonts (Bebas Neue + Space Grotesk)

**Design doc:** `docs/plans/2026-04-01-offerte-factuur-templates-design.md`

---

### Task 1: Create folder structure and shared CSS base

**Files:**
- Create: `docs/pyb/templates/offerte-party-booth.html`
- Create: `docs/pyb/templates/offerte-magic-mirror.html`
- Create: `docs/pyb/templates/offerte-dj.html`
- Create: `docs/pyb/templates/factuur.html`
- Create: `docs/offerte/.gitkeep`
- Create: `docs/factuur/.gitkeep`

**Step 1: Create output directories**

```bash
mkdir -p docs/pyb/templates
mkdir -p docs/offerte/2026
mkdir -p docs/factuur/2026
touch docs/offerte/.gitkeep
touch docs/factuur/.gitkeep
```

**Step 2: Commit**

```bash
git add docs/pyb/templates docs/offerte docs/factuur
git commit -m "chore: create offerte/factuur template and output folders"
```

---

### Task 2: Build the invoice template (factuur.html)

Start with the simplest template — 1 page, straightforward structure. This establishes the shared CSS pattern that proposals will extend.

**Files:**
- Create: `docs/pyb/templates/factuur.html`

**Step 1: Build the invoice HTML**

The template must be A4-sized (210mm x 297mm) for PDF export. All CSS is inline. Uses PYB design tokens: dark background (#08080b), gold accent (#f59e42), Space Grotesk + Bebas Neue fonts.

```html
<!DOCTYPE html>
<html lang="nl">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Factuur — PicYourBooth B.V.</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Space+Grotesk:wght@300;400;500;600;700&display=swap" rel="stylesheet">
  <style>
    /* --- Design tokens --- */
    :root {
      --bg: #08080b;
      --surface: #111116;
      --surface-up: #18181e;
      --text: #ededf0;
      --text-muted: rgba(237,237,240,0.60);
      --gold: #f59e42;
      --gold-light: #ffb86b;
      --border: rgba(255,255,255,0.06);
      --font-display: 'Bebas Neue', sans-serif;
      --font-body: 'Space Grotesk', sans-serif;
    }

    /* --- Reset --- */
    * { box-sizing: border-box; margin: 0; padding: 0; }

    /* --- Page setup (A4) --- */
    @page { size: A4; margin: 0; }
    body {
      width: 210mm;
      min-height: 297mm;
      margin: 0 auto;
      padding: 40px 48px;
      background: var(--bg);
      color: var(--text);
      font-family: var(--font-body);
      font-size: 14px;
      line-height: 1.5;
      -webkit-print-color-adjust: exact;
      print-color-adjust: exact;
    }

    /* --- Logo --- */
    .logo { height: 48px; margin-bottom: 40px; }

    /* --- Header section --- */
    .invoice-header { margin-bottom: 32px; }
    .invoice-title {
      font-family: var(--font-display);
      font-size: 36px;
      letter-spacing: 1px;
      color: var(--gold);
      text-transform: uppercase;
      margin-bottom: 8px;
    }
    .invoice-meta {
      display: flex;
      gap: 32px;
      color: var(--text-muted);
      font-size: 13px;
    }
    .invoice-meta strong { color: var(--text); }

    /* --- Client block --- */
    .client-block {
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 20px 24px;
      margin-bottom: 32px;
    }
    .client-block h3 {
      font-family: var(--font-display);
      font-size: 18px;
      letter-spacing: 0.5px;
      text-transform: uppercase;
      color: var(--gold);
      margin-bottom: 12px;
    }
    .client-row {
      display: flex;
      justify-content: space-between;
      padding: 6px 0;
      border-bottom: 1px solid var(--border);
    }
    .client-row:last-child { border-bottom: none; }
    .client-label { color: var(--text-muted); }

    /* --- Table --- */
    .line-items {
      width: 100%;
      border-collapse: collapse;
      margin-bottom: 24px;
    }
    .line-items th {
      font-family: var(--font-display);
      font-size: 14px;
      letter-spacing: 0.5px;
      text-transform: uppercase;
      color: var(--gold);
      text-align: left;
      padding: 12px 16px;
      border-bottom: 2px solid var(--gold);
    }
    .line-items th:last-child,
    .line-items td:last-child { text-align: right; }
    .line-items td {
      padding: 12px 16px;
      border-bottom: 1px solid var(--border);
    }

    /* --- Totals --- */
    .totals {
      margin-left: auto;
      width: 280px;
      margin-bottom: 40px;
    }
    .totals-row {
      display: flex;
      justify-content: space-between;
      padding: 8px 0;
      border-bottom: 1px solid var(--border);
    }
    .totals-row.total {
      border-bottom: none;
      border-top: 2px solid var(--gold);
      padding-top: 12px;
      margin-top: 4px;
      font-weight: 700;
      font-size: 18px;
    }
    .totals-row.total .amount { color: var(--gold); }

    /* --- Payment block --- */
    .payment-block {
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 20px 24px;
      margin-bottom: 40px;
    }
    .payment-block h3 {
      font-family: var(--font-display);
      font-size: 18px;
      letter-spacing: 0.5px;
      text-transform: uppercase;
      color: var(--gold);
      margin-bottom: 12px;
    }
    .payment-detail {
      display: flex;
      gap: 12px;
      padding: 4px 0;
      font-size: 13px;
    }
    .payment-detail .label { color: var(--text-muted); min-width: 120px; }

    /* --- Footer --- */
    .footer {
      position: absolute;
      bottom: 32px;
      left: 48px;
      right: 48px;
      text-align: center;
      font-size: 11px;
      color: var(--text-muted);
      border-top: 1px solid var(--border);
      padding-top: 16px;
    }
  </style>
</head>
<body>
  <!-- Logo -->
  <img src="../../../images/pyb/logo/logo-navbar-transparent.png" alt="PicYourBooth" class="logo">

  <!-- Invoice header -->
  <div class="invoice-header">
    <div class="invoice-title">Factuur</div>
    <div class="invoice-meta">
      <div><strong>Factuurdatum:</strong> {{factuurdatum}}</div>
      <div><strong>Factuurnummer:</strong> {{factuurnummer}}</div>
    </div>
    <div class="invoice-meta" style="margin-top: 4px;">
      <div><strong>Betreft:</strong> {{betreft}}</div>
    </div>
  </div>

  <!-- Client details -->
  <div class="client-block">
    <h3>Klant</h3>
    <div class="client-row">
      <span class="client-label">Naam</span>
      <span>{{klant_naam}}</span>
    </div>
    <!-- Show company row only if B2B -->
    <div class="client-row" style="{{klant_bedrijf_display}}">
      <span class="client-label">Bedrijf</span>
      <span>{{klant_bedrijf}}</span>
    </div>
    <div class="client-row">
      <span class="client-label">E-mail</span>
      <span>{{email}}</span>
    </div>
  </div>

  <!-- Line items -->
  <table class="line-items">
    <thead>
      <tr>
        <th>Omschrijving</th>
        <th>Bedrag</th>
      </tr>
    </thead>
    <tbody>
      <!-- Repeat for each line item -->
      <tr>
        <td>{{line_item_1_omschrijving}}</td>
        <td>€ {{line_item_1_bedrag}}</td>
      </tr>
      <tr>
        <td>{{line_item_2_omschrijving}}</td>
        <td>€ {{line_item_2_bedrag}}</td>
      </tr>
      <!-- Add/remove rows as needed per invoice -->
    </tbody>
  </table>

  <!-- Totals -->
  <div class="totals">
    <div class="totals-row">
      <span>Subtotaal</span>
      <span class="amount">€ {{subtotaal}}</span>
    </div>
    <div class="totals-row">
      <span>BTW 21%</span>
      <span class="amount">€ {{btw}}</span>
    </div>
    <div class="totals-row total">
      <span>Totaal</span>
      <span class="amount">€ {{totaal}}</span>
    </div>
  </div>

  <!-- Payment info -->
  <div class="payment-block">
    <h3>Betalingsinformatie</h3>
    <p style="margin-bottom: 12px;">Gelieve het totaalbedrag van <strong style="color: var(--gold);">€ {{totaal}}</strong> binnen 30 dagen over te maken naar onderstaand rekeningnummer o.v.v. <strong>{{factuurnummer}}</strong></p>
    <div class="payment-detail">
      <span class="label">Bank</span>
      <span>Rabobank</span>
    </div>
    <div class="payment-detail">
      <span class="label">IBAN</span>
      <span>NL22 RABO 0142 1467 57</span>
    </div>
    <div class="payment-detail">
      <span class="label">Ten name van</span>
      <span>PicYourBooth B.V.</span>
    </div>
  </div>

  <!-- Footer -->
  <div class="footer">
    Koekoekzoom 35 · 2643 KP · Pijnacker · KvK: 59400080 · BTW: NL853461776B01
  </div>
</body>
</html>
```

**Step 2: Open in browser to verify layout**

```bash
open docs/pyb/templates/factuur.html
```

Verify: dark background, gold accents, PYB logo loads, A4 proportions look correct, merge field placeholders visible.

**Step 3: Export test PDF via Playwright**

Save this as `/tmp/export-factuur.mjs`:

```javascript
import { chromium } from 'playwright';

const browser = await chromium.launch();
const page = await browser.newPage();

await page.goto('file:///Users/richardversluis/code/pic-your-booth/docs/pyb/templates/factuur.html', {
  waitUntil: 'networkidle'
});
await page.waitForTimeout(2000);

await page.pdf({
  path: '/Users/richardversluis/code/pic-your-booth/docs/factuur/2026/Factuur-PYB-2026-TEST.pdf',
  format: 'A4',
  printBackground: true,
  margin: { top: '0', right: '0', bottom: '0', left: '0' }
});

await browser.close();
console.log('PDF exported successfully');
```

```bash
cd /tmp && node export-factuur.mjs
open /Users/richardversluis/code/pic-your-booth/docs/factuur/2026/Factuur-PYB-2026-TEST.pdf
```

Verify PDF looks correct: dark background preserved, fonts rendered, layout fits A4.

**Step 4: Commit**

```bash
git add docs/pyb/templates/factuur.html
git commit -m "feat: add branded invoice (factuur) HTML template with PYB design system"
```

---

### Task 3: Build Magic Mirror XL proposal template (offerte-magic-mirror.html)

Start with the premium product — it has the most content and sets the pattern for other proposals.

**Files:**
- Create: `docs/pyb/templates/offerte-magic-mirror.html`

**Step 1: Build the 3-page proposal HTML**

Uses same design tokens as invoice. Three pages achieved via CSS `page-break-after: always`. Each page is A4 sized.

**Page 1 — Cover + Pricing:**
- PYB logo
- "OFFERTE" title in Bebas Neue gold
- Client details block (naam, email)
- Event details block (datum, locatie, begintijd)
- Pricing table:
  - Magic Mirror XL — 5 uur — € 599
  - Extra opties — € {{evenement_extraopties}}
  - Reiskosten — € {{evenement_reiskosten}}
  - Totaal incl. BTW 21% — € {{deal_value}}
- Scarcity hook: gift badge for fotogalerij cadeau

**Page 2 — Product Showcase + Upgrades:**
- Product photo (use `images/web/` Magic Mirror photo or placeholder)
- "Wat zit erin" list:
  - Magic Mirror XL Photobooth met interactief touchscreen
  - Professionele DSLR camera + studiobelichting
  - Fotostrip ontwerp in overleg
  - Onbeperkt printen gedurende event
  - Snelle printer — twee fotostrips in 13 seconden
  - Levering, installatie en test door ons team
  - 5 uur all-in
  - Reiskosten inclusief tot 50 km vanaf 2643 KP
- Social proof badge: "237+ events · 5-star rating"
- Upgrades table:
  - VIP Upgrade — +€ 149 — Aanbevolen badge
  - Wedding Keychain Station — +€ 499
  - Photobooth Host — +€ 149
  - AI Photo Experience — +€ 499
  - Live DJ Set — +€ 149

**Page 3 — Why PYB + Confirmation:**
- "Waarom PicYourBooth?" heading
- USP copy (adapted from existing: DSLR quality, studio lighting, professional team, hassle-free)
- Confirmation section:
  - "Bevestig je boeking" heading
  - Reply "AKKOORD" instruction
  - WhatsApp option
  - Payment terms: contant bij aankomst of vooraf per bank (24 uur voor event)
  - Algemene voorwaarden mention
  - Photo usage opt-out notice
- Signed: "Met feestelijke groet, Richard — PicYourBooth"
- Footer: company details

The full HTML will follow the same `<style>` pattern as the invoice, extended with page-break rules and additional component styles for the product showcase, upgrade table, and confirmation section.

Key CSS additions over invoice:
```css
.page { 
  width: 210mm; 
  min-height: 297mm; 
  padding: 40px 48px; 
  position: relative; 
  page-break-after: always; 
}
.page:last-child { page-break-after: avoid; }

/* Product showcase */
.product-card { 
  display: flex; 
  gap: 24px; 
  background: var(--surface); 
  border-radius: 12px; 
  padding: 24px; 
  margin-bottom: 32px; 
}
.product-image { 
  width: 200px; 
  height: 260px; 
  object-fit: cover; 
  border-radius: 8px; 
}

/* Upgrades */
.upgrade-row { 
  display: flex; 
  justify-content: space-between; 
  align-items: center; 
  padding: 12px 16px; 
  border-bottom: 1px solid var(--border); 
}
.upgrade-badge { 
  background: var(--gold); 
  color: var(--bg); 
  font-size: 11px; 
  font-weight: 600; 
  padding: 2px 8px; 
  border-radius: 4px; 
  text-transform: uppercase; 
}

/* Confirmation CTA */
.cta-block { 
  background: var(--surface); 
  border: 2px solid var(--gold); 
  border-radius: 12px; 
  padding: 24px; 
  text-align: center; 
  margin: 32px 0; 
}
.cta-akkoord { 
  display: inline-block; 
  background: var(--gold); 
  color: var(--bg); 
  font-family: var(--font-display); 
  font-size: 24px; 
  padding: 12px 48px; 
  border-radius: 8px; 
  letter-spacing: 1px; 
}
```

**Step 2: Open in browser and verify all 3 pages**

```bash
open docs/pyb/templates/offerte-magic-mirror.html
```

Verify: 3 pages visible when scrolling, correct content on each page, dark theme, gold accents, merge fields visible.

**Step 3: Export test PDF**

Save as `/tmp/export-offerte-mm.mjs`:

```javascript
import { chromium } from 'playwright';

const browser = await chromium.launch();
const page = await browser.newPage();

await page.goto('file:///Users/richardversluis/code/pic-your-booth/docs/pyb/templates/offerte-magic-mirror.html', {
  waitUntil: 'networkidle'
});
await page.waitForTimeout(2000);

await page.pdf({
  path: '/Users/richardversluis/code/pic-your-booth/docs/offerte/2026/Offerte-Magic-Mirror-XL-TEST.pdf',
  format: 'A4',
  printBackground: true,
  margin: { top: '0', right: '0', bottom: '0', left: '0' }
});

await browser.close();
console.log('PDF exported successfully');
```

```bash
cd /tmp && node export-offerte-mm.mjs
open /Users/richardversluis/code/pic-your-booth/docs/offerte/2026/Offerte-Magic-Mirror-XL-TEST.pdf
```

Verify: 3-page PDF, dark backgrounds preserved, fonts correct, page breaks clean.

**Step 4: Commit**

```bash
git add docs/pyb/templates/offerte-magic-mirror.html
git commit -m "feat: add Magic Mirror XL branded proposal template (3-page)"
```

---

### Task 4: Build Party Booth proposal template (offerte-party-booth.html)

**Files:**
- Create: `docs/pyb/templates/offerte-party-booth.html`

**Step 1: Build the 3-page proposal HTML**

Copy the Magic Mirror template structure, then adapt:

**Page 1 differences:**
- Service name: "Party Booth" (not Magic Mirror XL)
- Base price: € 199
- No "begintijd" — Party Booth is self-service pickup
- Add "Huur periode: Dag van event, retour volgende dag voor 13:00"

**Page 2 differences:**
- Product photo: Party Booth image
- "Wat zit erin" list:
  - Party Booth met touchscreen
  - Digitale foto's direct delen via QR, AirDrop, WhatsApp
  - Standaard fotostrip design (tekst aanpasbaar)
  - Compact & stijlvol design
  - Binnen 5 minuten klaar
  - Geen printer nodig, geen internet nodig
- Upgrades table:
  - Premium Fotostrip Design — +€ 25
  - Bezorging, Installatie & Ophalen — +€ 49
  - AI Foto's + Filters — +€ 49
  - Live DJ Set — +€ 149

**Page 3:** Same structure as Magic Mirror but with Party Booth specific USP copy (fun, simple, affordable, no hassle).

**Step 2: Open in browser and verify**

```bash
open docs/pyb/templates/offerte-party-booth.html
```

**Step 3: Export test PDF**

Same pattern as Task 3, output to `docs/offerte/2026/Offerte-Party-Booth-TEST.pdf`

**Step 4: Commit**

```bash
git add docs/pyb/templates/offerte-party-booth.html
git commit -m "feat: add Party Booth branded proposal template (3-page)"
```

---

### Task 5: Build DJ proposal template (offerte-dj.html)

**Files:**
- Create: `docs/pyb/templates/offerte-dj.html`

**Step 1: Build the 3-page proposal HTML**

Copy the proposal structure, adapt for DJ service:

**Page 1 differences:**
- Service name: "DJ {{dj_naam}}" (DJ Gianni or Milø)
- Base price: € 149 (3 uur)
- Event details: datum, locatie, begintijd
- Extra uur lines if applicable

**Page 2 differences:**
- DJ profile photo (use merge field for DJ-specific image)
- "Wat zit erin" list:
  - Professionele DJ set (3 uur)
  - Pioneer DJ apparatuur
  - Spotify playlist optimalisatie vooraf
  - Lichtshow basispakket
  - Op- en afbouw door DJ
- DJ-specific accent color: use `{{dj_accent}}` — coral (#f0654a) for Gianni, cyan (#34d399) for Milø
- Upgrades:
  - Extra uur — +€ 49 per uur (max 3 extra)

**Page 3:** Same confirmation structure, DJ-specific USP copy.

**Step 2: Open in browser and verify**

```bash
open docs/pyb/templates/offerte-dj.html
```

**Step 3: Export test PDF**

Output to `docs/offerte/2026/Offerte-DJ-TEST.pdf`

**Step 4: Commit**

```bash
git add docs/pyb/templates/offerte-dj.html
git commit -m "feat: add DJ branded proposal template (3-page)"
```

---

### Task 6: Visual review and polish all 4 templates

**Step 1: Export all 4 PDFs**

Create a single export script `/tmp/export-all.mjs` that exports all templates.

```bash
cd /tmp && node export-all.mjs
```

**Step 2: Review each PDF side by side**

Open all 4 PDFs and check:
- [ ] PYB logo renders correctly
- [ ] Dark background preserved in PDF
- [ ] Gold accents consistent across all templates
- [ ] Fonts render (Bebas Neue for headings, Space Grotesk for body)
- [ ] Page breaks are clean (no content cut off)
- [ ] Pricing tables aligned
- [ ] Footer company details correct on all pages
- [ ] Merge field placeholders clearly visible
- [ ] A4 proportions correct

**Step 3: Fix any issues found**

**Step 4: Delete test PDFs from output folders**

```bash
rm docs/offerte/2026/*TEST*.pdf
rm docs/factuur/2026/*TEST*.pdf
```

**Step 5: Commit any polish changes**

```bash
git add docs/pyb/templates/
git commit -m "fix: polish offerte/factuur templates after visual review"
```

---

### Task 7: Commit design doc and plan

**Step 1: Stage and commit**

```bash
git add docs/plans/2026-04-01-offerte-factuur-templates-design.md
git add docs/plans/2026-04-01-offerte-factuur-templates-plan.md
git commit -m "docs: add offerte/factuur templates design doc and implementation plan"
```
