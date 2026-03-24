# PicYourBooth Funnel Design

## Overview

Full-funnel advertising strategy for PicYourBooth photobooth rentals. Split-test approach across Magic Mirror XL and Party Booth with €500/month budget.

## Funnel Flow

```
Meta Ad → Website Landing Page → Proposal Form → HubSpot Lead → Proposal Email → Booking
```

### Landing Pages (= existing website pages)
- Magic Mirror XL ads → `magic-mirror.html`
- Party Booth ads → `party-booth.html`
- Message match: ad headline must echo landing page headline

---

## Budget & Campaign Structure

**Total budget:** €500/month
**Split:** €250 Magic Mirror XL + €250 Party Booth
**Daily budget:** ~€8/day per product

### Campaign 1: PROSPECTING — Magic Mirror XL (CBO, €250/month)

| Ad Set | Audience | Hook Focus |
|--------|----------|------------|
| MM-A | Advantage+ (broad, Randstad) | DSLR kwaliteit + 5 uur inclusief |
| MM-B | Interest: weddings, corporate events | VIP ervaring + direct printen |

### Campaign 2: PROSPECTING — Party Booth (CBO, €250/month)

| Ad Set | Audience | Hook Focus |
|--------|----------|------------|
| PB-A | Advantage+ (broad, Randstad) | Vanaf €199, elk feest |
| PB-B | Interest: birthday, celebrations | Zelf opzetten, direct delen |

### Future: RETARGETING (Phase 2, after enough pixel data)
- Website visitors 1-7 days (excl. converters)
- Website visitors 8-30 days
- IG/FB engagers 30 days
- Form openers who didn't submit
- Budget: reallocate 15-20% from prospecting once pixel has 1000+ events

---

## Testing Framework

### Phase 1: Test (Week 1-2)
- Run all 4 ad sets with equal budget
- Each ad set gets 2-3 creative variants (different hooks)
- Monitor daily: CTR, CPC, CPL

### Phase 2: Optimize (Week 3-4)
- Kill ad sets with CPL > €30 or CTR < 0.6%
- Move budget to winning ad sets
- If one product clearly wins, shift to 70/30 split

### What We're Testing

| Variable | Options | How We Measure |
|----------|---------|----------------|
| Product | Magic Mirror XL vs Party Booth | CPL, conversion rate |
| Hook | USP-focused vs scarcity vs social proof | CTR, engagement |
| Audience | Advantage+ vs Interest-based | CPC, CPL |
| Creative | Real photos vs AI-enhanced | CTR, conversion rate |

### USP + Hook Test Matrix

**Magic Mirror XL hooks to test:**
1. "Dit is geen photobooth — dit is een ervaring" (experience)
2. "DSLR camera, professionele belichting, direct printen — vanaf €599" (specs + price)
3. "5 uur inclusief. Geen haast. Eén prijs per event." (value)
4. "Waarom 200+ bruidsparen kozen voor een DSLR photobooth" (social proof, wedding)

**Party Booth hooks to test:**
1. "Fotoplezier voor elk feest — vanaf €199" (price)
2. "In 5 minuten opgezet, de hele avond plezier" (ease)
3. "Geen monteur nodig, geen gedoe — gewoon feesten" (convenience)
4. "Leuke foto's, klein budget — Party Booth vanaf €199" (budget-friendly)

---

## Historical Performance (Vizibooth 2025-2026)

Reference data from previous brand. Source: `docs/kpi/__KPI Rapport 2025.xlsx` and `2026.xlsx`.

### 2025 Monthly Performance

| Maand | Forms | FB Ads | Google Ads | Total Spend | Revenue | ROAS |
|-------|-------|--------|------------|-------------|-------|------|
| Jan | 26 | — | — | €0 | €0 | — |
| Feb | 21 | — | — | €0 | €329 | — |
| Mrt | 30 | — | — | €0 | €2,930 | — |
| Apr | 21 | — | — | €500 | €1,977 | 3.95x |
| Mei | 6 | — | — | €715 | €4,653 | 6.51x |
| Jun | 20 | €200 | €92 | €292 | €1,960 | 6.71x |
| Jul | 40 | €465 | €72 | €537 | €3,510 | 6.54x |
| Aug | 40 | €500 | €75 | €575 | €3,392 | 3.98x |
| Sep | 47 | €530 | €65 | €595 | €4,400 | 4.88x |
| Okt | 62 | €700 | €75 | €775 | €5,500 | 4.58x |
| Nov | 57 | €700 | €75 | €775 | €3,770 | 2.99x |
| Dec | 32 | €503 | €0 | €503 | €1,900 | 2.36x |

