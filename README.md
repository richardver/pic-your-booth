# PicYourBooth

Knowledge base and AI-powered marketing system for **PicYourBooth** — premium photobooth & DJ entertainment, Randstad, Netherlands.

## What This Repo Is

This is not an application — it's a **knowledge-driven marketing workspace** powered by Claude Code. It contains brand knowledge, marketing frameworks, design systems, and AI agents that work together to create campaigns, content, designs, and audits.

## Services

| Service | Starting Price | Description |
|---------|---------------|-------------|
| **Party Booth** | €199 | Digital photobooth, self-service, fun for every budget |
| **Magic Mirror XL** | €599 | Premium DSLR photobooth with pro lighting and printing |
| **DJs** | €149 | DJ Gianni (Afro/Caribbean/Hits) & Milo (House/Techno) |

All prices include 21% BTW. Combo packages available.

## AI Agents

Six specialist agents handle different domains:

| Agent | Domain | What It Does |
|-------|--------|-------------|
| **Architect** | Infrastructure | Repo architecture, agent/skill patterns, knowledge structure |
| **Product Specialist** | Products | Specs, packages, upgrades, pricing (source of truth) |
| **Designer** | Website & Visual | Website pages, landing pages, CRO, UI components, frontend code |
| **Social Media** | Social & Creative | Content plans, video scripts, DJ profiles, social graphics |
| **Strategist** | Strategy & Brand | Vision, USPs, hooks, competition, pricing strategy, brand quality gate, orchestrates other agents |
| **Ad Specialist** | Paid Advertising | Meta Ads + Google Ads campaigns, audiences, ad copy, 17 ads skills |
| **SEO** | Search & LLM Optimization | Keywords, meta tags, structured data, LLM discoverability, local SEO |

Agents are routed via `.claude/agents/_registry.md`.

## Quick Commands

```
/brand-audit        Check any content against PYB brand guidelines
/landing-page-audit Full CRO audit with scored report (55-item checklist)
/ad-campaign        Create a complete Meta Ads campaign (Dutch copy)
/content-plan       Generate a social media content calendar
/product-info       Look up product specs, packages, and pricing
/design-page        Design a complete website page (full knowledge stack + QA)
/design-landingpage Design a conversion-optimized landing page for Meta Ads
```

## Repo Structure

```
pic-your-booth/
├── CLAUDE.md              → Claude Code project instructions
├── README.md              → You are here
├── docs/
│   ├── plans/             → Brainstorm sessions, design docs, implementation plans
│   ├── templates/         → Visual templates & assets
│   │   ├── design-system/ → HTML design systems, tokens JSON
│   │   ├── website/       → 5 page templates (homepage, magic-mirror, party-booth, djs, offerte)
│   │   ├── djs/           → DJ Gianni (brand, social, photos) + Milo
│   │   └── ads/meta/      → Meta Ads design system
│   ├── marketing/         → Shared psychology frameworks
│   ├── website/           → PRD, CRO checklist, landing page frameworks
│   └── export-guide.md    → Playwright export workflow
└── .claude/
    ├── agents/            → 6 AI agents (5 deep, 1 flat)
    ├── skills/            → 8 PYB skills + 21 Impeccable + 17 ads skills
    └── rules/             → Always-active brand voice rules
```

## How It Works

1. **Ask a question or give a task** — Claude routes to the right agent based on keywords
2. **Agent loads its knowledge** — reads `_index.md` → finds the right `knowledge-*.md` file
3. **Agent executes** — produces content, designs, audits, or campaigns grounded in PYB knowledge
4. **Skills for repeatable workflows** — `/ad-campaign` runs a structured multi-step process

## Design System

Dark cinematic aesthetic. Three-layer hierarchy:

1. **Web parent** (`pyb-design-system-web.html`) — shared tokens, components
2. **Page-specific** — photobooth pages, DJ hub, Meta Ads
3. **Individual DJ brands** — DJ Gianni (coral), Milo (cyan)

Fonts: Bebas Neue (headings) + Space Grotesk (body). Colors: gold (#f59e42) for photobooth, violet (#8b5cf6) for DJ, dark bg (#08080b).

## Design Asset Exports

All visual assets exported via Playwright. See `.claude/agents/architect/knowledge-exports-guide.md`.

## Setup

### Required Plugins

Install these Claude Code plugins before working in this repo:

```bash
/plugin superpowers                    # Workflow skills: planning, parallel agents, code review
/plugin playwright                     # Browser automation for design asset exports
/plugin security-guidance              # Security best practices
/plugin marketplace add pbakaus/impeccable  # 20 design quality skills for frontend work
```

After installing, run `/reload-plugins` to activate.

### Impeccable Design Skills

The designer agent uses [Impeccable](https://impeccable.style) for frontend quality. Key commands:

| Command | Purpose |
|---------|---------|
| `/audit` | Technical quality audit before shipping |
| `/polish` | Final design pass |
| `/typeset` | Fix typography issues |
| `/arrange` | Fix layout and spacing |
| `/bolder` / `/quieter` | Adjust visual intensity |
| `/animate` | Add motion and transitions |
| `/overdrive` | Technically extraordinary effects (beta) |

Full list: 20 skills across Diagnostic, Quality, Intensity, Enhancement, Adaptation, and System categories.

### Verify

After setup, these should all be available:
- `/brand-audit`, `/landing-page-audit`, `/ad-campaign`, `/content-plan`, `/product-info` (PYB skills)
- `superpowers:*` skills (planning, dispatching, verification)
- Impeccable skills (`/audit`, `/polish`, `/typeset`, etc.)
- Playwright MCP tools (browser navigation, screenshots, form filling)

## Team

| Name | Role |
|------|------|
| **Richard** | Owner — business, tech, marketing |
| **Luca** | Photobooth operator & DJ (DJ Gianni) |
| **Milo** | Photobooth operator & DJ |

## Legal

**PicYourBooth** is a standalone brand. Legal entity: Pic Your Moment BV (invoices only, never in marketing).
