---
name: design-landingpage
description: "Design or optimize a high-converting landing page for Meta Ads traffic. Applies message match, CRO checklist, pricing psychology, and conversion architecture. Use /design-landingpage when the page must convert ad traffic into proposal requests."
user-invocable: true
---

# Design Landing Page

Design or optimize a landing page specifically for conversion from paid traffic (Meta Ads). This skill goes beyond `/design-page` by applying landing page-specific conversion architecture, message match, objection handling, and funnel psychology.

Use this when:
- Building a new landing page for a Meta Ads campaign
- Optimizing an existing page that isn't converting
- The page's #1 job is turning ad clicks into proposal requests

## Input

The user specifies:
- Which product/segment (Magic Mirror XL, Party Booth, DJ Combo, or All)
- The ad that drives traffic (headline, creative, offer) — for message match
- Any known conversion problems ("form abandonment", "high bounce", etc.)

## Steps

### Phase 1: Load Conversion Knowledge (mandatory)

1. **CRO framework** — Read these files:
   - `.claude/agents/designer/knowledge-cro-checklist.md` — 55-item audit checklist, scoring rubric, conversion killers
   - `.claude/agents/designer/knowledge-landing-pages.md` — page structure, hero formulas, CTA optimization, social proof placement
   - `.claude/agents/designer/knowledge-forms.md` — form optimization, message match rules, personalization, email sequences

2. **Pricing psychology** — Read:
   - `.claude/agents/strategist/knowledge-psychology-pricing.md` — anchoring, decoy, charm pricing, loss aversion, endowment, Cialdini, Fogg B=MAP
   - `.claude/agents/strategist/knowledge-psychology-buyer-journey.md` — JTBD, four forces of switching, psychographic profiles, moments of truth

3. **Product specs** — Dispatch product-specialist agent for the relevant product:
   - Read `.claude/agents/product-specialist/_index.md` → route to product + pricing knowledge

4. **Brand & design** — Read:
   - `.claude/agents/strategist/knowledge-brand.md` — brand guide, visual identity, tone
   - `.claude/agents/designer/knowledge-design-system-full.md` — tokens, colors, typography
   - `.claude/agents/designer/pyb-design-system-photobooth.html` — page-specific design system (if photobooth)
   - `.claude/agents/designer/pyb-design-system-dj.html` — page-specific design system (if DJ)

5. **Photo library** — Read `images/photos-source/INDEX.md` for available source photos per product/USP, quality ratings, and Gemini AI reference picks. Use best-rated photos for image selection and `/generate-asset` input.

6. **Ad context** — Read:
   - `.claude/agents/ad-specialist/knowledge-meta-ads-full.md` — campaign structure, creative specs
   - `.claude/agents/ad-specialist/knowledge-ad-copy-full.md` — hook formulas, copy specs
   - `.claude/agents/ad-specialist/knowledge-creative-testing-full.md` — testing framework

6. **PRD reference** — Read `docs/plans/prd-website.md` for canonical page spec.

### Phase 2: Conversion Architecture

7. **Message match audit** — Verify or define:
   - Ad headline → landing page headline must echo it
   - Ad visual style → landing page hero must match
   - Ad offer/price → must be visible above the fold
   - Visitor confirms "right place" within 3 seconds
   - Score: does the current page (if exists) pass the 3-second test?

8. **Identify the psychographic profile** — From buyer-journey knowledge:
   - Perfectionist Planner (Magic Mirror / Wedding)
   - Fun Organizer (Magic Mirror / Corporate)
   - Budget-Smart Celebrator (Party Booth)
   - All-in-One Seeker (DJ + Photobooth Combo)
   - Map their fears, motivations, and proof needs

9. **Apply Fogg B=MAP diagnosis** — For this page:
   - **Motivation**: What amplifies desire? What reduces fear?
   - **Ability**: How simple is the action? What friction exists?
   - **Prompt**: Is the CTA visible, clear, timed correctly?
   - Identify which element is weakest → that's the priority fix

10. **Define the conversion architecture** — Structure the page:

