# Forecast Skill Design

**Date:** 2026-04-02
**Status:** Approved
**Skill:** `/forecast`

## Overview

Live HubSpot revenue forecast report. Pulls deals from `hubspot-crm` MCP, calculates metrics, generates branded HTML report.

## Invocation

`/forecast` — no arguments needed.

## Data Flow

1. Pull all deals from `hubspot-crm` MCP (`hubspot-list-objects` or `hubspot-search-objects`)
2. Filter to current year by `closedate` (Jan 1 – Dec 31 of current year)
3. Classify each deal: Won (`closedwon`) / Lost (`closedlost`) / Pipeline (everything else)
4. Detect product type from `dealname`
5. Group by YYYY-MM
6. Calculate metrics
7. Generate HTML with stacked bar chart + summary tables
8. Save to `docs/kpi/reports/forecast-YYYY-MM-DD.html`

## Stage Mapping

- **Won:** `closedwon` (Akkoord)
- **Lost:** `closedlost` (Verloren)
- **Pipeline:** all other stages (contractsent, appointmentscheduled, qualifiedtobuy, etc.)

## Product Detection from Deal Name

| Pattern | Product |
|---------|---------|
| `MAGIC` or `Bruiloft` or `HUUR5` or `HEEL` | Magic Mirror XL |
| `PARTY` or `HUUR3` | Party Booth |
| `DIGITAAL` | Party Booth (digital) |
| `DJ` | DJ |
| Fallback | Overig |

## Report Metrics

1. **Monthly revenue bars** — stacked bar chart: Gewonnen + Te Winnen per month
2. **Win rate %** — won / (won + lost), per month and overall
3. **Projected revenue** — pipeline value * overall win rate
4. **Product split** — breakdown by product per month
5. **Average deal value** — per product type
6. **YTD cumulative revenue** — running total of won deals
7. **Month-over-month trend** — growth % between months

## Scope

- Current year only (2026 now, 2027 next year)
- Future months show pipeline only
- Past months show won + remaining pipeline

## Output

- HTML report: `docs/kpi/reports/forecast-YYYY-MM-DD.html`
- Branded PYB styling
- MCP server: `hubspot-crm` (private app token via `.env`)

## Technical Notes

- Paginate HubSpot results if >100 deals
- Use `closedate` for month grouping
- Chart rendered with inline CSS (no external dependencies)
- Date in filename for versioning
