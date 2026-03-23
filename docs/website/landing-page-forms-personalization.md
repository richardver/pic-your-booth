# Landing Pages — Forms, Personalization & Optimization

Generic frameworks for form optimization, personalization, and conversion. PYB-specific form specs, personalization rules, message match mapping, and email sequences live in the designer agent's `knowledge-website.md`.

---

## Form Optimization Principles

### The Golden Rule
Every additional form field reduces conversion by approximately 4-7%.

### Form UX Best Practices

| Principle | Implementation |
|---|---|
| **Progressive disclosure** | Show only essential fields first; collect more later |
| **Inline validation** | Real-time feedback as fields are completed |
| **Smart defaults** | Pre-select most common option |
| **Appropriate input types** | `tel` (numpad), `email` (@ keyboard), `date` (picker) |
| **Error messages** | Specific and near the field — not generic "Error" |
| **Submit button copy** | Describe value received, not the action ("Get your quote" not "Submit") |
| **Sub-CTA text** | Reduce anxiety ("No spam", "Free", "Within 24 hours") |
| **Thank-you page** | Set expectations for next steps |

### Multi-Step Forms
For high-value offers, split into steps:
1. **Step 1**: Low commitment (date, type) — gets user invested
2. **Step 2**: Contact details — already committed, more likely to complete
Progress bar reduces anxiety.

---

## Personalization Levels

### Level 1: Segment-Based
Match landing page content to the traffic source (ad, search, email). Headline, visuals, and pricing echo the referral source.

### Level 2: Rule-Based
Adapt based on visitor behavior:
- Visited pricing but didn't convert → add urgency
- Viewed specific category → show matching social proof
- Mobile from social → full-screen hero, thumb-friendly CTA
- Returning visitor → show familiarity cues, offer direct contact

---

## Message Match

The #1 conversion killer is mismatch between ad and landing page (-30 to -60% CVR impact).

**Rule:** Visitor confirms they're in the right place within 3 seconds.

| Ad Element | Landing Page Must Match |
|---|---|
| Headline/hook | Hero headline echoes it |
| Visual style | Hero image matches ad creative |
| Price/offer | Visible above the fold |
| Testimonial | Same person on landing page |

---

## Checkout / Booking Friction Reduction

| Friction | Generic Solution |
|---|---|
| Unclear pricing | Show price on every package — don't hide it |
| No availability | Date picker or "Check availability" CTA |
| Too many choices | Max 3 options, highlight recommended |
| No trust signals | Reviews, testimonials, guarantees near CTA |
| Slow response | Promise and deliver fast response time |
| No risk reversal | "Free", "No obligation", guarantee |

---

## Proposal / Quote Email Psychology

| Element | Psychology Principle |
|---|---|
| Personalized greeting | Liking |
| Visual of their selection | Endowment effect |
| Recommended option | Choice architecture |
| Matching testimonial | Social proof |
| Transparent pricing | Anxiety reduction |
| Availability note | Loss aversion / scarcity |
| One-click next step | Ability (Fogg) |
| Time-limited hold | Urgency |
