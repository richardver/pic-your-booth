# Skill Architecture

How PYB skills are structured, when to create them, and how they relate to agents.

---

## What Skills Are

Skills are **pre-programmed actionable workflows**. They answer "how do you do X?" — they define step-by-step procedures, checklists, or SOPs that an agent can execute.

Skills are NOT knowledge containers. If there are no steps to execute, there is no skill to create.

---

## Agents vs Skills

| | Agent | Skill |
|---|---|---|
| **Purpose** | Knowledge container with routing | Actionable workflow / SOP |
| **Answers** | "What do you know about X?" | "How do you do X?" |
| **Structure** | `_index.md` + `knowledge-*.md` files | `SKILL.md` with steps/checklist |
| **Invocation** | Dispatched as subagent via `Agent` tool | Invoked via `/skill-name` in Claude Code |
| **Required?** | Every domain needs an agent | Only when there's a real workflow |

---

## Skill Structure

Skills live in `.claude/skills/`:

```
.claude/skills/<skill-name>/SKILL.md
```

For agent-owned sub-skills:
```
.claude/skills/<agent-name>/skills/<skill-name>/SKILL.md
```

### SKILL.md Format

```markdown
---
name: <skill-name>
description: <when to use this skill - specific enough for Claude to auto-match>
user_invocable: true
---

# <Skill Title>

<Brief intro - what this skill does, prerequisites>

## Steps

1. **Step one** - ...
2. **Step two** - ...
```

Key fields:
- `name`: used as the `/command` name
- `description`: Claude uses this to decide when to invoke the skill — be specific
- `user_invocable: true`: makes the skill available as a `/slash-command`

---

## Current PYB Skills

| Skill | Command | Purpose |
|---|---|---|
| Brand Audit | `/brand-audit` | Check content against PYB brand guidelines |
| Landing Page Audit | `/landing-page-audit` | Full CRO audit with scored report |
| Ad Campaign | `/ad-campaign` | Create complete Meta Ads campaign |
| Content Plan | `/content-plan` | Generate social media content calendar |

---

## When to Create a Skill

**Create a skill when:**
- There's a repeatable multi-step procedure
- The steps reference standards from knowledge files but add an execution order
- You find yourself doing the same multi-step task repeatedly

**Do NOT create a skill when:**
- It would just be a redirect to an agent (use the agent directly)
- The "skill" has no steps — just information
- It's a one-time task

---

## Skill Routing — When NOT to Use

Simple data lookups bypass skill routing entirely. Skills are for **multi-step domain tasks** that require structured execution, not single questions.
