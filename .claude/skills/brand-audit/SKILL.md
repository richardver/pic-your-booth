---
name: brand-audit
description: "Review marketing content for brand consistency, tone alignment, and messaging quality. Use /brand-audit to check any copy, ad, design, or social post against PYB brand guidelines."
user-invocable: true
context: fork
agent: brand-guardian
---

# Brand Audit

Review the provided content against Pic Your Booth brand guidelines.

## Process

1. Read `knowledge/brand/brand.md` for the full brand guide
2. Identify which segment the content targets (Magic Mirror / iPad / DJ Combo)
3. Score the content on: tone, messaging, CTA clarity, value proposition, Dutch quality
4. Provide Pass / Revise / Reject verdict with specific feedback

## Input

The user will provide content to review — this could be ad copy, a landing page, social post, email, or proposal text.

## Output

1. **Verdict**: Pass / Revise / Reject
2. **Brand alignment score**: 1-10
3. **Segment match**: Which segment does this target?
4. **Feedback**: What to fix, with suggested alternatives
5. **Opportunities**: Ways to strengthen the brand message
