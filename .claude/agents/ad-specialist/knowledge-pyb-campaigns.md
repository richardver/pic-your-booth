# PYB Campaign Architecture

PicYourBooth-specific campaign structure, segments, budgets, and targets.

---

## Meta Ads Account Structure

```
Pic Your Booth Ad Account
├── PROSPECTING - Magic Mirror XL (CBO, €30-50/day)
│   ├── Advantage+ Audience - broad, NL Randstad
│   ├── Lookalike 1% - past leads/customers
│   └── Interest: weddings, corporate events, party planning
├── PROSPECTING - Party Booth (CBO, €20-30/day)
│   ├── Advantage+ Audience - broad, NL Randstad
│   └── Interest: birthday parties, celebrations
├── PROSPECTING - DJ + Photobooth Combo (CBO, €20-30/day)
│   └── Interest: party planning, wedding planning
├── RETARGETING (ABO, €10-15/day)
│   ├── Website visitors 1-7 days (excl. converters)
│   ├── Website visitors 8-30 days
│   ├── IG/FB engagers 30 days
│   └── Form openers who didn't submit
└── SEASONAL / PROMO (when applicable)
```

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
| CTR (prospecting) | >1.0% | Refresh creative/hook |
| CPC | <€1.50 | Improve creative relevance |
| CPL (cost per lead) | <€25 | Optimize audiences + creative |
| Form conversion rate | >5% | Audit landing page (`/design-landingpage`) |
| Frequency (prospecting) | <3.0 | Expand audience or rotate creative |
| Google Search CTR | >5% | Improve ad copy relevance |
| Google Search CPC | <€2.00 | Improve Quality Score |

## Segments & Messaging

| Segment | Product | Tone | Key Message | Price Anchor |
|---|---|---|---|---|
| Perfectionist Planner | Magic Mirror XL | Premium, trust | "DSLR kwaliteit, geen tijdslimiet" | Vanaf €599 |
| Budget Celebrator | Party Booth | Fun, easy | "Foto plezier voor elk feest" | Vanaf €199 |
| All-in-One Seeker | DJ + Combo | Energy, convenience | "Eén team, één vibe" | Vanaf €348 |
| Wedding Planners | Magic Mirror + DJ | Premium, personal | "Jullie dag, onze ervaring" | Vanaf €748 |

## Budget Allocation (Starting)

| Channel | % of Total | Monthly Budget |
|---|---|---|
| Meta Ads - Prospecting | 40% | €600-800 |
| Meta Ads - Retargeting | 15% | €225-300 |
| Google Ads - Search | 35% | €525-700 |
| Google Ads - PMax | 10% | €150-200 |

## Funnel: Ad → Conversion

```
Meta/Google Ad → Landing Page → Proposal Form → Proposal Email → Booking
```

Every ad must map to a landing page that passes the 3-second message match test.
Use `/design-landingpage` to build conversion-optimized pages for ad traffic.
