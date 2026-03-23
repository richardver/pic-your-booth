# Agent Registry

## Architecture

```
.claude/
  agents/      Domain agents — each owns a domain, declares its knowledge + scope
  skills/      Executable skills — actionable workflows invoked via /commands
  rules/       Always-active rules (brand voice)
docs/          All reference material (brand, design, marketing, website, DJ profiles)
docs/          Project documentation (PRD, export guide)
```

Routing: user request -> keyword match -> agent -> agent loads knowledge + executes.

## Master Routing Table

| Agent | Domain | Keywords | File | Tools |
|---|---|---|---|---|
| Architect | Infrastructure | architecture, agents, skills, knowledge, structure, exports, design systems, Claude Code config | `architect.md` | Read, Grep, Glob, Bash, Write, Edit |
| Designer | Website & Visual Design | design, UI, landing page, HTML, CSS, components, mockup, template, visual, frontend, website, page, form, funnel, conversion, CRO, wireframe | `designer.md` | Read, Grep, Glob, Bash, Write, Edit |
| Social Media | Social & Creative | social, Instagram, TikTok, Facebook, content, DJ profiles, captions, video scripts, social graphics, templates | `social-media.md` | Read, Grep, Glob, Bash, Write, Edit |
| Strategist | Strategy & Brand | vision, mission, pain points, USPs, hooks, competition, pricing strategy, growth, brand, tone, voice, audit, segments, orchestrate, campaign planning | `strategist.md` | Read, Grep, Glob, Bash, Write, Edit |
| Ad Specialist | Paid Advertising | Meta Ads, Google Ads, Facebook, Instagram, campaign, audience, ROAS, CPA, targeting, search, PMax, RSA, pixel, funnel | `ad-specialist.md` | Read, Grep, Glob |
| Product Specialist | Product Knowledge | product, specs, equipment, package, upgrade, pricing, Party Booth, Magic Mirror, DJ, Spotify, what's included | `product-specialist.md` | Read, Grep, Glob |

## Domain Routing Matrix

| Domain | Data/Analysis | Writing/Copy | Visual/Design | Architecture |
|---|---|---|---|---|
| Website | Designer | Designer | Designer | Architect |
| Ads | Ad Specialist | Ad Specialist | Designer | Architect |
| Social | Social Media | Social Media | Social Media | Architect |
| DJ Profiles | Social Media | Social Media | Social Media | Architect |
| Strategy & Brand | Strategist | Strategist | Designer | Architect |
| Products | Product Specialist | Product Specialist | Designer | Architect |

## Funnel Coverage

| Stage | Primary Agents | Goal |
|---|---|---|
| **Awareness** | Strategist → Ad Specialist, Social Media | Reach target audience |
| **Consideration** | Strategist → Designer, Ad Specialist | Convert visitors to form submissions |
| **Proposal** | Designer | Smooth proposal form experience |
| **Booking** | Strategist | Consistent, professional communication |
