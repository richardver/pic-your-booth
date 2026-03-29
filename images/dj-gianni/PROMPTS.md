# DJ Gianni - Gegenereerde Assets & Prompts

Alle AI-gegenereerde en verwerkte afbeeldingen voor DJ Gianni. Elke asset is gemaakt met Gemini AI of Playwright export.

---

## Mixtape Covers

Gegenereerd met `gemini-2.5-flash-image` model. Genre-specifieke accent kleuren uit DJ Gianni's warm palette.

### Caribbean Vibes Vol. 1 (`mixtape/caribbean-mixtape-cover.png`)

**Model:** gemini-2.5-flash-image
**Accent:** Golden Amber #f5b731
**Abstract achtergrond:** Flowing ocean wave vormen, palm frond silhouetten, gouden particle scatter

```
Design a stunning, premium DJ mixtape cover art for "DJ GIANNI - CARIBBEAN VIBES VOL. 1".

Square 1:1 format, high resolution.

TYPOGRAPHY:
- "DJ GIANNI" massive dominant title, heavy condensed uppercase (Bebas Neue style)
- "CARIBBEAN VIBES VOL. 1" subtitle
- Genre tags: DANCEHALL | SOCA | REGGAETON as pill-shaped labels
- "Pure Vibes" in italic sans-serif

ABSTRACT BACKGROUND:
- Dark base (#050508)
- Flowing organic wave forms in golden amber (#f5b731) at 20-30% opacity
- Layered translucent shapes suggesting palm fronds or island horizons
- Subtle golden amber particle scatter
- Warm gradient glow from bottom-center

BRAND ELEMENTS:
- 5 thin vertical EQ-bar lines in golden amber, varying heights
- Hexagonal badge with letter "G" in golden amber, top-right

COLORS:
- Background: #050508, Accent: #f5b731, Text: #ededf0

MOOD: Tropical luxury. Warm night air. Golden sunset over dark ocean.

DO NOT: realistic faces, photographs, watermarks, musical notes, cool blue/cyan tones.
```

### NL Urban Vol. 1 (`mixtape/nl-urban-mixtape-cover.png`)

**Model:** gemini-2.5-flash-image
**Accent:** Warm Purple #c084fc
**Abstract achtergrond:** Sharp angular geometry, purple smoke/mist, grid-like city patterns

```
Design a stunning, premium DJ mixtape cover art for "DJ GIANNI - NL URBAN VOL. 1".

Square 1:1 format, high resolution.

TYPOGRAPHY:
- "DJ GIANNI" massive dominant title, heavy condensed uppercase (Bebas Neue style)
- "NL URBAN VOL. 1" subtitle
- Genre tags: HIP-HOP | R&B NL | URBAN as pill-shaped labels
- "Pure Vibes" in italic sans-serif

ABSTRACT BACKGROUND:
- Dark base (#050508)
- Sharp angular geometric shapes in warm purple (#c084fc) at 15-25% opacity
- Diagonal slashes and trapezoids overlapping, creating depth
- Subtle warm purple smoke rising from bottom
- Grid-like patterns suggesting city blocks

BRAND ELEMENTS:
- 5 thin vertical EQ-bar lines in warm purple, varying heights
- Hexagonal badge with letter "G" in warm purple, top-right

COLORS:
- Background: #050508, Accent: #c084fc, Text: #ededf0

MOOD: Amsterdam at 2AM. Urban confidence. Street meets luxury.

DO NOT: realistic faces, photographs, watermarks, cool blue/cyan tones.
```

### Afro Beats Vol. 2 (`mixtape/afro-mixtape-cover.png`)

**Model:** gemini-2.5-flash-image
**Accent:** Coral #f0654a
**Abstract achtergrond:** Concentric circular rings, tribal-inspired modern geometry, ember particles

```
Design a stunning, premium DJ mixtape cover art for "DJ GIANNI - AFRO BEATS VOL. 2".

Square 1:1 format, high resolution.

TYPOGRAPHY:
- "DJ GIANNI" massive dominant title, heavy condensed uppercase (Bebas Neue style)
- "AFRO BEATS VOL. 2" subtitle
- Genre tags: AFRO BEATS | AMAPIANO | AFRO HOUSE as pill-shaped labels
- "Pure Vibes" in italic sans-serif

ABSTRACT BACKGROUND:
- Dark base (#050508)
- Concentric circular rings in coral (#f0654a) at 15-25% opacity
- Organic tribal-inspired geometric patterns abstracted into hexagons, circles, dotted arcs
- Warm coral ember particles floating upward
- Radial gradient glow from center

BRAND ELEMENTS:
- 5 thin vertical EQ-bar lines in coral, varying heights
- Hexagonal badge with letter "G" in coral, top-right

COLORS:
- Background: #050508, Accent: #f0654a, Text: #ededf0

MOOD: African sunset energy. Primal rhythm meets premium modern design.

DO NOT: realistic faces, photographs, watermarks, cool blue/cyan tones.
```

