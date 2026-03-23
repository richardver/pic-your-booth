# Website — PYB Specifics

PYB-specific page templates, form spec, personalization rules, and conversion tactics. For generic CRO frameworks see `docs/website/`.

---

## Page Templates

### Homepage
```
[Hero] - Bold headline + event video/photo + CTA
[Social Proof Bar] - 237+ Events, 4.9★, Randstad
[Services] - Party Booth / Magic Mirror / DJs (3 cards)
[How It Works] - 3 steps
[Testimonials] - 2-3 quotes with photos
[Gallery] - Best event photos
[FAQ] - Top 5 objections
[Final CTA] - Proposal request
```

### Service Landing Page (for ads)
```
[Hero] - Service-specific headline matching ad + CTA
[Problem] - Why generic isn't enough
[Solution] - What makes PYB different
[Social Proof] - Testimonials + event photos
[Pricing Preview] - Starting from €X
[How It Works] - 3 steps
[FAQ] - 3-5 objections
[Final CTA] - Proposal request form
```

---

## Proposal Form (Max 6 Fields)

| Field | Type | Required | Shadcn Component |
|---|---|---|---|
| Naam | Text | Yes | Input + Label |
| E-mail | Email | Yes | Input + Label |
| Telefoon | Tel | Yes | Input + Label |
| Datum Event | Date | Yes | Input + Label |
| Type Event | Select | Yes | Select |
| Bericht | Textarea | No | Textarea + Label |

**CTA button:** "Ontvang je voorstel" (gold, black text)
**Sub-CTA text:** "Binnen 24 uur reactie • Vrijblijvend"
**Thank-you page:** "We nemen binnen 24 uur contact op!"

### Form UX (PYB-specific)
- Gold focus ring on all fields (`border-[#d4b14e] ring-[#d4b14e]/20`)
- Input types: `tel` (numpad), `email`, `date`
- Inline validation: "Vul een geldig e-mailadres in" (not "Fout")
- "(populaire data gaan snel)" label on date field
- Pre-fill message field when coming from package builder with selected upgrades + total
- Multi-step alternative: Step 1 = date + type, Step 2 = contact details

---

## Personalization Rules

### By Traffic Source

| Source | Landing Page Adaptation |
|---|---|
| Meta ad — Magic Mirror | Premium visuals, wedding/corporate focus, €599 starting price |
| Meta ad — Party Booth | Fun visuals, party focus, "vanaf €199" |
| Meta ad — DJ + Combo | Energy visuals, combo pricing, Spotify feature |
| Google "photobooth huren" | General page, all services overview |
| Google "photobooth bruiloft" | Wedding-specific, wedding testimonials |
| Returning visitor | "Welkom terug" + last viewed package highlighted |

### By Behavior

| Rule | Personalization |
|---|---|
| Visited pricing but didn't convert | "Populaire datums raken snel vol" |
| Viewed wedding packages | Wedding testimonials in social proof bar |
| Viewed corporate packages | Corporate client logos |
| Mobile from Instagram | Full-screen video hero, thumb-friendly CTA |
| 2+ visits, no form submit | "Nog vragen? Bel ons: [phone]" sticky banner |

---

## Message Match (PYB-specific)

| Ad Content | Landing Page Must Show |
|---|---|
| "Magic Mirror XL Photobooth" + event video | Hero with same visual + "Magic Mirror XL" in headline |
| "Photobooth huren vanaf €199" | Price visible above fold: "Vanaf €199" |
| "DJ + Photobooth combo" | Combo package front and center |
| Testimonial ad from wedding couple | Same testimonial + more wedding proof |

---

## Booking Friction Fixes

| Friction | Solution |
|---|---|
| Unclear pricing | "Vanaf €X" on every package — don't hide prices |
| No availability info | "Check beschikbaarheid" CTA with date field |
| Too many choices | Max 3 packages, "Meest gekozen" badge on Magic Mirror |
| No trust signals | Google reviews widget, testimonial near form, "237+ events" |
| Slow response | "Binnen 24 uur reactie" — automate confirmation email |
| No risk reversal | "Vrijblijvend voorstel" prominently near form |

---

## Proposal Email Psychology

| Element | Psychology | Implementation |
|---|---|---|
| Personalized greeting | Liking | "Hoi [naam], leuk dat je een event plant!" |
| Visual mock-up | Endowment effect | Show their event type with PYB setup |
| Package recommendation | Choice architecture | Highlight one "Aanbevolen" package |
| Testimonial | Social proof | Match testimonial to their event type |
| Clear pricing | Reduce anxiety | No hidden costs, transparent total |
| Scarcity | Loss aversion | "Je datum is nog beschikbaar" |
| Easy next step | Ability (Fogg) | "Klik hier om te bevestigen" — one action |
| Time limit | Urgency | "We houden je datum 7 dagen vast" |

---

## Email Sequences

### Post-Form Nurture

| Email | Timing | Subject |
|---|---|---|
| 1 | Immediate | "Je voorstel van Pic Your Booth" |
| 2 | Day 2 | "Heb je nog vragen, [naam]?" |
| 3 | Day 5 | "Zo was het bij [similar event]" |
| 4 | Day 8 | "Je datum is populair" |
| 5 | Day 14 | "Laatste check: nog interesse?" |

### Post-Event

| Email | Timing | Subject |
|---|---|---|
| 1 | Day 1 | "Bedankt voor de geweldige avond!" |
| 2 | Day 3 | "Je foto's staan klaar!" |
| 3 | Day 5 | "Zou je ons willen reviewen?" |
| 4 | Day 7 | "Ken je iemand die ook een feest plant?" |
| 5 | Month 3 | "Alweer bijna [seizoen] — plan je iets?" |

---

## References (generic frameworks)

- CRO 55-item checklist: `.claude/agents/designer/knowledge-cro-checklist.md`
- Landing page structure templates: `.claude/agents/designer/knowledge-landing-pages.md`
- Full PRD: `docs/plans/prd-website.md`
