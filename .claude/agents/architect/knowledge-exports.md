# Export Workflows

How PYB exports design assets from HTML design systems.

---

## Tool: Playwright

All design asset exports use Playwright. Never use screenshot tools or browser extensions.

Full workflow documented in `.claude/agents/architect/knowledge-exports-guide.md`.

---

## Export Flow

1. **Serve the HTML file** — `npx serve` or Python HTTP server
2. **Run Playwright script** — captures specific elements at defined dimensions
3. **Output to `docs/images/`** (for PNGs) or **`docs/website/`** (for design systems)

---

## Common Exports

| Asset | Source | Output | Dimensions |
|---|---|---|---|
| SoundCloud banner | `docs/website/djs/dj-gianni/social/dj-gianni-social-templates.html` | `docs/images/generated/dj-gianni-soundcloud-banner.png` | 2480x520 |
| Mixtape cover | `docs/website/djs/dj-gianni/social/dj-gianni-social-templates.html` | `docs/images/generated/dj-gianni-afro-mixtape-cover.png` | 1400x1400 |

---

## Rules

1. **Always Playwright** — the canonical export method
2. **Exported PNGs go to `docs/images/`** — design system HTML stays in `docs/website/`
3. **Reference `.claude/agents/architect/knowledge-exports-guide.md`** — for the detailed step-by-step workflow
4. **Re-export after any HTML change** — keep PNGs in sync with source
