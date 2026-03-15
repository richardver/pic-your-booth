---
name: ad-campaign
description: "Create a complete Meta Ads campaign - structure, audiences, ad copy (Dutch), creative briefs, budget allocation, and testing plan. Use /ad-campaign to design a new campaign or optimize an existing one."
user-invocable: true
context: fork
agent: meta-ads-specialist
---

# Ad Campaign Creator

Design a complete Meta Ads campaign for Pic Your Booth.

## Process

1. Read `knowledge/brand/brand.md` for brand context
2. Read `knowledge/marketing/meta-ads.md` for campaign structure and benchmarks
3. Read `knowledge/marketing/ad-copy-frameworks.md` for copy specs and hook formulas
4. Ask which segment to target (Magic Mirror / iPad / DJ Combo / All)
5. Build campaign structure, audiences, copy, and testing plan

## Input

The user will specify:
- Which service/segment to promote
- Budget (or use default recommendations)
- Any seasonal context (wedding season, holidays, etc.)
- Whether this is a new campaign or optimization of existing

## Output

1. **Campaign structure** - campaigns, ad sets, audiences
2. **Budget allocation** - per campaign and ad set
3. **Ad copy** - 3-4 variations per ad set, full Dutch text
4. **Creative briefs** - visual direction per ad
5. **Testing plan** - what to test, timeline, success criteria
6. **KPI targets** - CPL, CTR, CPC targets with action thresholds
