# Meta Ads — Facebook & Instagram Reference

## Campaign Structure Overview

### CBO vs ABO

| Factor | CBO | ABO |
|---|---|---|
| Budget control | Campaign level — Meta distributes | Ad set level — you control each |
| Best for | Testing many audiences, scaling winners | Controlled tests, fixed audience budgets |
| When to use | 3+ ad sets, scaling phase | Launch testing, strict budget requirements |
| Minimum budget | €30-50/day per campaign | €10-20/day per ad set |

### Recommended Account Structure
```
Account
├── Prospecting (CBO)
│   ├── Advantage+ Audience — broad targeting
│   ├── Lookalike stack — 1%, 3%, 5%
│   └── Interest-based — layered interests
├── Retargeting (ABO)
│   ├── Website visitors 1-7 days
│   ├── Website visitors 8-30 days
│   ├── Engaged social audience
│   └── Form abandoners
├── Retention (ABO)
│   ├── Past customers — upsell
│   └── Lapsed customers — win-back
└── Advantage+ Shopping Campaign (if applicable)
    └── Existing customer budget cap 20-30%
```

## Audience Strategy

### Custom Audiences

| Source | Retention | Quality | Notes |
|---|---|---|---|
| Customer list (email/phone) | Refresh monthly | High | Min 1,000 records |
| Website visitors (all) | 180 days max | Medium-High | Pixel + CAPI |
| Website — specific pages | 30-90 days | High | Pricing, form pages |
| Video viewers (25%, 50%, 75%, 95%) | 365 days | Medium | Layer by engagement |
| Lead form openers/submitters | 90 days | High | Retarget non-converters |
| Instagram/Facebook engagers | 365 days | Medium | Broad but relevant |

### Lookalike Audiences

| Seed Audience | Recommended % | Quality |
|---|---|---|
| Purchasers / high-LTV customers | 1% | Highest |
| All converters (leads + purchases) | 1-3% | High |
| Website visitors (all) | 3-5% | Medium |
| Page engagers | 5-10% | Lower |

### Advantage+ Audience (Recommended Default)
- Replaces manual targeting with Meta's ML-driven discovery
- Provide audience suggestions as signals, not restrictions
- Outperforms manual targeting in 60-70% of A/B tests
- Best practice: A/B test against your best manual audience

## Creative Specs by Placement

| Placement | Format | Aspect Ratio | Resolution (min) | Max File Size |
|---|---|---|---|---|
| Feed (FB + IG) | Image | 1:1 or 4:5 | 1080x1080 / 1080x1350 | 30 MB |
| Feed (FB + IG) | Video | 1:1 or 4:5 | 1080x1080 / 1080x1350 | 4 GB |
| Stories / Reels | Image | 9:16 | 1080x1920 | 30 MB |
| Stories / Reels | Video | 9:16 | 1080x1920 | 4 GB |
| Right column (FB) | Image | 1:1 | 1080x1080 | 30 MB |
| Messenger | Image | 1:1 | 1080x1080 | 30 MB |

### Video Best Practices
- First 3 seconds must hook — assume sound off
- Add captions/text overlays (85% watch without sound)
- Optimal: 15-30 seconds for conversion, 6-15 seconds for awareness
- Vertical (9:16) outperforms horizontal in mobile-first placements

## Creative Best Practices

### The 4C Creative Framework

| Element | Description | Example |
|---|---|---|
| **Catch** | Pattern interrupt in first 1-3 seconds | Bold text overlay, unexpected visual, direct question |
| **Connect** | Relate to audience pain point | "Looking for the perfect party entertainment?" |
| **Convince** | Proof, features, social evidence | Testimonial, event footage, before/after |
| **Close** | Clear CTA aligned with funnel stage | "Vraag een offerte aan", "Book Now" |

### Creative Volume & Testing
- Launch with 3-6 creative variations per ad set minimum
- Test one variable at a time:
  - Hook / opening (biggest impact)
  - Format (static vs video vs carousel)
  - Copy angle (benefit vs feature vs testimonial vs UGC)
  - CTA (direct vs soft)
- Kill underperformers after 2x target CPA spend with zero or poor conversions
- Refresh creative every 2-4 weeks to combat fatigue

### Creative Types That Perform

| Format | Best For | Tips |
|---|---|---|
| UGC-style video | Conversion, consideration | Authentic feel, real people, not polished |
| Static with bold text | Retargeting, offers | Clear value prop, minimal design, high contrast |
| Carousel | Multi-product, storytelling | First card must hook; use all 10 cards |
| Reels-native video | Prospecting, awareness | Trending audio, fast cuts, vertical only |

## iOS ATT Mitigation

### Conversions API (CAPI)
- [ ] Server-side event tracking (Purchase, Lead, AddToCart, ViewContent minimum)
- [ ] Event match quality score above 6.0 (target 8.0+)
- [ ] Deduplicate Pixel + CAPI with matching `event_id`
- [ ] Include max user parameters: email, phone, IP, user agent, fbc, fbp
- [ ] Hash PII before sending (SHA-256)

### Aggregated Event Measurement (AEM)
- [ ] Domain verified in Business Manager
- [ ] 8 conversion events configured and prioritized
- [ ] Event priority: Purchase > Lead > AddToCart > ViewContent
- [ ] 72-hour delay after configuration changes

## Budget Scaling

### The 20% Rule
Never increase budget more than **20% every 3-5 days**. Larger jumps reset learning phase.

### Scaling Decision Framework

| Signal | Action |
|---|---|
| CPA below target for 5+ days | Scale budget by 20% |
| CPA at target, stable | Hold, test new creative |
| CPA 10-30% above target | Refresh creative, check frequency |
| CPA 30%+ above target | Reduce budget, diagnose issue |
| Frequency > 3.0 (prospecting) | Expand audience or refresh creative |
| Frequency > 6.0 (retargeting) | Reduce budget or expand window |

### Budget Allocation (Starting Point)

| Funnel Stage | % of Budget | Objective |
|---|---|---|
| Prospecting (TOF) | 60-70% | New audience acquisition |
| Retargeting (MOF) | 15-25% | Warm audience conversion |
| Retention (BOF) | 10-15% | Repeat booking & referrals |

## Key Benchmarks

| Metric | Prospecting | Retargeting |
|---|---|---|
| CTR | 0.8-1.5% | 1.5-3.0% |
| CPC | €0.60-€2.00 | €0.30-€1.00 |
| CPM | €8-€18 | €10-€25 |
| Conv Rate | 1-3% | 4-10% |
| Frequency (healthy) | < 3.0 | < 6.0 |

> Benchmarks vary by vertical, geography, season, and creative quality. Calibrate to your own data within 30 days.
