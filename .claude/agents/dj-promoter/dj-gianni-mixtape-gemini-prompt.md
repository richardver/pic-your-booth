# DJ Gianni - Mixtape Cover Gemini Prompt

Prompt template for generating mixtape and SoundCloud cover art via Gemini. Swap the **highlighted** parts for each variation.

---

## Prompt

```
Design a minimal, premium DJ social media graphic for "DJ GIANNI" - [EVENT/SET NAME e.g. Afro Beats Set at Festival Haarlem].

Layout:
- Square format (1:1), 3000x3000px
- "DJ GIANNI" as dominant title in Bebas Neue style (heavy, condensed, uppercase, letter-spacing 0.04em)
- "AFRO BEATS" / "CARIBBEAN" / "NEDERLANDS" / "HITS" as genre tags - small, pill-shaped, uppercase, Space Grotesk Bold
- "Pure Vibes" in italic Space Grotesk below the name
- Clean, structured typography hierarchy - no clutter

Visual style:
- Very dark background (#050508) with subtle coral (#f0654a) gradient glow at bottom or side
- MINIMAL design: no patterns, no textures, no noise - pure typography and whitespace
- If photo included: B&W studio portrait, 200x200px area, rounded corners (24px radius)
- EQ-bar motif: 5 thin vertical bars in coral, varying heights, as a subtle decorative element
- Gold/coral hexagon with letter "G" as the DJ brand logo mark - top-left or bottom-right corner

Color palette:
- Background: #050508 (void)
- Primary accent: #f0654a (coral) - for name, EQ bars, tags
- Text: #ededf0 (white) for headings, rgba(237,237,240,0.40) for secondary text
- Subtle: rgba(240,101,74,0.10) for tag backgrounds

Typography:
- Display: Bebas Neue (or similar heavy condensed sans-serif)
- Body: Space Grotesk (or similar geometric sans-serif)
- NO Oswald, NO Montserrat, NO serif fonts

Mood: Dark, minimal, premium, confident - "less is more" nightlife aesthetic
Brand reference: PicYourBooth DJ page design system

Do NOT include: realistic human faces, watermarks, busy backgrounds, neon glows, or old gold (#FFD700) accents
```

## Genre Accent Colors

Each mixtape series uses a different accent color from DJ Gianni's warm palette. Swap the accent color in the prompt accordingly.

| Genre | Accent | Hex | Gradient Glow | Mood |
|-------|--------|-----|---------------|------|
| **Afro Beats** | Coral | `#f0654a` | `rgba(240,101,74,0.12)` | Warm, sun-drenched, African energy |
| **Caribbean** | Golden Amber | `#f5b731` | `rgba(245,183,49,0.12)` | Tropical sunset, island gold, carnival warmth |
| **Nederlands Urban** | Warm Purple | `#c084fc` | `rgba(192,132,252,0.12)` | Street nightlife, Dutch urban, warm glow |

**Never use:** `#34d399` (Milo's cyan), `#00b4d8`, or any cool blue/green tones.

## Variables to Swap

| Variable | Example |
|----------|---------|
| Event/set name | "Afro Beats Set at Festival Haarlem" |
| Genre tags | Pick from: Afro Beats, Caribbean, Nederlands, Hits |
| Accent color | Pick from: `#f0654a` (Afro), `#f5b731` (Caribbean), `#c084fc` (Urban NL) |
| Format | 1:1 for covers, 2480x520 for SoundCloud banner |

## Exported Covers

- SoundCloud banner: `docs/images/dj-gianni/social/soundcloud-banner.png` (2480x520)
- Afro mixtape cover: `docs/images/dj-gianni/mixtape/afro-mixtape-cover-v2.png` (1400x1400)
- Caribbean mixtape cover: `docs/images/dj-gianni/mixtape/caribbean-mixtape-cover.png` (1400x1400)
- NL Urban mixtape cover: `docs/images/dj-gianni/mixtape/nl-urban-mixtape-cover.png` (1400x1400)
