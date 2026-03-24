# Gemini Image Prompt Guide — PicYourBooth

## Photo Reference Library

**Always check `docs/images/photos-source/INDEX.md` before generating images.** The index contains:
- 98 catalogued source photos with quality ratings and descriptions
- **Tier 1 picks** — the 8 best photos to embed as Gemini reference images
- **Tier 2 picks** — 18 secondary references for specific use cases
- Photos organized by product (Magic Mirror, Party Booth, DJ) and USP category

### Top Reference Photos for Gemini Enhance Mode

| Use Case | Reference Photo | Why |
|----------|----------------|-----|
| Magic Mirror DSLR quality | `magic-mirror-usp-geweldig-2.jpg` | #1 overall — fashion-shoot quality portrait |
| Party Booth at event | `party-booth-party-atmosphere-hero.jpg` | Dream venue with bokeh string lights |
| Luxury venue atmosphere | `magic-mirror-vip-venue-wide.png` | Golden chandeliers, wide comp for text |
| Wedding setup | `magic-mirror-photobooth-5.jpg` | Real wedding — cyan LED, balloon column |
| VIP red carpet setup | `magic-mirror-upgrade-vip-14.jpg` | Flower wall + red carpet + stanchions |
| Themed event portraits | `...inlijsten-couple-dayofthedead.png` | Cinematic Day of the Dead costumes |
| Friends at photobooth | `...inlijsten-friends-props-cheers.png` | Clean studio lighting, wedding energy |
| Wedding keychains | `magic-mirror-upgrade-keychain-1.jpg` | Couple holding keychains, pure joy |

## CRITICAL RULE: Always Use Enhance Mode

**ALWAYS use enhance mode with a real source photo.** Never use generate mode for images where our product (Party Booth or Magic Mirror) is visible. Generate mode invents fake hardware that doesn't match our actual products.

- **Enhance mode** = Gemini keeps our real product and transforms the environment. USE THIS.
- **Generate mode** = Gemini invents everything from scratch including fake equipment. AVOID unless the image has zero PYB products in it (e.g. a mood/concept image with no booth visible).

Best source photos for enhance mode per product:
- **Party Booth**: `party-booth-venue-setup-stringlights.png` (PREFERRED — real venue, correct floor-standing scale) or `party-booth-party-atmosphere-hero.jpg` (product in context with bokeh)
- **Magic Mirror**: `magic-mirror-photobooth-5.jpg` (real event, correct scale) or `magic-mirror-vip-venue-wide.png` (wide venue)
- **VIP Setup**: `magic-mirror-upgrade-vip-15.jpg` (red carpet + stanchions, correct scale)

**IMPORTANT: Always use source photos that show the product in a real environment** (not studio/isolated shots). Gemini needs environmental context to maintain correct product scale. Studio shots like `party-booth-product-clean-studio.png` give the right shape but Gemini loses the size — it puts a floor-standing 1.5m booth on a table because there's no room for scale reference.

---

## Brand Style Building Blocks

Every PYB image should combine these elements. Mix and match per product.

### Magic Mirror XL (Premium)
- **Lighting:** Dark cinematic, warm amber/gold (#f59e42), bokeh, chandeliers
- **Venue:** Elegant event halls, dark walls, velvet curtains, candles
- **People:** Semi-formal to formal, confident, glamorous
- **Mood:** VIP, exclusive, magazine-quality, aspirational
- **Props:** Gold stanchions, sequin/shimmer walls, red carpet, flower walls
- **Keywords:** premium, cinematic, warm, elegant, dark, bokeh, intimate

### Party Booth (Accessible)
- **Lighting:** Warm festive, string lights, fairy lights, natural daylight
- **Venue:** Living rooms, backyards, small halls, house parties
- **People:** Casual, friends, family, laughing, real moments
- **Mood:** Fun, relatable, easy, no stress, joyful
- **Props:** Balloons, birthday decorations, snacks, phones
- **Keywords:** casual, fun, cozy, compact, simple, festive, warm

### DJs (Energetic)
- **Lighting:** Purple/violet + amber, lasers, fog, moving heads
- **Venue:** Dark venues, party settings, intimate not festival
- **People:** Dancing crowd silhouettes, DJ focused on equipment
- **Mood:** Energetic, immersive, party vibes
- **DJ Gianni:** Coral accent, Afro Beats/Caribbean, tropical energy
- **DJ Milo:** Mint accent, House/Techno, minimal underground

## Prompt Patterns

### Enhance (real photo + AI styling)
Best for: USP cards, profile photos, product shots with real equipment

```
Keep the [subject] exactly as it appears — authentic.
Transform the BACKGROUND into [target venue].
[Lighting direction]. [Mood direction].
Remove [unwanted elements].
DO NOT add/change [protected elements].
[Format] format. Photorealistic.
```

### Generate (from scratch)
Best for: Upgrade modals, concept images, scenes without real product

```
[Scene description — who, what, where].
[Lighting and atmosphere].
[Mood and energy level].
No text, no logos, no watermarks.
[Format] format. Photorealistic, not illustrated.
```

## Anti-Patterns (learned from experience)

| Problem | Fix |
|---------|-----|
| AI generates duplicate people | Say "DO NOT add any people" or limit to specific count |
| People in suits at house parties | Specify "casual outfit" or "no formal attire" |
| Generic stock photo look | Add specific details: props, decorations, venue features |
| Background clutter remains | Explicitly say "remove commercial signage, brand logos, clutter" |
| Award/prop gets removed when it shouldn't | Say "keep the [item] exactly as it appears" |
| Too much AI glow/fantasy | Add "photorealistic, like a real photo taken at an event" |

## Format Reference

| Usage | Aspect | Size | For |
|-------|--------|------|-----|
| hero | 16:9 landscape | 1920x1080, 1280x720, 768x432 | Page hero backgrounds |
| usp | 1:1 square | 400x400 | USP thumbnail cards |
| card | 3:2 landscape | 600x400 | Service cards |
| modal | 4:3 landscape | 800x600 | Upgrade info modals |
| og | 1.91:1 landscape | 1200x630 | Social share images |

## Post-Processing (Python/Pillow)

### Magic Mirror XL warm shift
```python
r = r.point(lambda x: min(255, int(x * 1.06)))  # boost red
b = b.point(lambda x: int(x * 0.90))             # reduce blue
contrast = 1.12
saturation = 1.10
```

### Party Booth — punchy party mood, vibrant colors
```python
r = r.point(lambda x: min(255, int(x * 1.05)))
b = b.point(lambda x: int(x * 0.92))
contrast = 1.14
saturation = 1.18
brightness = 1.04
```

### Before/After split-screen
- Before side: desaturate (0.7), slight cool, darker (0.95 brightness)
- After side: warm shift, boost contrast (1.15), saturate (1.15)
- Gold divider (#f59e42) with subtle glow
- Labels: "ORIGINEEL" (gray) vs "AI EXPERIENCE" (gold)
