"""
Prompt templates for Gemini image generation.
Product-specific visual identities driven by real photography characteristics.

CRITICAL RULE: ALWAYS use enhance mode with a real source photo when our product
(Party Booth or Magic Mirror) should be visible. Generate mode invents fake hardware.
Only use generate mode for concept images with NO PYB products in frame.

Photo reference library: docs/images/photos-source/INDEX.md
- 98 source photos catalogued with quality ratings
- Tier 1 picks: 8 best photos for Gemini reference input

Best source photos per product (ALWAYS use venue shots, not studio — Gemini needs room context for correct scale):
- Party Booth: partybooth/product/party-booth-venue-setup-stringlights.png (PREFERRED) or party-booth-party-atmosphere-hero.jpg
- Magic Mirror: magicmirror/photobooth/magic-mirror-photobooth-5.jpg (PREFERRED) or magic-mirror-vip-venue-wide.png
- VIP Setup: magicmirror/upgrade - vip/magic-mirror-upgrade-vip-15.jpg
- AVOID studio/isolated shots (e.g. party-booth-product-clean-studio.png) — correct shape but Gemini loses scale

Visual identity system:
- Magic Mirror XL → Black & Gold Editorial / luxury portrait (Canon R5 + 85mm f/1.2)
- Party Booth → Neon Modern Party / Fujifilm Instax (Fujifilm X-T5 + 23mm f/2)
- DJs → Concert photography / moody stage lighting (Sony A7S III + 35mm f/1.4)
"""

# =============================================================================
# PHOTOGRAPHY REALISM LAYER — appended to ALL prompts
# This is the secret sauce for realistic people/faces
# =============================================================================

REALISM_DIRECTIVES = """
Photography realism requirements:
- Shot on a real camera by a professional event photographer
- Natural skin texture with pores, subtle imperfections, and real skin tones
- Authentic facial expressions — mid-laugh, mid-conversation, candid moments, NOT posed stock-photo smiles
- Natural motion blur on moving hands/hair — people are alive, not frozen
- Real clothing with wrinkles, folds, and fabric texture — not smooth CG clothing
- Visible depth of field — subject sharp, background has natural bokeh
- No symmetrical faces, no uncanny smoothness, no plastic skin
- Slight lens imperfections are OK: minor chromatic aberration, natural vignette, subtle lens flare from light sources
- Each person should look like a DIFFERENT individual — varied ages, body types, ethnicities, heights
- NO text, logos, watermarks, or readable signage in the image
"""

# =============================================================================
# PRODUCT-SPECIFIC BRAND CONTEXTS
# Each product gets its own visual DNA based on photography style
# =============================================================================

