---
name: seo-audit
description: "Audit a page for SEO and LLM optimization. Checks keywords, meta tags, headings, structured data, content structure, and AI discoverability. Use /seo-audit with a page name or URL."
user-invocable: true
context: fork
agent: seo
---

# SEO & LLM Audit

Audit a page for search engine and AI answer optimization.

## Input

The user provides a page to audit (file path, URL, or page name like "homepage" or "magic-mirror").

## Steps

### Phase 1: Load Context

1. Read `.claude/agents/seo/_index.md` for audit rules
2. Read `.claude/agents/seo/knowledge-keywords.md` for the focus keyword of this page
3. Read `.claude/agents/seo/knowledge-technical-seo.md` for meta tag specs and schema requirements
4. Read `.claude/agents/seo/knowledge-on-page.md` for heading and content rules
5. Read `.claude/agents/seo/knowledge-llm-optimization.md` for LLM checklist
6. Read the actual page file

### Phase 2: Keyword Audit

7. Identify the focus keyword for this page from the keyword map
8. Check H1 contains focus keyword
9. Check meta title starts with focus keyword (max 60 chars)
10. Check meta description contains keyword + CTA (max 155 chars)
11. Check URL slug matches keyword
12. Check keyword appears in first 100 words
13. Check keyword density (target 1-2%, flag if over 3%)
14. Check long-tail keywords in H2/H3 headings

### Phase 3: Technical SEO Audit

15. Verify `<html lang="nl">`
16. Verify `<link rel="canonical">`
17. Verify Open Graph tags (og:title, og:description, og:image)
18. Check heading hierarchy (one H1, logical H2/H3 nesting)
19. Check image alt text (descriptive, keyword where relevant)
20. Check internal links (anchor text descriptive, links to offerte)
21. Check mobile meta viewport tag

### Phase 4: Structured Data Audit

22. Check for LocalBusiness schema
23. Check for Product schema (on product pages)
24. Check for FAQPage schema
25. Check for AggregateRating schema
26. Validate schema structure (correct @type, required fields)

### Phase 5: LLM Discoverability Audit

27. Check FAQ section present with clear Q&A format
28. Check entity clarity (name, type, location, products in first paragraph)
29. Check "citeerbaar samenvattingsblok" (price, includes, unique, region)
30. Check comparison content available
31. Check direct answer format (specific, with prices, not vague)

### Phase 6: Score & Report

32. Score each category (0-10):
    - Keyword targeting (10 points)
    - Technical SEO (10 points)
    - On-page content (10 points)
    - Structured data (10 points)
    - LLM discoverability (10 points)
33. Calculate total SEO Score (0-50)
34. List issues by priority (CRITICAL / IMPORTANT / NICE-TO-HAVE)
35. Provide specific fix recommendations

## Output

1. **SEO Score**: X/50 with category breakdown
2. **Focus keyword**: confirmed or missing
3. **Critical issues**: must fix before launch
4. **Important issues**: fix within first week
5. **Nice-to-have**: future improvements
6. **LLM readiness**: ready / needs work / not ready

## Target Scores

- 40-50: Launch ready
- 30-39: Needs work on key areas
- 20-29: Significant gaps
- Below 20: Not ready for search
