---
name: forecast
description: "Pull deals from HubSpot and generate a branded HTML revenue forecast report. Use /forecast to create a current-year deals & revenue overview with win rate, projections, and product breakdown."
user-invocable: true
context: fork
---

# Revenue Forecast Report

Generate a branded HTML revenue forecast report from live HubSpot deal data.

**Output:** `docs/kpi/reports/forecast-YYYY-MM-DD.html` (today's date)

## Process

### Step 1: Pull all deals from HubSpot

Use `mcp__hubspot-crm__hubspot-search-objects` to pull all deals for the **current year**.

```
objectType: "deals"
properties: ["dealname", "dealstage", "amount", "closedate", "pipeline", "createdate"]
filterGroups:
  - filters:
    - propertyName: "closedate"
      operator: "GTE"
      value: "{CURRENT_YEAR}-01-01T00:00:00Z"
    - propertyName: "closedate"
      operator: "LTE"
      value: "{CURRENT_YEAR}-12-31T23:59:59Z"
sorts:
  - propertyName: "closedate"
    direction: "ASCENDING"
limit: 100
```

If results have paging cursor, paginate until all deals are retrieved.

### Step 2: Classify deals

For each deal, determine:

**Status** based on `dealstage`:
- `closedwon` → **Won** (Gewonnen)
- `closedlost` → **Lost** (Verloren)
- Everything else → **Pipeline** (Te Winnen)

**Product** based on `dealname` (case-insensitive):
- Contains `MAGIC` or `Bruiloft` or `HUUR5` or `HEEL` → **Magic Mirror XL**
- Contains `PARTY` or `HUUR3` → **Party Booth**
- Contains `DIGITAAL` → **Party Booth (Digitaal)**
- Contains `DJ` → **DJ**
- Fallback → **Overig**

**Month** from `closedate` → extract YYYY-MM.

### Step 3: Calculate metrics

For each month (Jan–Dec of current year):

| Metric | Formula |
|--------|---------|
| Gewonnen | Sum of `amount` where status = Won |
| Te Winnen | Sum of `amount` where status = Pipeline |
| Verloren | Sum of `amount` where status = Lost |
| Win Rate % | Won deals count / (Won + Lost deals count) * 100 |

**Overall metrics:**
- **Total Gewonnen YTD** — sum of all won deals
- **Total Pipeline** — sum of all pipeline deals
- **Overall Win Rate** — total won count / (won + lost count)
- **Projected Revenue** — Total Gewonnen + (Total Pipeline * Overall Win Rate)
- **Average Deal Value** — per product type (won deals only)
- **MoM Trend** — % change in won revenue vs previous month

### Step 4: Generate HTML report

Create the HTML report with these sections:

#### Header
- PYB logo (use data URI or text fallback)
- Title: "PicYourBooth Omzet Prognose {YEAR}"
- Generated date
- Report period: "Januari – December {YEAR}"

#### Summary Cards (top row)
4 cards in a row:
1. **Totale Omzet** — won revenue YTD (large number, gold)
2. **Pipeline** — total pipeline value
3. **Prognose** — projected revenue (won + pipeline * win rate)
4. **Win Rate** — overall % with visual indicator

#### Monthly Revenue Chart
Stacked bar chart (pure CSS/HTML, no JS libraries):
- X-axis: months Jan–Dec (show Dutch abbreviations: Jan, Feb, Mrt, Apr, Mei, Jun, Jul, Aug, Sep, Okt, Nov, Dec)
- Bars: Gewonnen (gold `#d4882e`) stacked with Te Winnen (light grey `#e0e0e0`)
- Values displayed on/above bars
- Scale relative to max monthly total
- Current month highlighted with subtle border

#### Product Breakdown Table
Table with columns: Product | Deals Won | Won Revenue | Pipeline | Avg Deal Value

#### Monthly Detail Table
Table with columns: Maand | Gewonnen | Te Winnen | Verloren | Win Rate % | Cumulatief

#### Deal List
Collapsible/scrollable list of all deals grouped by month:
- Deal name | Amount | Status (color-coded badge)

### Step 5: Styling

Use PYB brand styling consistent with factuur/offerte templates:

```css
:root {
  --bg: #ffffff;
  --surface: #f5f5f5;
  --surface-up: #ebebeb;
  --text: #1a1a1a;
  --text-muted: #6b6b6b;
  --gold: #d4882e;
  --gold-light: #f59e42;
  --border: #e0e0e0;
  --won: #d4882e;
  --pipeline: #c8c8c8;
  --lost: #e0e0e0;
  --font-display: 'Bebas Neue', sans-serif;
  --font-body: 'Space Grotesk', sans-serif;
}
```

**Typography:**
- Google Fonts: Bebas Neue + Space Grotesk
- Title: Bebas Neue, 48px, gold
- Section headers: Bebas Neue, 28px
- Body: Space Grotesk, 14px
- Numbers/amounts: Space Grotesk 600 weight

**Layout:**
- Max-width: 1100px, centered
- Not A4 constrained (this is a dashboard, not a printable document)
- Responsive padding
- Cards use subtle shadows and rounded corners

### Step 6: Save report

1. Ensure `docs/kpi/reports/` directory exists
2. Save HTML to `docs/kpi/reports/forecast-{YYYY-MM-DD}.html` using today's date
3. Tell the user the file path and key highlights:
   - Total won revenue
   - Pipeline value
   - Projected revenue
   - Win rate
   - Number of deals

## Important Rules

- **MCP server:** Always use `mcp__hubspot-crm__` (NOT `mcp__hubspot__`)
- **Current year only:** Filter by closedate within Jan 1 – Dec 31 of current year
- **No external JS:** Chart must be pure CSS/HTML (inline styles, no Chart.js or similar)
- **Dutch labels:** All labels in Dutch (Gewonnen, Te Winnen, Verloren, Omzet, Prognose, Maand)
- **Currency format:** Always `€ {amount}` with space, no decimals for round numbers
- **Empty months:** Show all 12 months even if no deals (zero bars)
- **Zero division:** Handle months with no won+lost deals (win rate = "–")
