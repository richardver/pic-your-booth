# Pic Your Booth

Photobooth rental & DJ entertainment brand under **Pic Your Moment BV**, Randstad, Netherlands.

## Project Overview

This repo contains the marketing knowledge base, specialist agents, and skills for Pic Your Booth. No application code — this is the brain behind the brand.

## Services

- **Magic Mirror XL** — Premium photobooth (DSLR, pro lighting, VIP add-ons) from €599
- **iPad Photobooth** — Digital-only, budget-friendly from €200
- **DJ Services** — Combinable with photobooth, Spotify playlist optimization
- **DJ + Photobooth Combo** — One team, one vibe, one booking

## Team

- **Richard** — Owner (business, tech, marketing)
- **Luca** — Photobooth operator & DJ (DJ Gianni: meezingers, afro, dance)
- **Milo** — Photobooth operator & DJ (house, techno)

## Funnel

Meta Ads → Website → Proposal Form → Send Proposal → Event Booked

## Tech Stack

WordPress, HubSpot, Zapier, Meta Ads, Google Analytics, Google Workspace

## Project Structure

```
pic-your-booth/
├── CLAUDE.md                              ← You are here (loaded every session)
├── .claude/
│   ├── agents/                            ← Specialist agents (auto-discovered)
│   │   ├── brand-guardian.md              — Brand quality gate
│   │   ├── designer.md                   — UI/UX, visual design, frontend
│   │   ├── meta-ads-specialist.md        — Meta Ads campaigns & copy
│   │   ├── social-creative.md            — Social media content & DJ profiles
│   │   └── website-designer.md           — WordPress pages, CRO, forms
│   ├── skills/                            ← Invocable with /skill-name
│   │   ├── brand-audit/SKILL.md          — /brand-audit
│   │   ├── landing-page-audit/SKILL.md   — /landing-page-audit
│   │   ├── ad-campaign/SKILL.md          — /ad-campaign
│   │   └── content-plan/SKILL.md         — /content-plan
│   └── rules/
│       └── brand-voice.md                — Always-active brand voice rules
│
├── knowledge/
│   ├── brand/                             ← Brand identity
│   │   └── brand.md                      — Mission, vision, tone, segments, positioning
│   ├── dj-profiles/                       ← DJ personal brands
│   │   └── luca-dj-gianni.md             — DJ Gianni brand, music style, social bios
│   ├── photobooth/                        ← Website & conversion
│   │   ├── website-design-landing-pages.md — Page structure, hero formulas, CTAs
│   │   ├── website-design-cro.md         — 55-item audit checklist, scoring rubric
│   │   └── landing-page-forms-personalization.md — Forms, personalization, email sequences
│   ├── marketing/                         ← Ads, social, psychology
│   │   ├── meta-ads.md                   — Campaign structure, audiences, benchmarks
│   │   ├── ad-copy-frameworks.md         — Copy specs, hooks, testing methodology
│   │   ├── creative-testing-and-fatigue.md — Testing framework, fatigue management
│   │   ├── social-creatives.md           — Platform guides, content pillars, specs
│   │   ├── video-marketing.md            — Video specs, production, distribution
│   │   ├── marketing-psychology-pricing.md — Anchoring, Cialdini, Fogg, objections
│   │   ├── marketing-psychology-buyer-journey.md — JTBD, journey map, psychographics
│   │   ├── marketing-psychology-viral-retention.md — Viral loops, referrals, retention
│   │   └── ab-testing.md                 — ICE framework, sample sizes, test methodology
│   └── design/                            ← UI/UX & design system
│       ├── design-system.md              — Tokens, colors, typography, components
│       ├── ui-ux-principles.md           — UX guidelines, accessibility, responsive
│       ├── pym-design-tokens.json        — Design token values (JSON)
│       ├── pym-design-system-web.html    — PYM parent design system
│       ├── pym-design-system-photobooth.html — Photobooth design system (dark+light)
│       └── pym-design-system-dj.html     — DJ Hub design system (split-energy)
```

## Quick Commands

- `/brand-audit` — Check any content against PYB brand guidelines
- `/landing-page-audit` — Full CRO audit with scored report
- `/ad-campaign` — Create a complete Meta Ads campaign
- `/content-plan` — Generate a social media content calendar
