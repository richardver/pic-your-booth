---
name: design-page
description: "Design a complete website page from scratch using the full PYB knowledge stack — brand, product specs, design system, CRO, and Impeccable quality skills. Use /design-page to build any page for picyourbooth.nl."
user-invocable: true
---

# Design Page

Design a complete, production-ready website page for PicYourBooth using the full knowledge stack. Never skips a step.

## Input

The user specifies which page to build:
- Homepage (`/`)
- Magic Mirror XL (`/magic-mirror`)
- Party Booth (`/party-booth`)
- DJs (`/djs`)
- Offerte / Proposal Form (`/offerte`)
- Custom page (describe it)

## Steps

### Phase 1: Load Context (never skip)

1. **Product knowledge** — Dispatch the product-specialist agent to load specs for the relevant product(s):
   - Read `.claude/agents/product-specialist/_index.md` → route to the right knowledge file
   - For homepage: load ALL products (party-booth, magic-mirror, dj-services, pricing)
   - For product pages: load that product + pricing
   - For DJs page: load dj-services + pricing
   - For offerte: load pricing (all products)

2. **Brand context** — Read these files:
   - `.claude/agents/strategist/knowledge-brand.md` — brand guide, services, tone, visual identity
   - `.claude/rules/brand-voice.md` — always-active voice rules (auto-loaded, but verify)

3. **Design system** — Read these files:
   - `.claude/agents/designer/knowledge-design-system-full.md` — tokens, colors, typography, components
   - `.claude/agents/designer/knowledge-ux-principles.md` — accessibility, responsive, visual hierarchy
   - `.claude/agents/designer/pyb-design-system-web.html` — parent design system (visual reference)
   - Page-specific design system if applicable:
     - Photobooth pages → `.claude/agents/designer/pyb-design-system-photobooth.html`
     - DJ page → `.claude/agents/designer/pyb-design-system-dj.html`

4. **Photo library** — Read `images/photos-source/INDEX.md` for available source photos per product/USP, quality ratings, and Gemini AI reference picks. Use best-rated photos for image placeholders and `/generate-asset` input.

5. **CRO & conversion knowledge** — Read these files:
   - `.claude/agents/designer/knowledge-landing-pages.md` — page structure, hero formulas, CTAs
   - `.claude/agents/designer/knowledge-cro-checklist.md` — 55-item audit checklist
   - `.claude/agents/designer/knowledge-forms.md` — form optimization, message match

5. **Psychology & buyer journey** — Read these files:
   - `.claude/agents/strategist/knowledge-psychology-pricing.md` — anchoring, charm pricing, Cialdini
   - `.claude/agents/strategist/knowledge-psychology-buyer-journey.md` — JTBD, journey map, psychographics

6. **PRD reference** — Read `docs/plans/prd-website.md` for the canonical page specification (sections, copy, interactions, integrations).

### Phase 2: Plan

7. **Identify the page spec** — From the PRD, extract the exact sections, copy, and interactions for this page. List them.

8. **Identify the target segment** — Which psychographic profile(s) does this page serve? What visual mode applies (premium/accessible/energy)?

9. **Identify conversion goal** — What is the primary CTA? Where does this page sit in the funnel (Meta Ad → Landing Page → Form → Proposal → Booking)?

10. **Present the plan** — Show the user:
    - Page sections in order
    - Visual mode (dark/gold/violet/coral/cyan)
    - Primary CTA text and placement
    - Key conversion psychology to apply
    - Ask for approval before building

### Phase 3: Build

11. **Invoke `/impeccable:frontend-design`** — Use the Impeccable frontend-design skill to build the page. This skill produces distinctive, production-grade code that avoids generic AI aesthetics. Feed it:
    - The page plan from step 10
    - PYB design tokens and visual mode
    - The section-by-section spec from the PRD

    The frontend-design skill will handle semantic HTML, Tailwind CSS, responsive behavior, and accessibility. Ensure the output follows PYB conventions:
    - Apply PYB design tokens (colors, typography, spacing from design-system.md)
    - Use the correct visual mode for the segment
    - Apply CRO best practices (hierarchy, contrast, CTA placement)
    - Ensure mobile-first (70%+ traffic is mobile)
    - Include accessibility (ARIA, focus states, contrast, touch targets)

12. **Interactive elements** — If the page has:
    - Package builder → toggle switches, running total, pre-fill form CTA
    - DJ booking wizard → hour selector, running total
    - Proposal form → 6 fields max, inline validation, appropriate input types
    - Audio player → play/pause, progress bar

13. **Apply pricing psychology** — From marketing-psychology-pricing.md:
    - Anchoring (show premium first)
    - Charm pricing (€199, €599, €149)
    - Price partitioning (show components)
    - Social proof near CTA
    - Scarcity where true

### Phase 4: Quality Assurance (never skip)

14. **Run `/impeccable:audit`** — Technical quality audit on the built page. Fix all issues found.

15. **Run `/impeccable:typeset`** — Fix any typography issues (Bebas Neue headings, Space Grotesk body, scale, spacing).

16. **Run `/impeccable:arrange`** — Fix any layout and spacing issues.

17. **Run `/impeccable:polish`** — Final design pass before shipping.

18. **CRO checklist** — Score the page against the 55-item checklist from `knowledge-cro-checklist.md`:
    - Above-Fold Clarity (20%)
    - Trust & Credibility (15%)
    - Copy & Messaging (15%)
    - CTA & Form Design (20%)
    - Visual Design (10%)
    - Mobile Experience (10%)
    - Page Speed (10%)
    - Report the Landing Page Score (0-100)

19. **Brand check** — Verify against brand-voice.md:
    - [ ] Correct segment tone (premium / accessible / energy)
    - [ ] Party Booth (not iPad Photobooth)
    - [ ] PicYourBooth (not Pic Your Moment)
    - [ ] No red (#ff494a) or pink (#e839a0)
    - [ ] Dutch copy sounds native (not translated)
    - [ ] Gold buttons have black text
    - [ ] Charm pricing used

### Phase 5: Deliver

20. **Output the complete page** — Production-ready HTML/CSS/Tailwind code with:
    - All sections built
    - Responsive behavior documented
    - Accessibility notes
    - Landing Page Score
    - Any remaining recommendations

## Rules

- **Never skip Phase 1** — context loading is mandatory, even if you "already know" the brand
- **Never skip Phase 4** — quality assurance catches what humans miss
- **Always use PYB design tokens** — never invent colors or fonts
- **Always check the PRD** — it has the canonical page spec
- **Mobile-first** — build for mobile, enhance for desktop
- **Dutch copy** — all customer-facing text in Dutch
- **One primary CTA per viewport** — don't compete with yourself
