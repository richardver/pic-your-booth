# Agent Architecture

How PYB agents are structured and discovered.

---

## What Agents Are

Agents are **knowledge containers with routing**. They answer "what do you know?" — they hold domain expertise in knowledge files and route queries to the right file via a sub-topic router.

Agents do NOT define workflows or actionable steps — those belong in skills.

---

## Agent Structure

Every PYB agent consists of two parts:

### 1. Native entry point (single file)

```
.claude/agents/<name>.md
```

A thin file with YAML frontmatter (`name`, `description`) and an Operating Manual section pointing to `_index.md`. Spawnable via the `Agent` tool with `subagent_type=<name>`.

### 2. Knowledge directory

```
.claude/agents/<name>/
  _index.md           <- identity, sub-topic router, scope, hard rules
  knowledge-*.md      <- domain knowledge files (one per topic)
```

The `_index.md` is the routing hub. It tells the agent which knowledge file to read for a given topic.

---

## Native Agent `.md` Template

```markdown
---
name: <agent-name>
description: <precise one-liner matching registry Domain Keywords>
---

# <Agent Title>

> <verbatim identity line from _index.md>

## Scope
<2-3 sentences: what it owns, what it does NOT do>

## Operating Manual
Read `.claude/agents/<name>/_index.md` before executing any task.

## Handoff Rules
- Does NOT: <explicit exclusions>
- For <out-of-scope need>: call <agent-name> agent
```

---

## Agent Registry

`.claude/agents/_registry.md` is the master routing table. It maps:
- Agent name → domain keywords → index file
- Helps Claude route user requests to the correct agent

---

## Current PYB Agents

| Agent | Domain | Structure | Keywords |
|---|---|---|---|
| Architect | Infrastructure | Deep (6 knowledge files) | architecture, agents, skills, knowledge, structure, exports |
| Strategist | Strategy & Brand | Deep (10 knowledge files) | vision, USPs, hooks, competition, pricing, growth, brand, orchestration |
| Product Specialist | Product Knowledge | Deep (7 knowledge files) | product, specs, equipment, package, upgrade, pricing |
| Designer | Website & Visual Design | Deep (8 knowledge files) | design, UI, landing page, website, CRO, form, components |
| Social Media | Social & Creative | Deep (7 knowledge files) | social, Instagram, TikTok, DJ profiles, video, content |
| DJ Promoter | DJ Talent Brands & Growth | Deep (3 knowledge files) | DJ brand, DJ Gianni, Milø, voice tags, mixtape art, photo direction, talent, growth |
| Ad Specialist | Paid Advertising | Deep (6 knowledge files + 17 skills) | Meta Ads, Google Ads, campaign, audience, ROAS, PMax, RSA |
| Video Editor | Programmatic Video | Deep (2 knowledge files) | video, Remotion, TikTok, Reels, clip, render, template, 9:16 |
| SEO | Search & LLM Optimization | Deep (7 knowledge files) | SEO, keywords, meta tags, schema, ranking, search, LLM, local SEO |

---

## Agent Communication

- **Hierarchical only** — orchestrator spawns agents, agents return results
- **Context isolation** — each subagent has its own context window
- **Parallel dispatch** — independent tasks can be dispatched simultaneously via multiple `Agent` tool calls

---

## Flat vs Deep Agents

PYB uses a mix:

| Type | Structure | Example |
|---|---|---|
| **Flat** (simple) | Single `.md` file, no subdirectory | (none currently — all agents are deep) |
| **Deep** (complex) | `.md` + subdirectory with `_index.md` + `knowledge-*.md` | architect |

Migrate flat agents to deep structure only when they accumulate enough domain knowledge to warrant multiple knowledge files. Don't over-engineer — a single-file agent is fine for focused domains.