BRAND_CONTEXTS = {
    "magic-mirror": """You are creating a luxury editorial event photo for PicYourBooth Magic Mirror XL,
a high-end DSLR photobooth brand in the Netherlands.

Visual identity: BLACK & GOLD EDITORIAL / LUXURY PORTRAIT
Think: Canon R5 with 85mm f/1.2 L lens. The kind of photo a wedding photographer puts in their portfolio. Vanity Fair Oscar party meets high-end Dutch wedding.

The Magic Mirror XL product:
- Full-length rectangular mirror (approximately 1.8m tall) with a glowing LED frame edge
- The LED frame glows cyan/teal — this is the cool accent against the warm gold environment
- DSLR camera hidden inside captures professional portraits
- Touchscreen mirror surface where guests interact
- Premium piece of furniture, not just equipment — it looks like it BELONGS in a luxury venue
- Usually accompanied by gold stanchions, velvet ropes, backdrop walls

Color system — CRITICAL:
- Deep TRUE BLACKS — shadows are rich and black, NOT lifted (opposite of Party Booth)
- Warm gold (#f59e42) as the key lighting on venue/environment: chandeliers, candles, uplighting
- The Mirror's LED frame glows CYAN/TEAL — the cool complement to warm gold
- Gold + teal/cyan = the Magic Mirror XL signature color pair
- Skin tones: warm, sculpted by directional lighting, portrait-lens beauty with natural pores
- Background bokeh from candles/chandeliers renders as warm golden circles (85mm f/1.2 characteristic)
- NO neon, NO pastels, NO bright daylight — this is evening-only, intentionally dark and luxurious

Photography/lighting style:
- Intentional portrait lighting — NOT just ambient. Think Rembrandt or split lighting on faces
- Key light (warm gold) from one side, subtle rim/hair light from behind
- Deep blacks in shadows, rich warm highlights — high contrast but controlled
- Extremely shallow depth of field (f/1.2) — subject sharp, background melts into creamy bokeh
- Golden bokeh circles from chandeliers and candles in the background
- The 85mm f/1.2 renders skin beautifully — smooth but with real texture, gorgeous subject separation
- People in formal/semi-formal attire: cocktail dresses, tailored blazers, real jewelry catching light
- Elegant venue: dark textured walls, velvet curtains, real flame candles, crystal chandeliers, gold hardware
- Mood: "I can't believe this photo came from a photobooth" — it looks like an editorial portrait
- Every photo should feel like it belongs in a luxury wedding album or magazine spread
""",

    "party-booth": """You are creating a fun, vibrant event photo for PicYourBooth Party Booth,
an accessible digital photobooth brand in the Netherlands.

Visual identity: FUJIFILM INSTAX + NEON MODERN PARTY
Think: Shot on Fujifilm X-T5 with 23mm f/2, Fujifilm Classic Chrome film simulation. A modern house party you'd post on Instagram.

The Party Booth product:
- Floor-standing black photobooth, approximately 1.5 meters tall (waist-to-head height)
- Large illuminated ring light at the top (warm gold glow — this is the PYB brand signature)
- Tablet/screen mounted in the center of the ring light
- Sleek minimal black body/stand from floor to ring light
- NOT a small tabletop device — it stands on the floor and people look UP at it slightly

Color system — CRITICAL:
- The RING LIGHT glows warm gold (#f59e42) — the ONLY gold element, the PYB brand anchor
- Environment has NEON ACCENT lighting: LED strip lights (pink, electric blue), maybe a neon wall sign
- Base lighting is still BRIGHT — not a dark club. Think bright room WITH neon accents
- Balloons: mix of white, clear/transparent, and some bold colors — NOT pastels, NOT gold
- Neon pinks, electric blues, LED greens as accent pops — modern party decorations
- Slightly lifted blacks (Fujifilm film look — shadows are never pure black, but pick up neon color)
- Skin tones are natural-warm, flattering, with subtle neon color reflections
- Overall palette: bright base + neon color pops = "modern house party" not "kids birthday" and not "nightclub"

Photography style:
- BRIGHT overall with neon accent lighting creating colorful highlights and reflections
- Fujifilm film look: gentle grain, lifted shadows that catch neon colors, soft highlights
- The neon accents give it energy and modernity without making it dark
- People in trendy casual: streetwear, sneakers, crop tops, denim jackets, gold jewelry, fun earrings
- Age 20-35, diverse, modern, the kind of people who'd also book a DJ
- Casual venue: modern living room or loft, decorated for a party with LED strips and string lights
- Mood: "This is THE party everyone's posting about" — fun, social, high-energy but still bright
- This is a €199 house party, NOT a €599 premium event — but it looks COOL, not cheap
- NO phones in people's hands unless specifically requested
- This visual style naturally bridges to the DJ upgrade — same crowd, same energy
""",

    "djs": """You are creating an energetic music/nightlife photo for PicYourBooth DJ services,
featuring professional DJs in the Netherlands.

Visual identity: CONCERT PHOTOGRAPHY / STAGE LIGHTING
Think: Sony A7S III with 35mm f/1.4 in a dark venue with stage lighting.

Photography style:
- Dark base exposure with dramatic colored lighting — purple, violet, amber
- Fog/haze catching light beams — atmospheric depth
- High ISO grain is acceptable — adds to the live music feel
- Silhouettes of crowd against lit stage
- DJ in sharp focus behind decks, crowd slightly blurred
- Colored LED wash on faces — not natural skin tones, that's OK for this context
- Mood: immersive, energetic, "you can feel the bass"
- DJ Gianni scenes: coral accent lighting, warm Caribbean/tropical energy
- Milø scenes: mint/cyan accent lighting, minimal underground tech house feel
""",

    "homepage": """You are creating a wide hero image for PicYourBooth,
a photobooth and DJ entertainment brand in the Netherlands.

Visual identity: MIX OF PREMIUM + FUN
Think: Wide establishing shot that shows both the premium and accessible sides.

Photography style:
- Dark cinematic base with warm pockets of light
- Wide-angle (24mm) showing a venue with both photobooth and DJ visible
- Multiple groups of people having fun in different ways
- Rich, warm color palette — amber, gold, with pops of color from the party
- Mood: "This team brings the complete party experience"
""",
}

