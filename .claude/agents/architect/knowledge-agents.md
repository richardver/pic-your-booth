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
| Architect | Infrastructure | Deep (5 knowledge files) | architecture, agents, skills, knowledge, structure, exports |
| Product Specialist | Product Knowledge | Deep (4 knowledge files) | product, specs, equipment, package, upgrade, pricing |
| Designer | Website & Visual Design | Deep (3 knowledge files) | design, UI, landing page, website, CRO, form, components |
| Social Media | Social & Creative | Deep (5 knowledge files) | social, Instagram, TikTok, DJ profiles, video, content |
| Brand Guardian | Brand Compliance | Flat | brand, tone, voice, review, audit, compliance |
| Ad Specialist | Paid Advertising | Deep (5 knowledge files + 17 skills) | Meta Ads, Google Ads, campaign, audience, ROAS, PMax, RSA |

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
| **Flat** (simple) | Single `.md` file, no subdirectory | brand, social-creative |
| **Deep** (complex) | `.md` + subdirectory with `_index.md` + `knowledge-*.md` | architect |

Migrate flat agents to deep structure only when they accumulate enough domain knowledge to warrant multiple knowledge files. Don't over-engineer — a single-file agent is fine for focused domains.
