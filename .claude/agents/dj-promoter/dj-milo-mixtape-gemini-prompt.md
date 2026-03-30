# Milø - Mixtape Cover Gemini Prompt

Prompt workflow for generating mixtape and SoundCloud cover art via Gemini. Two-step process: generate base with Imagen, then edit text with Flash Image.

---

## Method: Two-Step (Imagen + Flash Image Edit)

Imagen 4.0 cannot render the Ø character. The working method:

1. **Step 1:** Generate base cover with `imagen-4.0-generate-001` using "MILO" (regular O)
2. **Step 2:** Edit text from MILO → MILØ using `gemini-2.5-flash-image` with the base as reference

Once you have one good base cover, use it as the reference image for all genre variants.

---

## Step 1: Base Cover Prompt (Imagen 4.0)

Use `imagen-4.0-generate-001` with `aspect_ratio='1:1'`:

```
Minimalist vinyl record sleeve mockup. A light matte white cardboard record sleeve standing upright with a black vinyl record partially sliding out from behind it to the right. The vinyl grooves catch subtle [ACCENT COLOR] light reflections. Clean bright studio background with soft natural lighting.

On the front of the sleeve:
- "MILO" in large bold condensed sans-serif black text, left-aligned
- "[SERIES NAME]" below in smaller uppercase text
- "Deep in the groove" in small italic text below
- Small diamond shape logo bottom left corner

Ultra-minimal. Bright clean studio lighting from above. White matte cardboard sleeve texture. Premium underground DJ vinyl pressing aesthetic. Lots of negative space on the sleeve. The vinyl record has a subtle [ACCENT COLOR] colored center label.

No people. No busy elements. Clean, bright studio photography style.
```

## Step 2: Text Edit Prompt (Gemini 2.5 Flash Image)

Use `gemini-2.5-flash-image` with the Step 1 output as reference image:

**For the base genre (Tech House):**
```
Edit this vinyl sleeve image. Change the text MILO to MILØ — the last letter should be the Scandinavian letter Ø (an O with a diagonal stroke through it). Keep everything else exactly the same — same sleeve, same vinyl, same composition, same lighting, same other text.
```

**For other genres (use the Tech House base as reference):**
```
Edit this vinyl sleeve image. Change the text MILO to MILØ — the last letter should be the Scandinavian letter Ø (an O with a diagonal stroke through it). Also change [OLD SERIES] to [NEW SERIES]. Change the vinyl center label color from [OLD COLOR] to [NEW COLOR]. Keep everything else the same.
```

---

## Python Implementation

```python
from google import genai
from google.genai import types
from dotenv import load_dotenv
import os

load_dotenv()
client = genai.Client(api_key=os.getenv('GOOGLE_AI_API_KEY'))

# Step 1: Generate base cover with Imagen
response = client.models.generate_images(
    model='imagen-4.0-generate-001',
    prompt=base_prompt,  # See template above
    config=types.GenerateImagesConfig(number_of_images=1, aspect_ratio='1:1')
)
response.generated_images[0].image.save('base-cover.png')

# Step 2: Edit text MILO → MILØ with Flash Image
with open('base-cover.png', 'rb') as f:
    ref_bytes = f.read()

response = client.models.generate_content(
    model='gemini-2.5-flash-image',
    contents=[
        types.Part.from_bytes(data=ref_bytes, mime_type='image/png'),
        edit_prompt  # See template above
    ],
    config=types.GenerateContentConfig(response_modalities=['IMAGE'])
)

for part in response.candidates[0].content.parts:
    if hasattr(part, 'inline_data') and part.inline_data is not None:
        with open('final-cover.png', 'wb') as f:
            f.write(part.inline_data.data)
        break
```

---

## Genre Accent Colors

Each mixtape series uses a different accent color from Milø's cool palette. Swap the accent color and series name accordingly.

| Genre | Accent | Hex | Vinyl Label Color | Series Name |
|-------|--------|-----|-------------------|-------------|
| **Tech House** | Cyan | `#34d399` | Cyan/green | TECH HOUSE SESSIONS VOL X |
| **House** | Electric Blue | `#38bdf8` | Electric blue | HOUSE GROOVES VOL X |
| **Deep** | Violet | `#8b5cf6` | Violet/purple | DEEP CUTS VOL X |

**Never use:** `#f0654a` (Gianni's coral), `#f5b731`, or any warm orange/amber/red tones.

---

## Cover Style: Vinyl Minimalist

| Attribute | Specification |
|-----------|--------------|
| Style | Vinyl record sleeve product photography mockup |
| Sleeve | Light/white matte cardboard, standing upright |
| Vinyl | Black record partially visible behind sleeve, genre-colored center label |
| Background | Clean bright studio, soft natural light |
| Typography | "MILØ" large bold condensed sans-serif, black on white sleeve |
| Series name | Smaller uppercase below MILØ |
| Tagline | "Deep in the groove" small italic |
| Logo | Diamond (M) shape, bottom-left corner |
| Composition | Left-aligned text, vinyl sliding out right |
| Mood | Premium, collectible, clean & bright vinyl pressing |

---

## Exported Covers

| Cover | Path |
|-------|------|
| Tech House | `images/dj-milo/mixtape/tech-house-mixtape-cover-gemini.png` |
| House | `images/dj-milo/mixtape/house-mixtape-cover-gemini.png` |
| Deep | `images/dj-milo/mixtape/deep-mixtape-cover-gemini.png` |
| Tech House (Playwright) | `images/dj-milo/mixtape/tech-house-mixtape-cover.png` |
| House (Playwright) | `images/dj-milo/mixtape/house-mixtape-cover.png` |
| Deep (Playwright) | `images/dj-milo/mixtape/deep-mixtape-cover.png` |

---

## Key Learnings

- `imagen-4.0-generate-001` cannot render Ø — always outputs Ö, Á, or garbage
- `gemini-2.5-flash-image` with a reference image can edit MILO → MILØ reliably
- Keep prompts simple and descriptive — avoid CSS/hex codes in Imagen prompts (it renders them as text)
- The vinyl sleeve mockup style produces the most consistent results
- Always generate the base Tech House cover first, then use it as reference for other genres
