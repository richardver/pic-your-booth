# SEO & LLM Optimization Agent — Design Document

**Date:** 2026-03-23
**Status:** Approved
**Author:** Richard + Claude

---

## Overview

New standalone SEO agent that owns keyword strategy, technical SEO, structured data, LLM discoverability, and page-level optimization audits. Works alongside designer (builds pages), ad-specialist (keyword alignment), and strategist (content framing).

## Knowledge Files (6)

| # | File | Content |
|---|---|---|
| 1 | `knowledge-keywords.md` | Focus keyword map per page, long-tail clusters, keyword intent, seasonal trends |
| 2 | `knowledge-technical-seo.md` | Meta tags, canonical URLs, sitemap, robots.txt, Core Web Vitals, structured data schemas |
| 3 | `knowledge-on-page.md` | Heading hierarchy, keyword placement, internal linking, image alt text, Dutch content rules |
| 4 | `knowledge-llm-optimization.md` | AI answer optimization: FAQ schema, entity markup, citation-worthy content, comparison positioning |
| 5 | `knowledge-competition-seo.md` | Competitor keyword analysis, domain authority gaps, content gaps, backlink opportunities |
| 6 | `knowledge-local-seo.md` | Google Business Profile, local pack, city landing pages, NAP consistency, review strategy |

## Focus Keyword Map

| Page | Primary | Long-tail |
|---|---|---|
| Homepage | photobooth huren | fotobooth huren, photobooth verhuur, photobooth huren nederland, entertainment bruiloft, photobooth en dj huren |
| Magic Mirror | fotospiegel huren | ai photobooth, ai photobooth huren, spiegel photobooth huren, premium photobooth, photobooth bruiloft, photobooth bedrijfsfeest, photobooth huren randstad |
| Party Booth | photobooth huren goedkoop | fotobox huren, goedkope photobooth, photobooth verjaardag, digitale photobooth huren, photobooth huren rotterdam |
| DJs | dj huren | dj boeken, dj huren bruiloft, dj huren feest, dj inhuren randstad, dj huren amsterdam, dj huren rotterdam |
| Offerte | photobooth offerte aanvragen | photobooth huren prijs, photobooth kosten, dj huren prijs, wat kost een photobooth, photobooth huren offerte |

## Skills

### New: `/seo-audit`
Standalone page SEO + LLM audit with scoring.

### Updated: `/design-page` and `/design-landingpage`
Add SEO validation phase after build:
- H1 matches focus keyword
- Meta title max 60 chars, keyword front-loaded
- Meta description max 155 chars with CTA
- Structured data present
- Heading hierarchy correct
- LLM discoverability check

## What Changes
- New: `.claude/agents/seo.md` + `seo/` directory (6 knowledge files)
- New: `.claude/skills/seo-audit/SKILL.md`
- Update: `/design-page` and `/design-landingpage` get SEO phase
- Update: `_registry.md`, `CLAUDE.md`, `README.md`
