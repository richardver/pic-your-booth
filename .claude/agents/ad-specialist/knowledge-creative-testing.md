# Creative Testing & Fatigue

Testing framework and fatigue management. Full reference in `.claude/agents/ad-specialist/knowledge-creative-testing-full.md`.

---

## Fatigue Signals

| Signal | Meaning |
|---|---|
| Frequency rises + CTR drops | Fatigue beginning |
| CTR velocity declining | Earliest warning (2-3 days ahead) |
| CPM inflating + CTR drops | Unambiguous fatigue |
| CPA rising + conv rate holds | Spending more to find responsive users |

## Fatigue Thresholds

| Audience Size | Fatigue Begins | Creative Lifespan |
|---|---|---|
| Narrow (<100K) | Frequency 4-6 | 2-3 weeks |
| Medium (100K-1M) | Frequency 6-10 | 3-6 weeks |
| Broad (>1M) | Frequency 10-15 | 6-12 weeks |
| Retargeting | Fastest | Rotate every 1-2 weeks |

## Action Triggers

| Metric | Warning (prepare) | Action (rotate now) |
|---|---|---|
| CTR | Below 80% of baseline | Below 70% of baseline |
| CPM | Above 115% of baseline | Above 130% of baseline |
| Cost per result | Above 120% of baseline | Above 140% of baseline |

## Testing Cadence

- **PYB volume**: Bi-weekly creative refreshes
- **Pipeline**: Brief (day 1) → Production (days 2-3) → Review (day 4) → Launch (day 5) → Monitor (days 6-14) → Analyze (day 15)

## Available Skills

| Task | Invoke Skill |
|---|---|
| Analyze creative performance | `skills/ads/meta/meta-ads-creative-analyzer.md` |
| Design full funnel | `skills/ads/cross-platform/ads-funnel-builder.md` |
| Generate performance reports | `skills/ads/cross-platform/ads-report-generator.md` |

For full testing framework: `.claude/agents/ad-specialist/knowledge-creative-testing-full.md`
For A/B testing methodology: `.claude/agents/ad-specialist/knowledge-ab-testing.md`
