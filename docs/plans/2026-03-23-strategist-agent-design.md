# Strategist Agent — Design Document

**Date:** 2026-03-23
**Status:** Approved
**Author:** Richard + Claude

---

## Overview

Create a strategist agent that replaces the brand agent and becomes PYB's single strategic brain. Owns what PYB says, why, and to whom — then orchestrates other agents with strategic context.

## Decision Log

- Strategist is an **orchestrator** (option C) — coordinates multi-agent work with strategy context
- **Replaces brand agent** (option A) — absorbs brand knowledge, brand audit becomes a skill not an agent
- Pricing **strategy** owned by strategist, pricing **list** stays with product-specialist
- All customer-facing text in **Dutch**
- Competition stored as **reference only** — never copy, only suggest improvements
- PYB positioning/offering is **sacred** — strategist doesn't change it, only suggests where to improve

## Knowledge Files (10)

| # | File | Content | Build Method |
|---|---|---|---|
| 1 | `knowledge-brand.md` | Mission, vision, why, personality, tone | Move from brand agent |
| 2 | `knowledge-voice.md` | Voice rules, do's/don'ts, segment tone map | Move from brand agent |
| 3 | `knowledge-review.md` | Brand audit checklist, flagging rules | Move from brand agent |
| 4 | `knowledge-segments.md` | Buyer segments, psychographics, pain points, JTBD — all Dutch | Build from existing + expand |
| 5 | `knowledge-usps.md` | USP matrix per product per segment, ranked — Dutch | Build new |
| 6 | `knowledge-hooks.md` | PYB-specific hooks library — Dutch, by segment + platform | Build new |
| 7 | `knowledge-competition.md` | Competitive landscape photobooth + DJ NL, where we win/lose | Web research |
| 8 | `knowledge-competition-references.md` | Raw intel — URLs, pricing, offerings per competitor | Web research |
| 9 | `knowledge-pricing-strategy.md` | Why we price this way, competitive context, when to adjust | Build new |
| 10 | `knowledge-growth.md` | Growth priorities, focus now vs later, strategic roadmap | Build new |

## Orchestration Pattern

```
User request
  → Strategist loads relevant strategy context
  → Builds strategic brief (segment + pain points + USPs + hooks + competition)
  → Dispatches domain agent(s) with brief
  → Reviews output via /brand-audit
```

## What Changes

### Delete
- `.claude/agents/brand.md` — replaced by strategist
- `.claude/agents/brand/` — knowledge moves to strategist

### Create
- `.claude/agents/strategist.md` — agent entry point
- `.claude/agents/strategist/_index.md` — router with 10 knowledge files
- `.claude/agents/strategist/knowledge-*.md` — 10 knowledge files
- 7 new knowledge files (segments, usps, hooks, competition x2, pricing-strategy, growth)

### Update
- `.claude/agents/_registry.md` — replace Brand with Strategist
- `.claude/skills/brand-audit/SKILL.md` — route to strategist
- All agent handoffs — "brand agent" → "strategist agent"
- `CLAUDE.md` — project structure
- `README.md` — agent table

## Web Research Required

### Photobooth Market ("photobooth huren")
- Top 5-10 competitors in NL/Randstad
- For each: URL, pricing, packages, USPs, visual quality, weaknesses

### DJ Market ("dj huren")
- Top 5-10 competitors in NL/Randstad
- For each: URL, pricing, services, USPs, weaknesses

## Rules

1. Dutch for all customer-facing content (hooks, USPs, pain points)
2. Never change PYB positioning/offering — only suggest improvements
3. Competition is reference — store and analyze, don't copy
4. Strategist loads context before dispatching — never dispatch blind
5. Pricing strategy separate from price list (product-specialist owns the list)
