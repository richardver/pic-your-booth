# PicYourBooth

Premium photobooth & DJ entertainment brand. Standalone brand under Pic Your Moment BV (legal entity, invoices only). Randstad, Netherlands.

## Services

- **Party Booth** - Digital photobooth, vanaf €199
- **Magic Mirror XL** - Premium DSLR photobooth, vanaf €599
- **DJs** - DJ Gianni (Afro Beats, Caribbean, Nederlands Hits) & Milo (House, Techno), vanaf €149

## Team

- **Richard** - Owner (business, tech, marketing)
- **Luca** - Photobooth operator & DJ (DJ Gianni)
- **Milo** - Photobooth operator & DJ

## Funnel

Meta Ads → Website → Proposal Form → Send Proposal → Event Booked

## Tech Stack (planned)

Next.js + Tailwind CSS + Vercel + HubSpot + Meta Ads + Google Analytics

## Python Tooling (`.venv`)

Python 3.14 venv at project root for image processing (Pillow), Gemini AI (google-generativeai/google-genai), and automation. See `knowledge-organization.md` for full package list.

## Knowledge Architecture

Three layers in `.claude/`:
- **`agents/`** — 6 domain agents with routing registry (`_registry.md`), strategist orchestrates
- **`skills/`** — Actionable workflows invoked via `/commands`
- **`rules/`** — Always-active rules (brand voice)

Agent registry: `.claude/agents/_registry.md`

**Routing:** user request → keyword match → agent → agent loads knowledge → executes.

**Agents are knowledge containers** — they answer "what do you know?" Skills are actionable workflows — they answer "how do you do X?" Don't create a skill if there are no steps to execute.

## Project Structure

