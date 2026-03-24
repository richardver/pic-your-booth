# Meta Ads

Meta Ads strategy, audiences, specs, and benchmarks. Full reference in `.claude/agents/ad-specialist/knowledge-meta-ads-full.md`.

---

## Key Concepts

- **CBO vs ABO**: CBO for prospecting (3+ ad sets), ABO for retargeting (fixed budgets)
- **Advantage+ Audience**: ML-driven, outperforms manual in 60-70% of tests — use as default
- **CAPI**: Server-side event tracking, event match quality >6.0, deduplicate with Pixel
- **20% Rule**: Never increase budget more than 20% every 3-5 days

## Available Skills

| Task | Invoke Skill |
|---|---|
| Write ad copy | `skills/ads/meta/meta-ads-ad-copy.md` |
| Audit Advantage+ campaigns | `skills/ads/meta/meta-ads-asc-auditor.md` |
| Build audiences | `skills/ads/meta/meta-ads-audience-builder.md` |
| Analyze creative performance | `skills/ads/meta/meta-ads-creative-analyzer.md` |
| Optimize hooks | `skills/ads/meta/meta-ads-hook-optimizer.md` |
| Audit pixel/tracking | `skills/ads/meta/meta-ads-pixel-auditor.md` |

## Benchmarks (NL Market)

| Metric | Prospecting | Retargeting |
|---|---|---|
| CTR | 0.8-1.5% | 1.5-3.0% |
| CPC | €0.60-€2.00 | €0.30-€1.00 |
| CPM | €8-€18 | €10-€25 |
| Conv Rate | 1-3% | 4-10% |
| Frequency (healthy) | < 3.0 | < 6.0 |

## PYB Budget & Targets

- **€500/month** split test: €250 Magic Mirror XL + €250 Party Booth
- **ROAS target: >4.0x** (Vizibooth 2025 avg was 4.5x)
- All Meta Ads in Phase 1 — Google Ads in Phase 2
- Full funnel: `docs/funnel/funnel-design.md`

For full Meta Ads reference: `.claude/agents/ad-specialist/knowledge-meta-ads-full.md`
