# DJ Milo - Mixtape Cover Gemini Prompt

Prompt template for generating mixtape and SoundCloud cover art via Gemini. Swap the **highlighted** parts for each variation.

---

## Prompt

```
Design a minimal, premium DJ social media graphic for "MILO" - [EVENT/SET NAME e.g. Tech House Set at Club Rotterdam].

Layout:
- Square format (1:1), 3000x3000px
- "MILO" as dominant title in Bebas Neue style (heavy, condensed, uppercase, letter-spacing 0.04em)
- "TECH HOUSE" / "HOUSE" / "DEEP" as genre tags - small, pill-shaped, uppercase, Space Grotesk Bold
- "Deep in the groove" in italic Space Grotesk below the name
- Clean, structured typography hierarchy - no clutter

Visual style:
- Very dark background (#050508) with subtle cyan (#34d399) gradient glow at bottom or side
- MINIMAL design: no patterns, no textures, no noise - pure typography and whitespace
- If photo included: B&W studio portrait, 200x200px area, rounded corners (24px radius)
- Sine wave motif: 3-4 thin horizontal wave lines in accent color, as a subtle decorative element
- Cyan diamond with letter "M" as the DJ brand logo mark (clip-path: polygon(50% 0%, 100% 50%, 50% 100%, 0% 50%)) - top-left or bottom-right corner

Color palette:
- Background: #050508 (void)
- Primary accent: #34d399 (cyan) - for name, sine waves, tags
- Text: #ededf0 (white) for headings, rgba(237,237,240,0.40) for secondary text
- Subtle: rgba(52,211,153,0.10) for tag backgrounds

Typography:
- Display: Bebas Neue (or similar heavy condensed sans-serif)
- Body: Space Grotesk (or similar geometric sans-serif)
- NO Oswald, NO Montserrat, NO serif fonts

Mood: Deep, immersive, groove-driven - dark club aesthetic
Brand reference: PicYourBooth DJ page design system

Do NOT include: warm tones, coral, golden amber, realistic human faces, watermarks, busy backgrounds
```

## Genre Accent Colors

Each mixtape series uses a different accent color from DJ Milo's cool palette. Swap the accent color in the prompt accordingly.

| Genre | Accent | Hex | Gradient Glow | Mood |
|-------|--------|-----|---------------|------|
| **Tech House** | Cyan | `#34d399` | `rgba(52,211,153,0.12)` | Groovy, rhythmic, infectious energy |
| **House** | Electric Blue | `#38bdf8` | `rgba(56,189,248,0.12)` | Uplifting, warm house, rolling basslines |
| **Deep** | Violet | `#8b5cf6` | `rgba(139,92,246,0.12)` | Atmospheric, hypnotic, late-night immersion |

**Never use:** `#f0654a` (Gianni's coral), `#f5b731`, or any warm orange/amber/red tones.

## Variables to Swap

| Variable | Example |
|----------|---------|
| Event/set name | "Tech House Set at Club Rotterdam" |
| Genre tags | Pick from: Tech House, House, Deep |
| Accent color | Pick from: `#34d399` (Tech House), `#38bdf8` (House), `#8b5cf6` (Deep) |

## Exported Covers

- Tech House mixtape cover: `docs/images/dj-milo/mixtape/tech-house-mixtape-cover.png` (1400x1400)
- House mixtape cover: `docs/images/dj-milo/mixtape/house-mixtape-cover.png` (1400x1400)
- Deep mixtape cover: `docs/images/dj-milo/mixtape/deep-mixtape-cover.png` (1400x1400)
