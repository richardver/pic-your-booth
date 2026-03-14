---
name: landing-page-audit
description: "Audit a landing page for conversion performance using the 55-item CRO checklist. Produces a scored report with prioritized recommendations. Use /landing-page-audit with a URL or page description."
user-invocable: true
context: fork
agent: website-designer
---

# Landing Page Audit

Audit a landing page for conversion rate optimization.

## Process

1. Read `knowledge/website-design-cro.md` for the 55-item checklist and scoring rubric
2. Read `knowledge/website-design-landing-pages.md` for structure best practices
3. Read `knowledge/marketing-psychology-pricing.md` for persuasion principles
4. Evaluate the page section by section against the checklist
5. Score each category (weighted) and calculate overall Landing Page Score (0-100)

## Input

The user will provide a URL to audit, or describe the page structure and content.

## Output

1. **Landing Page Score**: 0-100 (weighted across 7 categories)
2. **Category scores**: Above-Fold, Trust, Copy, CTA/Form, Visual, Mobile, Speed
3. **Top conversion killers**: Ranked by impact
4. **Immediate fixes** (0-48 hours, no dev): Quick wins
5. **Quick wins** (1-2 weeks): Minor effort, meaningful lift
6. **Strategic improvements** (2-6 weeks): Larger changes
7. **Test hypotheses**: A/B test ideas generated from findings