```
pic-your-booth/
├── CLAUDE.md                              ← You are here
├── .venv/                                 ← Python 3.14 tooling (Pillow, Gemini, etc.)
├── docs/
│   ├── plans/                            - PRD, brainstorm sessions, design documents
│   ├── website/                          - Website & design assets
│   │   ├── deployment/                  - Live website HTML pages (DO NOT MOVE)
│   │   │   └── assets/images/          - Optimized images served by website
│   │   ├── design-system/              - HTML design systems, tokens JSON
│   │   └── djs/                        - DJ brand guides & assets
│   │       ├── dj-gianni/             - Brand guide, social/, photos/
│   │       └── milo/                  - Brand guide, profile
│   ├── images/                          - All image assets
│   │   ├── photos-source/             - Original photos + INDEX.md (catalogue with Gemini picks)
│   │   │   ├── magicmirror/           - Magic Mirror XL photos (photobooth, USPs, upgrades)
│   │   │   ├── partybooth/            - Party Booth photos (product, USPs, upgrades)
│   │   │   └── dj/                    - DJ photos
│   │   ├── generated/                 - AI-generated & processed images
│   │   ├── web/                       - Optimized WebP for website
│   │   └── screenshots/              - Dev screenshots
│   ├── ads/                             - Ad design & assets
│   │   └── meta/                      - Meta Ads design system HTML
│   ├── kpi/                             - Historical KPI Excel reports (Vizibooth 2025, 2026)
│   └── funnel/                          - Funnel strategy & campaign management
│       ├── campaigns/                 - Campaign specs, audiences, ad copy per month
│       ├── creatives/                 - Creative briefs, HTML mockups
│       ├── tracking/                  - Pixel setup, KPIs, conversion tracking
│       └── results/                   - Test results, optimization logs, winner data
├── .claude/
│   ├── agents/
│   │   ├── _registry.md                  - Master routing table (all agents)
│   │   ├── architect.md                  - Architecture, agents, skills, knowledge structure
│   │   ├── architect/                    - Architect knowledge directory
│   │   │   ├── _index.md                - Sub-topic router
│   │   │   ├── knowledge-agents.md      - Agent architecture patterns
│   │   │   ├── knowledge-skills.md      - Skill architecture patterns
│   │   │   ├── knowledge-organization.md - Knowledge folder structure
│   │   │   ├── knowledge-design-systems.md - Design system hierarchy
│   │   │   └── knowledge-exports.md     - Playwright export workflows
│   │   ├── product-specialist.md          - Product specs, packages, pricing
│   │   ├── product-specialist/            - Product knowledge directory
│   │   │   ├── _index.md                - Sub-topic router
│   │   │   ├── knowledge-party-booth.md - Party Booth specs, upgrades
│   │   │   ├── knowledge-magic-mirror.md - Magic Mirror XL specs, upgrades
│   │   │   ├── knowledge-dj-services.md - DJ Gianni, Milo, Spotify, equipment
│   │   │   └── knowledge-pricing.md     - All pricing, combos, rules
│   │   ├── designer.md                    - Website + visual design, CRO, frontend
│   │   ├── designer/                      - Designer knowledge directory
│   │   │   ├── _index.md                - Sub-topic router
│   │   │   ├── knowledge-design-system.md - Colors, tokens, typography, visual modes
│   │   │   ├── knowledge-website.md     - Page templates, forms, CRO checklist
│   │   │   └── knowledge-ux.md          - Accessibility, responsive, visual hierarchy
│   │   ├── social-media.md                - Social content, DJ profiles, social graphics
│   │   ├── social-media/                  - Social media knowledge directory
│   │   │   ├── _index.md                - Sub-topic router
│   │   │   ├── knowledge-platforms.md   - Platform strategy, specs, content pillars
│   │   │   ├── knowledge-video.md       - Video scripting, hooks, production
│   │   │   ├── knowledge-dj-gianni.md   - DJ Gianni profile, brand, assets
│   │   │   ├── knowledge-dj-milo.md     - Milo profile, brand, assets
│   │   │   └── knowledge-viral-retention.md - Viral loops, referrals, post-event
│   │   ├── strategist.md                  - Strategy, brand, orchestration
│   │   ├── strategist/                    - Strategist knowledge (10 files)
│   │   │   ├── _index.md                - Router + orchestration pattern
│   │   │   ├── knowledge-brand.md       - Mission, vision, identity, tone
│   │   │   ├── knowledge-voice.md       - Voice rules, do's/don'ts
│   │   │   ├── knowledge-review.md      - Brand audit checklist
│   │   │   ├── knowledge-segments.md    - Buyer segments, pain points, JTBD (NL)
│   │   │   ├── knowledge-usps.md        - USP matrix per product/segment (NL)
│   │   │   ├── knowledge-hooks.md       - Hooks library (NL, per segment/platform)
│   │   │   ├── knowledge-competition.md - Competitive landscape photobooth + DJ NL
│   │   │   ├── knowledge-competition-references.md - Raw intel, URLs, pricing
│   │   │   ├── knowledge-pricing-strategy.md - Why we price this way
│   │   │   └── knowledge-growth.md      - Growth priorities, phased roadmap
│   │   ├── ad-specialist.md              - Paid ads (Meta + Google)
│   │   └── ad-specialist/                 - Ad specialist knowledge directory
│   │       ├── _index.md                - Sub-topic router + 17 ads skills index
│   │       ├── knowledge-pyb-campaigns.md - PYB campaign architecture, budgets, targets
│   │       ├── knowledge-meta-ads.md    - Meta Ads strategy, audiences, benchmarks
│   │       ├── knowledge-google-ads.md  - Google Ads search, PMax, keywords
│   │       ├── knowledge-ad-copy.md     - Hooks, frameworks, testing
│   │       └── knowledge-creative-testing.md - Fatigue, lifecycle, refresh
│   │   ├── seo.md                         - SEO & LLM optimization
│   │   └── seo/                           - SEO knowledge (6 files)
│   │       ├── _index.md                - Keyword map, audit rules
│   │       ├── knowledge-keywords.md    - Focus keywords per page, long-tail
│   │       ├── knowledge-technical-seo.md - Meta tags, schema, performance
│   │       ├── knowledge-on-page.md     - Headings, content, internal links
│   │       ├── knowledge-llm-optimization.md - AI answer visibility, FAQ schema
│   │       ├── knowledge-competition-seo.md - Competitor rankings, gaps
│   │       └── knowledge-local-seo.md   - Google Business, city pages, reviews
│   ├── skills/
│   │   ├── brand-audit/SKILL.md          - /brand-audit
│   │   ├── seo-audit/SKILL.md            - /seo-audit (SEO + LLM audit)
│   │   ├── landing-page-audit/SKILL.md   - /landing-page-audit
│   │   ├── ad-campaign/SKILL.md          - /ad-campaign (Meta + Google)
│   │   ├── ads/                          - 17 ads skills from labofideas/ads-skills
│   │   │   ├── google/                  - 6 Google Ads skills (audit, RSA, PMax, etc.)
│   │   │   ├── meta/                    - 6 Meta Ads skills (copy, audience, pixel, etc.)
│   │   │   └── cross-platform/          - 5 cross-platform (funnel, reports, video)
│   │   ├── content-plan/SKILL.md         - /content-plan
│   │   ├── product-info/SKILL.md         - /product-info
│   │   ├── design-page/SKILL.md          - /design-page (full page design workflow)
│   │   ├── design-landingpage/SKILL.md   - /design-landingpage (conversion-optimized landing page)
│   │   └── impeccable/                   - 21 Impeccable design skills (designer agent)
│   │       ├── frontend-design/          - Enhanced frontend design + references
│   │       ├── audit, critique           - Diagnostic
│   │       ├── polish, normalize,        - Quality
│   │       │   optimize, harden
│   │       ├── bolder, quieter, distill  - Intensity
│   │       ├── animate, colorize,        - Enhancement
│   │       │   delight, clarify
│   │       ├── adapt, onboard            - Adaptation
│   │       ├── extract, typeset, arrange - System
│   │       ├── overdrive                 - Beta
│   │       └── teach-impeccable          - Project context setup
│   └── rules/
│       └── brand-voice.md                - Always-active brand voice rules
```

## Quick Commands

- `/brand-audit` - Check any content against PYB brand guidelines
- `/landing-page-audit` - Full CRO audit with scored report
- `/ad-campaign` - Create a complete Meta Ads campaign
- `/content-plan` - Generate a social media content calendar
- `/product-info` - Look up product specs, packages, and pricing
- `/design-page` - Design a complete website page using full knowledge stack
- `/design-landingpage` - Design a conversion-optimized landing page for Meta Ads traffic
- `/seo-audit` - SEO & LLM optimization audit with scoring

## Design Asset Exports

Always use Playwright for exports. See `.claude/agents/architect/knowledge-exports-guide.md` for workflow.