---

## SoundCloud Profiel Banner (`soundcloud/banner-2480x520.png`)

**Methode:** Gemini AI achtergrond + Playwright typography overlay
**Afmetingen:** 2480x520px
**Bron HTML:** `/tmp/dj-gianni-soundcloud-banner.html` (niet gecommit)
**Achtergrond:** `/tmp/banner-bg-gemini.png` (Gemini 2.5 Flash Image)

### Design: Tri-Genre Gradient Flow

Gemini-gegenereerde abstracte achtergrond met drie genre-kleuren die van links naar rechts vloeien:
- Links (0-700px): Coral (#f0654a) — concentric rings, hexagons (Afro Beats motief)
- Midden (~1240px): Golden Amber (#f5b731) — golvende lijnen, palmblad silhouetten (Caribbean motief)
- Rechts (1780-2480px): Warm Purple (#c084fc) — diagonale lijnen, trapezoid geometry (NL Urban motief)

Typography overlay via HTML/Playwright voor pixel-perfect tekst en safe zones.

### Mobile Safe Zone

Alleen het midden ~1400px is zichtbaar op mobiel. Alle tekst en branding zit in deze zone:
- "DJ GIANNI" — Bebas Neue, 130px, centered, met subtiele text-shadow
- "Pure Vibes" — Space Grotesk italic, 26px, 45% opacity
- Genre pills: AFRO BEATS (coral), CARIBBEAN (amber), NL URBAN (purple) met backdrop-filter blur
- EQ bars (12 stuks, tri-color, 30% opacity) en hexagon G logo
- Center-darken gradient zorgt voor tekstleesbaarheid over de achtergrond

### Avatar Dead Zone

SoundCloud plaatst het ronde profielfoto links-onder (~280px). Geen content in dat gebied.

### Gemini Achtergrond Prompt

Model: `gemini-2.5-flash-image` via `generate_content` met `response_modalities=['IMAGE']`
Output: 1024x1024 → resize naar 2480px breed → center-crop naar 520px hoog

```
Generate an image: A stunning ultra-wide abstract background for a premium DJ profile banner.

DIMENSIONS: Ultra-wide landscape format, approximately 4.8:1 ratio (very wide, very short — like a panoramic strip).

TRI-COLOR GRADIENT FLOW (left to right across the width):
- LEFT ZONE: Deep coral/warm orange (#f0654a) glow with concentric circular ring patterns, tribal-inspired hexagonal geometry, rising ember-like particles. African sunset energy.
- CENTER ZONE: Golden amber (#f5b731) glow with flowing organic wave forms, subtle palm frond silhouettes, tropical warmth. Caribbean golden hour.
- RIGHT ZONE: Warm purple (#c084fc) glow with sharp diagonal slash lines, angular trapezoid geometry, rising purple smoke/mist. Amsterdam 2AM urban nightlife.

The three color zones should BLEND smoothly into each other — no hard edges. The transition should feel like a panoramic nightclub lighting sweep.

BACKGROUND: Very dark, near-black (#050508). The colored glows emerge from the darkness like concert lighting.

STYLE:
- Abstract, geometric, atmospheric — NO text, NO faces, NO musical instruments, NO DJ equipment
- Premium, cinematic, minimal — like a high-end event production visual
- Motifs and patterns at 15-30% opacity — texture and depth, not competing for attention
- Subtle film grain aesthetic
- The center area should be slightly darker/cleaner (text will be overlaid there later)

MOOD: Dark nightclub panorama. Three genre identities flowing into one cinematic sweep. Premium, confident, warm.

DO NOT INCLUDE: Any text, letters, words, numbers, logos, realistic faces, photographs, musical notes, cool blue/cyan tones, bright neon, busy textures, or cluttered elements. ONLY abstract geometric patterns and atmospheric light on a near-black background.
```

### Python Script

Generatie script: `/tmp/generate-banner-bg.py`
- Laadt API key uit `.env` (`GOOGLE_AI_API_KEY`)
- Genereert met `gemini-2.5-flash-image` model
- Resize naar 2480px breed, center-crop naar 520px hoog
- Output: `/tmp/banner-bg-gemini.png`

---

## Profiel Foto's (`profile/`)

| Bestand | Bron | Methode |
|---------|------|---------|
| `profiel.jpeg` | Originele foto Luca | Geen AI - origineel |
| `preview.jpg` | Cropped versie profiel | Geen AI - resize |
| `luca-portrait.jpg` | Portret foto | Geen AI - origineel |

---

## Genre Accent Kleuren

| Genre | Kleur | Hex | Gebruik |
|-------|-------|-----|---------|
| Afro Beats | Coral | `#f0654a` | Primary, default |
| Caribbean | Golden Amber | `#f5b731` | Caribbean serie |
| Nederlands Urban | Warm Purple | `#c084fc` | NL Urban serie |