# Fallback for unknown pages
BRAND_CONTEXTS["offerte"] = BRAND_CONTEXTS["homepage"]

# =============================================================================
# PROMPT TEMPLATES
# =============================================================================

ENHANCE_PROMPT = """{brand_context}

{realism}

I am providing a real photo of our {product} in action.
CRITICAL: Keep the photobooth/equipment EXACTLY as it appears — shape, proportions, screen, ring light.
This is our real product and must remain authentic and recognizable.

Enhancement instructions:
- Transform the ENVIRONMENT to match the visual identity described above
- Upgrade the lighting to match the photography style
- If people are present in the source photo, keep them but enhance naturally
- If generating new people, follow the realism requirements strictly
- Remove any commercial signage, brand logos, cables, or clutter
- Keep the composition balanced with room for text overlay on the left or right third

Scene context: {scene_description}

Output: High-resolution, {aspect_ratio} format. Must pass as a real photograph."""

GENERATE_PROMPT = """{brand_context}

{realism}

Generate this scene from scratch:
{scene_description}

CRITICAL quality checks:
- This must look like a REAL PHOTOGRAPH taken by a professional event photographer
- NOT a stock photo, NOT an illustration, NOT a 3D render
- If people are in the scene, they must have natural skin, real expressions, and individual features
- The lighting must be physically accurate — light sources should cast real shadows and highlights
- Include subtle environmental details: condensation on glasses, wrinkles in tablecloths, scuff marks on floors

Output: High-resolution, {aspect_ratio} format. Must be indistinguishable from a real photo."""

# =============================================================================
# PER-PAGE SCENE DESCRIPTIONS
# =============================================================================

