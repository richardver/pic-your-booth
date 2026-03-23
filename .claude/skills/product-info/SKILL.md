---
name: product-info
description: "Get accurate product specs, packages, upgrades, and pricing for any PYB service. Use /product-info to look up Party Booth, Magic Mirror XL, DJ services, or pricing details."
user-invocable: true
context: fork
agent: product-specialist
---

# Product Info Lookup

Get accurate, up-to-date product information for any PYB service.

## Process

1. Read the product-specialist agent's knowledge files for the requested product
2. If a specific product is asked: load that product's knowledge file
3. If pricing is asked: load `knowledge-pricing.md`
4. If comparison is asked: load both products and compare
5. Present the information clearly with pricing and specs

## Input

The user will ask about:
- A specific product (Party Booth, Magic Mirror XL, DJs)
- Pricing for a product or combination
- What's included in a package
- Upgrade options
- Equipment specs
- Setup requirements
- Product comparisons or recommendations by event type

## Output

1. **Product name and tagline**
2. **What's included** (base package)
3. **Pricing** (base + upgrades with totals)
4. **Key specs** (equipment, setup, requirements)
5. **Best for** (target segment / event types)
