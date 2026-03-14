# A/B Testing — Methodology & Framework

## Test Design Framework

### Step 1: Hypothesis
**Format**: "If we [change], then [metric] will [improve/decrease] by [estimated amount], because [rationale]."

**Quality checklist:**
- [ ] Based on data (analytics, heatmaps, user research), not opinion
- [ ] Specifies a single, measurable primary metric
- [ ] Includes a falsifiable prediction
- [ ] Tied to a documented user problem
- [ ] Estimated impact is realistic

### Step 2: Variable Selection

| Type | Description | When to Use |
|---|---|---|
| Single variable | One element changed | Diagnosing what works |
| Compound variable | Multiple related elements | Strong hypothesis about a section |
| Page-level | Entirely different design | Enough traffic, need step-change |

### Step 3: Primary Metric
Choose ONE primary metric. Track secondaries for context only.

### Step 4: Duration
- Minimum: 2 full weeks (capture all days of week)
- Maximum: 8 weeks
- Avoid: Holidays, seasonal peaks, launch periods

### Step 5: Sample Size
Calculate BEFORE launching. Never start without knowing when to stop.

## Sample Size Reference Table
*95% significance, 80% power, per variation:*

| Baseline CVR | MDE: 10% relative | MDE: 20% relative | MDE: 25% relative |
|---|---|---|---|
| 2% | 383,000 | 98,000 | 63,000 |
| 5% | 147,000 | 38,000 | 25,000 |
| 10% | 68,000 | 18,000 | 12,000 |
| 20% | 30,000 | 8,200 | 5,400 |

**For PYB**: With ~1,000-5,000 monthly visitors, skip A/B testing and implement best practices directly. Use before/after measurement. Consider qualitative testing (5 user tests catch 85% of issues).

---

## ICE Prioritization

Score each test idea (1-10):

| Dimension | Question |
|---|---|
| **Impact** | How large will the effect be? |
| **Confidence** | How certain based on data? |
| **Ease** | How simple to implement? |

**ICE Score = Impact × Confidence × Ease**

### PYB Test Priority List

| Test | I | C | E | ICE | Priority |
|---|---|---|---|---|---|
| Rewrite hero headline to match top ad copy | 7 | 8 | 9 | 504 | P1 |
| Reduce form from current to 5-6 fields | 8 | 7 | 7 | 392 | P1 |
| Add video testimonial above fold | 6 | 6 | 5 | 180 | P2 |
| Add Google reviews widget near form | 7 | 7 | 8 | 392 | P1 |
| Sticky CTA button on mobile | 6 | 7 | 9 | 378 | P1 |
| Price anchoring (show VIP first) | 5 | 6 | 9 | 270 | P2 |

---

## Common Testing Pitfalls

### 1. Peeking
Checking daily and stopping at first p < 0.05. False positive rate jumps from 5% to ~26%.
**Fix**: Pre-commit to sample size and duration.

### 2. Novelty Effect
New design performs well initially, fades as returning visitors adjust.
**Fix**: Segment new vs returning visitors. Run 3-4 weeks.

### 3. Underpowered Tests
Small traffic = can't detect real differences. "No significant result" ≠ "no effect."
**Fix**: For low traffic sites, implement best practices directly.

### 4. Multiple Comparisons
Testing 5 variations: 23% chance of at least one false positive.
**Fix**: Test fewer variations with stronger hypotheses.

### 5. Message Mismatch
Testing landing page without aligning ad creative.
**Fix**: Always ensure ad → landing page consistency.

---

## Test Documentation Template

```
TEST: [Name]
DATE: [Start] — [End]
PAGE: [URL]

HYPOTHESIS:
If we [change], then [metric] will [direction] by [amount],
because [rationale].

VARIATIONS:
- Control: [Description]
- Variant: [Description]

PRIMARY METRIC: [Metric]
SAMPLE SIZE NEEDED: [Per variation]

RESULTS:
- Control: [X%]
- Variant: [X%] (p = [X])
- Winner: [Control / Variant / Inconclusive]

DECISION: [Implement / Iterate / Archive]
LEARNINGS: [What we learned]
```

---

## Testing Velocity

| Stage | Tests/Month | Focus |
|---|---|---|
| PYB now (low traffic) | 1-2 | High-impact changes, implement best practices directly |
| PYB growing | 2-4 | Section-level tests on landing pages |
| PYB scaling | 4-8 | Element-level tests, creative testing |

**Compounding effect**: 8 tests/month × 30% win rate × 5% avg lift = ~14% improvement per quarter = 60%+ per year.
