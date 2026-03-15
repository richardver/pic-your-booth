# Creative Testing Framework & Fatigue Management

## Creative Testing - 10-Step Methodology

### 1. Define Testing Variables
Catalog all testable creative elements:
- Headline copy, body copy length, CTA text and color
- Hero image subject, image style (photo vs UGC vs graphic)
- Video hook (first 3 seconds), video length
- Ad format (static vs carousel vs video)
- Offer framing (discount vs value vs urgency)
- Social proof type (testimonial vs stat vs event footage)

### 2. Prioritize by Impact & Effort
Score each variable on a 2x2 matrix:
- **High impact, low effort** → Test FIRST
- **High impact, high effort** → Test SECOND
- **Low impact, low effort** → Test when capacity allows
- **Low impact, high effort** → Skip

### 3. Design Testing Matrix
- 2-4 variants per variable, tested against current control
- One variable per test (isolated testing)
- Map each test to audience segment and platform

### 4. Calculate Sample Size
Based on: current conversion rate, minimum detectable effect (10-20% lift), significance level (90-95%)

### 5. Define Holdout Control
- Allocate 10-20% of testing budget to unchanging control
- Refresh control quarterly or when it degrades below threshold
- New winners graduate to become the new control

### 6. Set Statistical Thresholds
- 90% confidence for directional decisions
- 95% confidence for major creative shifts
- Minimum 7-day observation period (day-of-week variation)
- No peeking before sample size is reached

### 7. Create Iteration Cadence
- **High-volume**: Weekly creative refreshes
- **Mid-volume**: Bi-weekly
- **Low-volume**: Monthly
- Pipeline: Brief (day 1) → Production (days 2-3) → Review (day 4) → Launch (day 5) → Monitor (days 6-14) → Analyze (day 15)

### 8. Build Winner Selection Criteria
- Primary metric (CTR, conversion rate, ROAS, or CPA)
- Minimum confidence level reached
- Minimum sample size reached
- Guardrail metrics must not degrade

### 9. Naming Convention
`platform_audience_variable_variant_date`
Example: `meta_prospecting_hook_testimonial_20260314`

### 10. Document Results
Test card template:
- Hypothesis → Variable tested → Variants → Audience → Platform
- Date range → Sample size → Primary metric results
- Statistical significance → Winner → Key learning → Next test

---

## Creative Fatigue Management

### What It Is
Performance degrades because the audience has seen the creative too many times. Not about quality - about exhaustion.

### Decay Curve Types
- **Linear decay**: Gradual, steady decline. Broad audiences. CTR drops ~2-5% per week.
- **Cliff decay**: Stable then sudden sharp drop (>30% in 48 hours). Narrow audiences.
- **Plateau-drop**: Extended stable period, then accelerating decline. Well-targeted ads.
- **S-curve decay**: Slow decline, accelerating, then leveling at a lower floor. Always-on campaigns.

### Per-Segment Fatigue Thresholds

| Audience Size | Fatigue Begins at Frequency | Creative Lifespan |
|---|---|---|
| Narrow (<100K) | 4-6 | 2-3 weeks |
| Medium (100K-1M) | 6-10 | 3-6 weeks |
| Broad (>1M) | 10-15 | 6-12 weeks |
| Retargeting | Fastest | Rotate every 1-2 weeks |

### Fatigue Signal Detection

**Primary Signals:**
- Frequency rises but CTR drops → fatigue beginning
- CTR velocity declining (rate of change, not absolute) → earliest warning (2-3 days ahead)
- CPM inflating while CTR drops → lagging but unambiguous
- CPA rising while conversion rate holds → spending more to find responsive users

**Secondary Signals:**
- Likes/reactions declining before clicks
- Negative feedback ("hide", "not interested") increasing
- Comment sentiment shifting ("I keep seeing this ad")
- Video completion rate dropping

### Distinguishing Fatigue Types

| Type | CTR | Conversion Rate | Solution |
|---|---|---|---|
| **Creative fatigue** | Drops first | Then drops | Rotate creative |
| **Landing page fatigue** | Holds | Drops | Fix landing page |
| **Offer fatigue** | Drops | Drops, but CTR recovers with new creative | Change the offer |
| **Audience exhaustion** | All decline | All decline, no recovery with creative changes | Expand audience |

### Fatigue Threshold Triggers

| Metric | Warning (prepare replacement) | Action (rotate now) |
|---|---|---|
| CTR | Below 80% of baseline | Below 70% of baseline |
| CPM | Above 115% of baseline | Above 130% of baseline |
| Engagement rate | Below 75% of baseline | Below 60% of baseline |
| Negative feedback | Above 150% of baseline | Above 200% of baseline |
| Cost per result | Above 120% of baseline | Above 140% of baseline |

### Time-to-Fatigue Estimation
```
days_to_fatigue = (audience_size / daily_impressions) * platform_factor
```
Platform factors: Meta ~0.8, TikTok ~0.6

### Creative Lifecycle Phases
1. **Creation**: Brief → Production → Review → Approval (include fatigue estimate)
2. **Launch**: Deploy with full tracking, capture baseline in first 72 hours
3. **Monitor**: Weekly fatigue assessment using moving averages
4. **Predict**: Estimate days to action threshold, communicate to team
5. **Refresh/Rotate**: Deploy new variant, A/B test against fatigued creative
6. **Archive**: Store performance data, tag with audience/platform/lifespan
