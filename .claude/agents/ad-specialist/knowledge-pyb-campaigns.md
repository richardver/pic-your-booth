# PYB Campaign Architecture

PicYourBooth-specific campaign structure, segments, budgets, and targets.

---

## Meta Ads Account Structure

```
Pic Your Booth Ad Account
├── PROSPECTING - Magic Mirror XL (CBO, ~€8/day)
│   ├── Advantage+ Audience - broad, NL Randstad
│   ├── Lookalike 1% - past leads/customers
│   └── Interest: weddings, corporate events, party planning
├── PROSPECTING - Party Booth (CBO, ~€8/day)
│   ├── Advantage+ Audience - broad, NL Randstad
│   └── Interest: birthday parties, celebrations
├── RETARGETING (ABO, subset of above once pixel has data)
│   ├── Website visitors 1-7 days (excl. converters)
│   ├── Website visitors 8-30 days
│   ├── IG/FB engagers 30 days
│   └── Form openers who didn't submit
└── SEASONAL / PROMO (when applicable)
```

> **Note:** DJ + Photobooth Combo campagne niet in Fase 1. DJ is upgrade (+€149) in photobooth-campagnes.

## Google Ads Account Structure (Planned)

```
Pic Your Booth Google Ads
├── SEARCH - Magic Mirror XL
│   ├── Brand: "picyourbooth", "pic your booth"
│   ├── Generic: "photobooth huren", "fotobooth bruiloft"
│   └── Premium: "premium photobooth", "DSLR photobooth"
├── SEARCH - Party Booth
│   ├── Generic: "photobooth huren goedkoop", "fotobox huren"
│   └── Events: "photobooth verjaardag", "photobooth feest"
├── SEARCH - DJ Services
│   ├── Generic: "dj huren", "dj boeken"
│   └── Event-specific: "dj bruiloft", "dj feest huren"
├── SEARCH - Combo
│   └── "dj en photobooth huren", "entertainment bruiloft"
└── PMAX (when enough conversion data)
    └── Asset groups by segment
```

## Key Metrics & Targets

| Metric | Target | Action if missed |
|---|---|---|
| ROAS | >4.0x | Optimize funnel + creative + audiences |
| CTR (prospecting) | >1.0% | Refresh creative/hook |
| CPC | <€1.50 | Improve creative relevance |
| CPL (cost per lead) | <€25 | Optimize audiences + creative |
| Form conversion rate | >5% | Audit landing page (`/design-landingpage`) |
| Frequency (prospecting) | <3.0 | Expand audience or rotate creative |
| Google Search CTR | >5% | Improve ad copy relevance |
| Google Search CPC | <€2.00 | Improve Quality Score |

> Vizibooth 2025 reference data in `docs/kpi/`. Magic Mirror XL higher price (€599) = lower volume, higher AOV than Vizibooth.

## Segments & Messaging

| Segment | Product | Tone | Key Message | Price Anchor |
|---|---|---|---|---|
| Perfectionist Planner | Magic Mirror XL | Premium, trust | "DSLR kwaliteit, 5 uur inclusief" | Vanaf €599 |
| Budget Celebrator | Party Booth | Fun, easy | "Foto plezier voor elk feest" | Vanaf €199 |
| All-in-One Seeker | DJ + Combo | Energy, convenience | "Eén team, één vibe" | Vanaf €348 |
| Wedding Planners | Magic Mirror + DJ | Premium, personal | "Jullie dag, onze ervaring" | Vanaf €748 |

## Budget Allocation — Fase 1 (Photobooth Focus)

**Total monthly budget: €500 (Phase 1 test budget)**

**Fase 1 regel: 100% ad budget op photobooth verhuur. DJ is upgrade (+€149), geen aparte campagnes.**

**Approach A — Split Test:**

| Channel | Focus | Monthly Budget |
|---|---|---|
| Meta Ads - Magic Mirror XL | Prospecting, NL Randstad | €250 |
| Meta Ads - Party Booth | Prospecting, NL Randstad | €250 |

- **All Meta Ads** for now — Google Ads in Phase 2
- **Retargeting:** subset of above budgets once pixel has sufficient data (no separate budget)
- **ROAS target: >4.0x** (Vizibooth 2025 avg was 4.5x)

**DJ-boekingen in Fase 1:** komen via combo-upgrade op website en organisch social media. Geen apart DJ ad budget.

**Fase 2 (later):** Google Ads toevoegen, DJ-campagnes, "dj huren" search, PMax, retargeting schalen.

## Funnel: Ad → Conversion

```
Meta/Google Ad → Landing Page → Proposal Form → Proposal Email → Booking
```

Every ad must map to a landing page that passes the 3-second message match test.
Use `/design-landingpage` to build conversion-optimized pages for ad traffic.

Full funnel design: `docs/funnel/funnel-design.md`
