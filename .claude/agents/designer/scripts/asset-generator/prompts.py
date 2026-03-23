"""
Prompt templates for Gemini image generation.
PicYourBooth brand style: dark cinematic, warm lighting, premium event atmosphere.
"""

BRAND_CONTEXT = """You are creating a premium event photography image for PicYourBooth,
a photobooth and DJ entertainment brand based in the Randstad, Netherlands.

Style guidelines:
- Dark cinematic atmosphere, like walking into a VIP event at night
- Warm lighting with amber/orange tones (brand color #f59e42)
- Professional, premium feel but approachable and fun
- Real event energy: guests laughing, dancing, enjoying
- Clean composition with room for text overlay if needed
- Photorealistic quality, not illustrated or cartoon
- No text, logos, or watermarks in the image"""

ENHANCE_PROMPT = """{brand_context}

I am providing a real photo of our {product} in action at an event.
Keep the photobooth/equipment exactly as it appears — this is our real product
and must look authentic. Enhance the following:
- Improve the overall lighting to be more cinematic and atmospheric
- Make the venue feel more premium and elegant
- Enhance colors to match our dark/warm brand aesthetic
- Keep the event energy and any people visible
- Do not change the product itself, only the environment and mood

Scene context: {scene_description}

Output: High-resolution, photorealistic, {aspect_ratio} format."""

GENERATE_PROMPT = """{brand_context}

Generate a new scene from scratch:
{scene_description}

The image should feel like a real photo taken at a premium event,
not like a stock photo or AI-generated image.

Output: High-resolution, photorealistic, {aspect_ratio} format."""

# Per-page scene suggestions
SCENES = {
    "magic-mirror": {
        "hero": "Premium fotospiegel photobooth at an elegant evening event. Dark venue with warm ambient lighting. Guests in semi-formal attire having fun. The mirror booth is the focal point, glowing with LED frame lights.",
        "usp-1": "Close-up of a professional camera and studio lighting setup at an event. Warm tones, shallow depth of field.",
        "usp-2": "Guest stepping in front of professional studio lighting, looking great. Warm flattering light on their face.",
        "usp-3": "Guest holding a freshly printed photo strip, smiling. Warm event lighting in background.",
        "usp-4": "Red carpet and velvet stanchions leading to a photobooth. VIP premium setup with elegant props.",
    },
    "party-booth": {
        "hero": "Colorful, fun party atmosphere with a compact digital photobooth on a table. Birthday decorations, balloons, warm festive lighting. Casual, accessible, joyful.",
        "usp-1": "Friends looking at phone screens, sharing photos via QR code. Warm party lighting, social media vibe.",
        "usp-2": "Someone easily setting up a compact photobooth on a table. Simple, quick, no stress.",
        "usp-3": "Compact photobooth fitting perfectly in a living room party setting. Cozy but fun.",
        "usp-4": "Before/after comparison of a photo: messy background vs AI-enhanced clean background with beautify filter.",
    },
    "djs": {
        "hero": "DJ performing at a premium nightlife event. Purple/violet lighting, fog machine, crowd dancing. Dark, energetic, immersive atmosphere.",
        "gianni": "DJ performing Afro Beats set. Warm coral-toned lighting. Energetic crowd, tropical vibes, sunset party atmosphere.",
        "milo": "DJ performing deep house set. Cool mint/green lighting. Minimal, immersive, late-night underground feel.",
    },
    "homepage": {
        "hero": "Wide shot of a premium event with both photobooth and DJ setup visible. Dark cinematic venue, warm lighting, guests having the time of their lives.",
    },
}

# Aspect ratios
ASPECT_RATIOS = {
    "hero": "16:9 landscape",
    "usp": "1:1 square",
    "card": "3:2 landscape",
    "modal": "4:3 landscape",
    "og": "1.91:1 landscape",
}