**2025 totals:** 402 forms, €4,767 ad spend, €34,321 revenue, avg ROAS 4.5x

### 2026 Performance (so far)

| Maand | Forms | FB Conv | FB Ads | Google Ads | Total Spend | Revenue | ROAS |
|-------|-------|---------|--------|------------|-------------|-------|------|
| Jan | 72 | 55 | €620 | €0 | €620 | €2,470 | 3.04x |

### Key Insights from Historical Data
- **Best ROAS months:** Jun-Jul 2025 (6.5x) — wedding season, lower competition
- **Peak lead volume:** Okt 2025 (62 forms) — corporate event season
- **ROAS floor:** Dec 2025 (2.36x) — seasonal low, still profitable
- **Avg CPL 2025:** ~€12 (€4,767 / 402 forms) — well below €25 target
- **Avg order value:** ~€85 per form (€34,321 / 402) — note: not all forms convert to bookings
- **2026 Jan shows strong start:** 72 forms (+177% vs Jan 2025), ROAS 3.04x

### Important: PYB vs Vizibooth Volume Expectations
Vizibooth operated at a lower price point. PicYourBooth's Magic Mirror XL (€599) is significantly higher than Vizibooth's products. This means:
- **Lower lead volume expected** — fewer people convert at premium price points
- **Higher AOV** — each booking is worth more, so fewer leads needed for same revenue
- **CPL will likely be higher** — premium products naturally attract fewer but more qualified leads
- **ROAS may differ** — fewer conversions but higher revenue per conversion
- Party Booth (€199) is closer to Vizibooth pricing, so volume should be comparable
- Use Vizibooth data as directional benchmark, not a direct target

---

## KPI Targets (PicYourBooth)

### Ad Performance Metrics

| Metric | Target | Kill Threshold | Vizibooth Benchmark |
|--------|--------|----------------|---------------------|
| CTR (prospecting) | > 1.0% | < 0.6% | — |
| CPC | < €1.50 | > €2.50 | — |
| CPL (cost per lead) | < €25 | > €35 | ~€12 avg |
| Form conversion rate | > 5% | < 2% | — |
| Frequency (prospecting) | < 3.0 | > 4.0 | — |
| **ROAS** | **> 4.0x** | **< 2.0x** | **4.5x avg** |

### Revenue & Funnel Metrics

| Metric | Target | How to Calculate |
|--------|--------|------------------|
| ROAS | > 4.0x | Revenue from ad leads / Ad spend |
| AOV (avg order value) | Track | Total revenue / Number of bookings |
| Lead-to-proposal rate | > 60% | Proposals sent / Form submissions |
| Proposal-to-booking rate | > 30% | Bookings / Proposals sent |
| Lead-to-booking rate | > 20% | Bookings / Form submissions |
| Revenue per lead | Track | Total revenue / Total leads |
| Customer acquisition cost | < €50 | Ad spend / Bookings |
| Lifetime value | Track | Avg booking value + repeat + referral |

### Monthly Targets (€500 budget)
- Impressions: ~30,000-60,000
- Clicks: ~300-600
- Leads: ~15-25
- ROAS: > 4.0x (based on Vizibooth avg)
- Revenue target: > €2,000 (4x ad spend)

---

## Tracking & Pixel Setup

### Meta Pixel Events
| Event | Trigger | Page |
|-------|---------|------|
| PageView | All pages | * |
| ViewContent | Product page view | magic-mirror.html, party-booth.html |
| Lead | Form submission | offerte.html (thank you state) |
| InitiateCheckout | Form opened/started | offerte.html (form focus) |

### HubSpot Integration
- Form submissions → HubSpot contacts
- Hidden fields: utm_source, utm_medium, utm_campaign, utm_content
- Deal pipeline: Lead → Proposal Sent → Booked → Completed
- Lead source tracking: Meta Ads / Google Ads / Organic / Direct

### Website Requirements (before launch)
- [ ] Meta Pixel base code on all pages
- [ ] Conversions API (server-side) via n8n or direct
- [ ] UTM parameter capture in proposal form
- [ ] HubSpot form embed or API integration
- [ ] Thank you page/state for conversion tracking
- [ ] Google Analytics 4 setup

