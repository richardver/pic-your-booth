---
name: hubspot-deal
description: "Parse text and create a contact + deal in HubSpot. Use /hubspot-deal to paste any unstructured text (email, WhatsApp, form, notes) and automatically create a linked contact and deal in the CRM."
user-invocable: true
context: fork
---

# HubSpot Deal Creator

You MUST follow these steps exactly. Do NOT ask what the user wants to do. Do NOT analyze the source of the text. Do NOT comment on whether this is from another system, pipeline, or account.

The user's input (after `/hubspot-deal`) is ALWAYS unstructured text to parse. It can be any format: email, WhatsApp, HubSpot screenshot text, form submission, notes, copy-pasted from anywhere.

**Your ONLY job:** extract contact + deal fields from the text → show confirmation → create in HubSpot.

**Rules:**
- NEVER ask "what would you like me to do?" — just parse it
- NEVER comment on where the text came from (ViziBooth, other CRM, etc.)
- Ignore any pipeline/stage/prefix info from the source text — always use PYB defaults
- The ONLY question you may ask is "Magic Mirror XL or Party Booth?" if the product is unclear
- Start Step 1 immediately

## HubSpot Configuration

- **MCP Server:** `hubspot-crm` (private app token via `.env`)
- **Pipeline:** `default` (Deals pipeline)
- **Stage:** `closedwon` (Akkoord)
- **Deal type:** `newbusiness` (Nieuw bedrijf)
- **Owner ID:** `90114999` (PicYourBooth NL)
- **Association type:** Contact → Deal = `4` (HUBSPOT_DEFINED)

## Process

### Step 1: Parse the text

Extract all available fields from the user's pasted text. Use Claude's NLP — the text can be any format (email, WhatsApp, form submission, notes, screenshot text).

**Contact fields to extract:**
- `firstname` — First name
- `lastname` — Last name
- `email` — Email address
- `phone` — Phone number (Dutch format, keep as-is)
- `city` — City/location if mentioned
- `company` — Company name if mentioned
- `service` — Product type: `magic-mirror`, `party-booth`, or `dj`
- `evenement_date` — Event date (YYYY-MM-DD)
- `evenement_type` — Event type if detectable: `wedding`, `corporate_event`, `birthday`, `other` (festival/club), or `anders`
- `evenement_upgrades` — Semicolon-separated upgrades if mentioned: `vip`, `keychain`, `host`, `ai_photobooth`, `live_dj`, `premium_design`, `levering`, `ai_background+filters`, `dj_extra_uur_1`, `dj_extra_uur_2`, `dj_extra_uur_3`

**Deal fields to extract:**
- `product` — Magic Mirror XL or Party Booth (ask user if unclear)
- `amount` — Price in euros (number only, no currency symbol)
- `event_date` — Event date (for close date, format: YYYY-MM-DD)
- `event_description` — Short event description (e.g. "bruiloft", "bedrijfsfeest")
- `location` — Event location/city

### Step 2: Determine deal name prefix

Based on the product:
- Magic Mirror XL → prefix `MAGIC`
- Party Booth → prefix `PARTY`

No number after the prefix. Just `MAGIC` or `PARTY`.

If the product is not clear from the text, ask the user: "Magic Mirror XL or Party Booth?"

### Step 3: Show confirmation

Present the parsed data to the user in a clear table:

```
CONTACT:
  Name:      {firstname} {lastname}
  Email:     {email}
  Phone:     {phone}
  City:      {city}
  Service:   {service}
  Event:     {evenement_date} ({evenement_type})
  Upgrades:  {evenement_upgrades} (if any)

DEAL:
  Name:      {PREFIX}/{firstname} - {city} - {phone}
  Amount:    EUR {amount}
  Close:     {event_date}
  Product:   {product}
  Stage:     Akkoord
  Owner:     PicYourBooth NL
```

Ask: "Klopt dit? Zal ik aanmaken?" (Does this look right? Shall I create it?)

Wait for user confirmation before proceeding. If the user corrects any field, update and re-confirm.

### Step 4: Create contact

Use tool: `mcp__hubspot-crm__hubspot-batch-create-objects`
- objectType: "contacts"
- inputs: one object with properties:
  - `firstname`
  - `lastname`
  - `email`
  - `phone`
  - `city` (if available)
  - `company` (if available)
  - `service` — based on product: `magic-mirror`, `party-booth`, or `dj`
  - `evenement_date` — event date in YYYY-MM-DD format
  - `evenement_type` — if detectable: `wedding`, `corporate_event`, `birthday`, `other` (festival/club), or `anders`

Save the returned contact ID.

### Step 5: Create deal

Use tool: `mcp__hubspot-crm__hubspot-batch-create-objects`
- objectType: "deals"
- inputs: one object with properties:
  - `dealname` — Generated name: `{PREFIX}/{Name} - {City} - {Phone}`
  - `pipeline` — `default`
  - `dealstage` — `closedwon`
  - `amount` — Extracted amount as string
  - `closedate` — Event date in ISO format (YYYY-MM-DD)
  - `dealtype` — `newbusiness`
  - `hubspot_owner_id` — `90114999`

Save the returned deal ID.

### Step 6: Associate contact to deal

Use tool: `mcp__hubspot-crm__hubspot-batch-create-associations`
- fromObjectType: "contacts"
- toObjectType: "deals"
- types: [{"associationCategory": "HUBSPOT_DEFINED", "associationTypeId": 4}]
- inputs: [{"from": {"id": "{contact_id}"}, "to": {"id": "{deal_id}"}}]

### Step 7: Report result

Show the user:
- Contact created: {name} (link: `https://app-eu1.hubspot.com/contacts/148115666/record/0-1/{contact_id}`)
- Deal created: {dealname} (link: `https://app-eu1.hubspot.com/contacts/148115666/record/0-3/{deal_id}`)
- Contact linked to deal

## Error Handling

- If contact creation fails: show error, do not proceed to deal creation
- If deal creation fails: show error, note that contact was already created
- If association fails: show error, provide manual link instructions

## Example

Input text:
```
Nivin Elgammal
nivinelgammal@gmail.com
0622062049
Magic Mirror XL
Rijswijk, mistura movement
4 april 2026
EUR 299
```

Output deal name: `MAGIC/Nivin - Rijswijk - 0622062049`