SCENES = {
    "magic-mirror": {
        "hero": "The Magic Mirror XL photobooth seen from a 3/4 angle in an elegant dark venue. The mirror is a tall (1.8m) sleek rectangular mirror with a glowing cyan/teal LED edge frame — the teal glow contrasts beautifully against the warm gold environment. A couple in cocktail attire (woman in a black dress with gold jewelry, man in a dark tailored blazer) are posing in front of it, laughing naturally, the woman's hand on his chest, mid-conversation energy. Behind the mirror: dark textured walls with warm gold uplighting, crystal chandeliers creating golden bokeh circles, real flame candles on surfaces. Gold stanchions with velvet ropes define the photobooth area. The floor is dark hardwood or marble. The lighting is intentional and directional — warm key light from the left sculpts their faces (Rembrandt lighting), a subtle rim light from behind separates them from the dark background. The mirror's cyan LED glow illuminates the floor around it. Shot on Canon R5 with 85mm f/1.2 L — extremely shallow depth of field, the couple is tack-sharp while the background melts into gorgeous warm golden bokeh. Deep blacks, rich contrast, luxury editorial feel.",
        "usp-1": "Close-up of hands holding a freshly printed photo strip, the print still warm. The strip shows four frames of friends making silly faces. Behind: blurred warm party lights, someone's champagne glass catching the light. Shot at f/1.8, macro-style with shallow depth.",
        "usp-2": "A woman in a cocktail dress stepping in front of professional ring lighting at the Magic Mirror. The light wraps around her face beautifully — you can see the catchlights in her eyes. She's mid-laugh, one hand touching her necklace. Dark background with warm bokeh. Shot at f/1.4, portrait style.",
        "usp-3": "A guest holding a freshly printed photo strip between two fingers, showing it to a friend who is reacting with delight. Warm event lighting, dark venue background with candles. The print is sharp, the background beautifully blurred. Shot at f/2.0.",
        "usp-4": "Red velvet carpet leading to the Magic Mirror setup. Gold stanchions with velvet ropes on either side. A shimmer wall backdrop catches the light. One couple is walking down the carpet toward the mirror, seen from behind. Elegant, VIP atmosphere. Shot at f/2.8, wide angle.",
    },
    "party-booth": {
        "hero": "A bright, modern house party in a stylish living room or loft space. The Party Booth is seen from a 3/4 angle (not straight-on) — it is a tall (1.5m) sleek black floor-standing photobooth with a large illuminated ring light at the top glowing warm gold, and a tablet screen in the center. The booth is angled so we see its profile/silhouette more than the screen. A group of 4-5 friends in their mid-20s to early 30s wearing trendy casual clothes (streetwear, denim jacket, crop top, fresh sneakers, gold hoop earrings) are gathered around the booth, laughing together, some posing, candid energy. Behind them: an LED strip light on the wall glowing neon pink/magenta, some string lights. White and clear balloons with a few bold-colored ones. A small neon sign or LED letters on a shelf. The room is BRIGHT overall — the base lighting is warm and well-lit, but the neon accents add electric pink and blue color pops to the shadows and reflections on skin. The ring light's warm gold glow is the anchor point. Hardwood or concrete floors, modern furniture. Shot on Fujifilm X-T5, 23mm f/2, Classic Chrome film simulation, gentle film grain, slightly lifted shadows catching the neon colors.",
        "usp-1": "Close-up of two friends' hands holding their phones side by side, both showing the same photobooth photo they just received via QR code. One phone shows the WhatsApp share screen. Background: blurred colorful party with fairy lights and balloons. Bright, warm Fujifilm look. Shot at f/2.0.",
        "usp-2": "A woman in a casual striped top is placing the Party Booth on a kitchen table, plugging it in. The ring light just turned on, casting a warm glow on her face. She's smiling, it's clearly easy. Behind her: a living room being set up for a party — half-inflated balloons, a stack of paper plates, streamers not yet hung. Natural afternoon daylight. Real, unposed moment. Shot at f/2.8.",
        "usp-3": "The Party Booth sitting on a small side table in a tiny apartment balcony party. Fairy lights wrapped around the railing, a few friends squeezed onto the small balcony, city rooftops in the background at golden hour. Shows the booth fits ANYWHERE. Warm, intimate, fun. Shot on Fujifilm with golden hour glow.",
        "usp-4": "Split composition: left third shows a regular phone selfie (slightly blue-tinted, flat lighting, messy background visible). Right two-thirds shows the same person's Party Booth photo with AI background — clean, warm, beautiful setting behind them, skin looks great with beautify filter. The difference is night and day. The AI-enhanced side has the warm Fujifilm look.",
    },
    "djs": {
        "hero": "DJ behind a Pioneer controller at an intimate venue. Purple and amber stage lighting cuts through fog/haze. The DJ is focused, one hand on the jogwheel, headphones on one ear. Crowd silhouettes in the foreground, some hands raised. Laser beams cutting through the haze above. The energy is immersive — you can almost hear the music. Shot at f/1.4, high ISO, slight grain.",
        "gianni": "DJ Gianni performing at a warm, tropical-themed party. Coral and amber lighting. The DJ is energetic, one fist raised, smiling. Crowd is dancing, some singing along. Decorative palm leaves and warm Edison bulbs in the background. Caribbean/afrobeats energy. Shot at f/2.0 with warm tones.",
        "milo": "Milø performing a deep house set in a minimal, underground setting. Cool mint/cyan lighting with fog. The DJ is focused and in the zone, headphones on, adjusting levels. Small, intimate crowd moving to the rhythm. Dark concrete walls, minimal decor. The mood is hypnotic. Shot at f/1.4, moody.",
    },
    "homepage": {
        "hero": "Wide shot of a premium event space with both the Magic Mirror XL photobooth (left side, LED-lit, guests posing) and a DJ setup (right side, purple/amber lighting, crowd dancing) visible. The venue is dark with warm pockets of light. Multiple groups of people — some posing at the photobooth, some dancing, some chatting with drinks. It feels like one cohesive party experience. Shot at f/4.0, wide angle, showing the full scene.",
    },
}

# =============================================================================
# ASPECT RATIOS
# =============================================================================

ASPECT_RATIOS = {
    "hero": "16:9 landscape",
    "usp": "1:1 square",
    "card": "3:2 landscape",
    "modal": "4:3 landscape",
    "og": "1.91:1 landscape",
}