---

## n8n Automations

### 1. Daily KPI Monitor
**Trigger:** Daily at 09:00
**Flow:** Meta Ads API → check KPIs → alert if thresholds breached
**Alert conditions:**
- CPL > €25 (warning) or > €35 (critical)
- CTR drops below 0.8%
- Frequency > 3.0 on any ad set
- Daily spend anomaly (> 150% of target)
**Output:** Slack/email notification with dashboard link

### 2. Weekly Performance Report
**Trigger:** Monday 09:00
**Flow:** Meta Ads API → aggregate week data → format report → send
**Report includes:**
- Spend vs budget
- CPL, CTR, CPC per ad set
- Winner/loser ranking
- Recommendation: scale/pause/refresh

### 3. Lead Notification
**Trigger:** New form submission (webhook)
**Flow:** Website form → n8n → HubSpot contact create → Slack notification → email to Richard
**Data:** Name, event type, date, package interest, source

### 4. Creative Fatigue Alert
**Trigger:** Daily check
**Flow:** Meta Ads API → check frequency + CTR trend → alert if fatigued
**Conditions:**
- Frequency > 3.0 AND CTR declined 20% from baseline
- Any ad set with 0 conversions in 5+ days

### 5. Auto-Pause Underperformers (Phase 2)
**Trigger:** After 7 days of data
**Flow:** Meta Ads API → evaluate ad set performance → pause if below threshold
**Rules:** Only pause if ad set has 1000+ impressions and CPL > 2x target

---

## Creative Strategy

### Photo Assets Available
- **Magic Mirror XL:** 71 source photos (photobooth, VIP, USPs, upgrades)
- **Party Booth:** 9 source photos (product, upgrades)
- **DJ:** 5 photos (Gianni, Milo)

### Creative Types to Test
1. **Single image** — hero product shot with text overlay
2. **Carousel** — USP walkthrough (3-5 slides)
3. **Before/after** — AI photo experience showcase
4. **Social proof** — event photos with testimonial overlay

### Creative Production Process
1. Select best source photos per product
2. AI-enhance (lighting, background, branding)
3. Design ad mockup in HTML (using Meta Ads design system)
4. Export as image assets
5. A/B test in campaign

### Creative Refresh Cadence
- Week 1-2: initial creatives
- Week 3-4: refresh underperformers with new hooks
- Monthly: full creative audit + new batch

---

## Competitive Research

### To-Do: Gather Competitor Ad Intelligence
- [ ] Check Meta Ad Library for NL photobooth competitors
- [ ] Document winning ad formats (video vs image vs carousel)
- [ ] Note which hooks competitors use
- [ ] Identify gaps PYB can exploit (DSLR, 5 uur, combo)
- [ ] Richard shares Vizibooth historical campaign data

---

## Optimization Playbook

### Weekly Checklist
- [ ] Check CPL per ad set — pause if > €35 after 1000 impressions
- [ ] Check frequency — refresh creative if > 3.0
- [ ] Check CTR trend — flag if declining 3 consecutive days
- [ ] Reallocate budget from losers to winners
- [ ] Review HubSpot pipeline — are leads converting to proposals?

### Monthly Review
- [ ] Total spend vs leads vs bookings
- [ ] Calculate actual ROI (bookings revenue / ad spend)
- [ ] Decide budget for next month (increase winners, test new)
- [ ] Refresh all creatives
- [ ] Update hooks based on what worked

### Scaling Rules
- Never increase budget > 20% per 3-5 days
- Only scale ad sets with CPL < target for 7+ consecutive days
- When scaling, duplicate winning ad set rather than increasing budget

---

## Timeline

| Week | Action | Owner |
|------|--------|-------|
| Pre-launch | Deploy website + pixel + HubSpot | Richard + Claude |
| Pre-launch | Richard shares Vizibooth data | Richard |
| Pre-launch | Design ad creatives (HTML mockups) | Claude |
| Pre-launch | Set up n8n automations | Richard + Claude |
| Week 1 | Launch 4 ad sets, monitor daily | Richard |
| Week 2 | First optimization pass, kill losers | Richard + Claude |
| Week 3-4 | Scale winners, refresh creatives | Richard + Claude |
| Month end | Full review, plan next month | Richard + Claude |
