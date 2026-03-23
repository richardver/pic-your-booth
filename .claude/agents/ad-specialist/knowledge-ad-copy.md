# Ad Copy

Frameworks, hooks, and testing for ad copy. Full reference in `.claude/agents/ad-specialist/knowledge-ad-copy-full.md`.

---

## Hook Formulas

1. **Question hook**: "Nog geen photobooth voor je bruiloft?"
2. **Stat hook**: "200+ events in de Randstad"
3. **Story hook**: "Lisa en Tom hadden geen idee dat hun gasten zo gek zouden doen..."
4. **Result hook**: "DSLR kwaliteit foto's die je wilt inlijsten"
5. **This vs That**: "De meeste photobooths zijn een tablet op een stokje. Wij niet."

## Meta Ads Copy Specs

| Element | Limit | Best Practice |
|---|---|---|
| Primary text | 125 visible | Hook in first line |
| Headline | 40 chars | Clear value prop |
| Description | 30 chars | Supporting detail |

## Google Ads RSA Specs

| Element | Limit | Count |
|---|---|---|
| Headline | 30 chars | Up to 15 |
| Description | 90 chars | Up to 4 |
| Display path | 15 chars each | 2 paths |

## Testing Methodology

Priority order: Hook → Value prop → Social proof type → CTA → Offer → Format

- Run each variation 3-5 days minimum
- 100+ clicks per variation for CTR data
- 30+ conversions per variation for CPA data
- One variable at a time

## PYB Ad Copy Rules

- **Dutch** — native NL, not translated English
- **Charm pricing** — €199, €599, €149
- **Party Booth** — never "iPad Photobooth"
- **Segment tone** — premium for Mirror, fun for Party Booth, energy for DJ
- **CTA**: "Check beschikbaarheid" / "Vraag vrijblijvend voorstel aan"

## Available Skills

| Task | Invoke Skill |
|---|---|
| Write Meta ad copy | `skills/ads/meta/meta-ads-ad-copy.md` |
| Optimize hooks | `skills/ads/meta/meta-ads-hook-optimizer.md` |
| Generate Google RSAs | `skills/ads/google/google-ads-rsa-generator.md` |
| Write video ad scripts | `skills/ads/cross-platform/video-ad-script-writer.md` |

For full copy reference: `.claude/agents/ad-specialist/knowledge-ad-copy-full.md`