```
[1. Hero]           Message match + value prop + CTA (above fold)
[2. Social Proof]   Specific numbers, logos, or star ratings
[3. Problem]        Agitate the pain (why generic isn't enough)
[4. Solution]       PYB differentiators (DSLR, Spotify, family)
[5. Social Proof]   Testimonial matching the segment
[6. Package/Price]  Anchored pricing, charm pricing, builder if applicable
[7. How It Works]   3 steps (reduce anxiety)
[8. FAQ]            Top 3-5 objections handled
[9. Final CTA]      Repeat offer + urgency + risk reversal
[10. Form]          6 fields max, value-framed submit button
```

11. **Present the conversion plan** — Show the user:
    - Page sections with conversion purpose of each
    - Message match mapping (ad → hero)
    - Psychographic profile targeted
    - Fogg B=MAP assessment
    - Pricing psychology tactics to apply
    - Ask for approval before building

### Phase 3: Build

12. **Invoke `/impeccable:frontend-design`** — Build the landing page with:
    - The conversion architecture from step 10
    - PYB design tokens and visual mode
    - Single-page focus: no navigation distractions (remove or minimize nav)
    - One primary CTA per viewport
    - Mobile-first (70%+ of Meta Ads traffic is mobile)

13. **Apply conversion-specific patterns:**
    - **Hero**: headline matches ad, subheadline adds context, CTA visible without scroll
    - **Social proof bar**: "237+ Events Verzorgd | 4.9★ Google Reviews | Randstad"
    - **Pricing**: anchor high first, charm pricing, "MEEST GEKOZEN" badge on target option
    - **Form**: 6 fields, `tel`/`email`/`date` input types, "Ontvang je voorstel" CTA, sub-text "Binnen 24 uur reactie • Vrijblijvend"
    - **Urgency**: "(populaire data gaan snel)" on date field if true
    - **Risk reversal**: "100% vrijblijvend • Geen spam, beloofd" near form
    - **Directional cues**: visual flow pointing toward CTA

14. **Objection handling** — For the target segment, address in FAQ:
    - "Te duur" → anchor against alternatives, per-hour framing
    - "We denken er nog over na" → scarcity, social proof, reduce risk
    - "We doen het zelf wel" → quality difference (DSLR vs phone)
    - "Kennen jullie niet" → reviews, imagery, guarantee

### Phase 4: Conversion QA (never skip)

15. **Run `/impeccable:audit`** — Technical quality audit. Fix issues.

16. **Run `/impeccable:typeset`** — Fix typography.

17. **Run `/impeccable:arrange`** — Fix layout and spacing.

18. **Run `/impeccable:polish`** — Final design pass.

19. **55-item CRO checklist** — Score every item from `knowledge-cro-checklist.md`:
    - Above-Fold Clarity (20%) — items 1-10
    - Trust & Credibility (15%) — items 11-18
    - Copy & Messaging (15%) — items 19-28
    - CTA & Form Design (20%) — items 29-38
    - Visual Design (10%) — items 39-44
    - Mobile Experience (10%) — items 45-49
    - Page Speed (10%) — items 50-55
    - **Calculate Landing Page Score (0-100)**
    - Target: 85+ before shipping

20. **Brand check** — Verify:
    - [ ] Party Booth (not iPad Photobooth)
    - [ ] PicYourBooth (not Pic Your Moment)
    - [ ] No red (#ff494a) or pink (#e839a0)
    - [ ] Dutch copy sounds native
    - [ ] Gold buttons have black text
    - [ ] Charm pricing used
    - [ ] Correct segment tone

21. **Message match final check** — Re-verify:
    - [ ] Hero headline echoes ad headline
    - [ ] Visual style matches ad creative
    - [ ] Price/offer visible above fold matches ad promise
    - [ ] 3-second test passes

### Phase 5: Deliver

22. **Output** — Production-ready landing page with:
    - Complete HTML/CSS/Tailwind code
    - Landing Page Score (0-100) with category breakdown
    - Message match mapping
    - Fogg B=MAP assessment
    - Conversion psychology applied (list)
    - Remaining recommendations for A/B testing

## Rules

- **Single conversion goal** — every element serves the proposal form
- **No navigation distractions** — remove or minimize nav on landing pages
- **Message match is #1** — mismatch = -30 to -60% conversion rate
- **Mobile-first** — 70%+ of Meta Ads traffic is mobile
- **Landing Page Score must be 85+** — don't ship below this
- **Fogg B=MAP** — if conversion is low, diagnose which element is failing
- **Dutch copy** — all customer-facing text in native Dutch
