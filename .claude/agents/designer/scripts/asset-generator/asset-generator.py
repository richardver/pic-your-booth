#!/usr/bin/env python3
"""
PicYourBooth Asset Generator

Three modes:
  1. enhance — Real photo as reference + Gemini AI styling
  2. generate — Text prompt only, Gemini creates from scratch
  3. resize  — No AI, just resize/crop an existing image

Then: apply brand color grading, resize/crop to all needed dimensions, convert to WebP.

Usage:
  python asset-generator.py enhance --source path/to/photo.jpg --page magic-mirror --usage hero
  python asset-generator.py enhance --source photo.jpg --page magic-mirror --usage usp --name fotos-inlijsten
  python asset-generator.py generate --page magic-mirror --usage hero --scene "Custom scene description"
  python asset-generator.py resize --input path/to/image.png --page magic-mirror --usage hero
"""

import os
import sys
import argparse
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

# Load .env from project root
PROJECT_ROOT = Path(__file__).resolve().parents[5]  # up from scripts/asset-generator/ to project root
load_dotenv(PROJECT_ROOT / ".env")

try:
    from PIL import Image, ImageEnhance, ImageOps
except ImportError:
    print("Error: Pillow not installed. Run: pip install Pillow")
    sys.exit(1)

try:
    from google import genai
    from google.genai import types
except ImportError:
    print("Error: google-genai not installed. Run: pip install google-genai")
    sys.exit(1)

from prompts import BRAND_CONTEXT, ENHANCE_PROMPT, GENERATE_PROMPT, SCENES, ASPECT_RATIOS

# Output directories
GENERATED_DIR = PROJECT_ROOT / "docs" / "assets" / "generated"
WEB_DIR = PROJECT_ROOT / "docs" / "assets" / "web"

# Size configs per usage type
SIZES = {
    "hero": [(1920, 1080), (1280, 720), (768, 432)],
    "usp": [(400, 400)],
    "card": [(600, 400)],
    "modal": [(800, 600)],
    "og": [(1200, 630)],
}

WEBP_QUALITY = 85

# Brand color grading presets per page
COLOR_GRADES = {
    "magic-mirror": {
        "red_mult": 1.06,
        "blue_mult": 0.90,
        "green_mult": 1.01,
        "contrast": 1.12,
        "saturation": 1.10,
        "sharpness": 1.15,
        "brightness": 1.0,
    },
    "party-booth": {
        "red_mult": 1.05,
        "blue_mult": 0.92,
        "green_mult": 1.0,
        "contrast": 1.14,
        "saturation": 1.18,
        "sharpness": 1.12,
        "brightness": 1.04,
    },
    "djs": {
        "red_mult": 1.02,
        "blue_mult": 1.02,
        "green_mult": 1.0,
        "contrast": 1.15,
        "saturation": 1.12,
        "sharpness": 1.10,
        "brightness": 0.98,
    },
    "homepage": {
        "red_mult": 1.04,
        "blue_mult": 0.93,
        "green_mult": 1.01,
        "contrast": 1.10,
        "saturation": 1.08,
        "sharpness": 1.10,
        "brightness": 1.0,
    },
}


def build_output_name(page, usage, name=None, ext="png"):
    """Build unique output filename. Uses --name if provided, else timestamp."""
    if name:
        return f"{page}-{usage}-{name}.{ext}"
    timestamp = datetime.now().strftime("%H%M%S")
    return f"{page}-{usage}-{timestamp}.{ext}"


def apply_color_grade(img, page):
    """Apply brand color grading based on page/product."""
    grade = COLOR_GRADES.get(page, COLOR_GRADES["homepage"])

    # Channel adjustments
    r, g, b = img.split()
    r = r.point(lambda x: min(255, int(x * grade["red_mult"])))
    g = g.point(lambda x: min(255, int(x * grade["green_mult"])))
    b = b.point(lambda x: int(x * grade["blue_mult"]))
    img = Image.merge("RGB", (r, g, b))

    # Enhancement chain
    img = ImageEnhance.Contrast(img).enhance(grade["contrast"])
    img = ImageEnhance.Color(img).enhance(grade["saturation"])
    img = ImageEnhance.Sharpness(img).enhance(grade["sharpness"])
    img = ImageEnhance.Brightness(img).enhance(grade["brightness"])

    return img


def setup_gemini():
    """Configure Gemini API."""
    api_key = os.getenv("GOOGLE_AI_API_KEY")
    if not api_key or api_key == "your_api_key_here":
        print("Error: GOOGLE_AI_API_KEY not set in .env")
        sys.exit(1)
    client = genai.Client(api_key=api_key)
    return client


def enhance_image(client, source_path, page, usage, scene_override=None, name=None):
    """Mode 1: Enhance a real photo with Gemini AI styling."""
    source = Path(source_path)
    if not source.exists():
        print(f"Error: Source photo not found: {source}")
        sys.exit(1)

    print(f"Enhancing: {source.name}")
    print(f"Page: {page}, Usage: {usage}")

    # Build prompt
    scene = scene_override or SCENES.get(page, {}).get(usage, "Premium event atmosphere")
    aspect = ASPECT_RATIOS.get(usage, "16:9 landscape")
    prompt = ENHANCE_PROMPT.format(
        brand_context=BRAND_CONTEXT,
        product="Magic Mirror XL photobooth" if "mirror" in page else "Party Booth" if "party" in page else "DJ setup",
        scene_description=scene,
        aspect_ratio=aspect,
    )

    # Read source image (auto-rotate based on EXIF)
    print("Reading source photo...")
    source_image = ImageOps.exif_transpose(Image.open(source))

    # Generate with Gemini
    print("Generating styled image with Gemini...")
    response = client.models.generate_content(
        model="gemini-3-pro-image-preview",
        contents=[prompt, source_image],
        config=types.GenerateContentConfig(
            response_modalities=["IMAGE", "TEXT"],
        ),
    )

    # Save generated image with unique name
    output_name = build_output_name(page, usage, name, "png")
    output_path = GENERATED_DIR / output_name
    GENERATED_DIR.mkdir(parents=True, exist_ok=True)

    if response.candidates:
        for part in response.candidates[0].content.parts:
            if part.inline_data and part.inline_data.mime_type.startswith("image/"):
                with open(output_path, "wb") as f:
                    f.write(part.inline_data.data)
                print(f"Saved: {output_path}")
                return output_path
            elif part.text:
                print(f"Gemini response text: {part.text[:200]}")

    print("Error: No image in Gemini response")
    return None


def generate_image(client, page, usage, scene_override=None, name=None):
    """Mode 2: Generate image from scratch with Gemini."""
    print(f"Generating from scratch")
    print(f"Page: {page}, Usage: {usage}")

    scene = scene_override or SCENES.get(page, {}).get(usage, "Premium event atmosphere")
    aspect = ASPECT_RATIOS.get(usage, "16:9 landscape")
    prompt = GENERATE_PROMPT.format(
        brand_context=BRAND_CONTEXT,
        scene_description=scene,
        aspect_ratio=aspect,
    )

    print("Generating image with Gemini...")
    response = client.models.generate_content(
        model="gemini-3-pro-image-preview",
        contents=prompt,
        config=types.GenerateContentConfig(
            response_modalities=["IMAGE", "TEXT"],
        ),
    )

    output_name = build_output_name(page, usage, name, "png")
    output_path = GENERATED_DIR / output_name
    GENERATED_DIR.mkdir(parents=True, exist_ok=True)

    if response.candidates:
        for part in response.candidates[0].content.parts:
            if part.inline_data and part.inline_data.mime_type.startswith("image/"):
                with open(output_path, "wb") as f:
                    f.write(part.inline_data.data)
                print(f"Saved: {output_path}")
                return output_path
            elif part.text:
                print(f"Gemini response text: {part.text[:200]}")

    print("Error: No image in Gemini response")
    return None


def resize_image(input_path, page, usage, name=None, grade=True):
    """Resize a master image to all needed dimensions, apply color grading, convert to WebP."""
    input_path = Path(input_path)
    if not input_path.exists():
        print(f"Error: Input image not found: {input_path}")
        sys.exit(1)

    WEB_DIR.mkdir(parents=True, exist_ok=True)

    img = Image.open(input_path)
    img = ImageOps.exif_transpose(img)
    if img.mode == "RGBA":
        img = img.convert("RGB")

    # Apply brand color grading
    if grade:
        print(f"  Applying {page} color grade...")
        img = apply_color_grade(img, page)

    sizes = SIZES.get(usage, [(1920, 1080)])
    output_files = []

    for width, height in sizes:
        # Calculate crop box (center-weighted)
        img_ratio = img.width / img.height
        target_ratio = width / height

        if img_ratio > target_ratio:
            # Image is wider — crop sides
            new_width = int(img.height * target_ratio)
            left = (img.width - new_width) // 2
            box = (left, 0, left + new_width, img.height)
        else:
            # Image is taller — crop top/bottom
            new_height = int(img.width / target_ratio)
            top = (img.height - new_height) // 2
            box = (0, top, img.width, top + new_height)

        cropped = img.crop(box)
        resized = cropped.resize((width, height), Image.LANCZOS)

        # Build filename
        if name:
            webp_name = f"{page}-{usage}-{name}-{width}x{height}.webp"
        else:
            webp_name = f"{page}-{usage}-{width}x{height}.webp"

        webp_path = WEB_DIR / webp_name
        resized.save(webp_path, "WEBP", quality=WEBP_QUALITY)
        output_files.append(webp_path)
        print(f"  WebP: {webp_name}")

        # Also save PNG for OG images
        if usage == "og":
            png_name = webp_name.replace(".webp", ".png")
            png_path = WEB_DIR / png_name
            resized.save(png_path, "PNG")
            output_files.append(png_path)
            print(f"  PNG:  {png_name}")

    return output_files


def main():
    parser = argparse.ArgumentParser(description="PicYourBooth Asset Generator")
    subparsers = parser.add_subparsers(dest="mode", help="Generation mode")

    # Enhance mode
    enhance_parser = subparsers.add_parser("enhance", help="Enhance a real photo with AI")
    enhance_parser.add_argument("--source", required=True, help="Path to source photo")
    enhance_parser.add_argument("--page", required=True, choices=["homepage", "magic-mirror", "party-booth", "djs", "offerte"])
    enhance_parser.add_argument("--usage", required=True, choices=list(SIZES.keys()))
    enhance_parser.add_argument("--scene", help="Custom scene description (overrides default)")
    enhance_parser.add_argument("--name", help="Asset name (e.g. 'fotos-inlijsten'). Prevents file overwrites.")
    enhance_parser.add_argument("--no-grade", action="store_true", help="Skip brand color grading")

    # Generate mode
    gen_parser = subparsers.add_parser("generate", help="Generate image from scratch")
    gen_parser.add_argument("--page", required=True, choices=["homepage", "magic-mirror", "party-booth", "djs", "offerte"])
    gen_parser.add_argument("--usage", required=True, choices=list(SIZES.keys()))
    gen_parser.add_argument("--scene", help="Custom scene description (overrides default)")
    gen_parser.add_argument("--name", help="Asset name (e.g. 'vip-upgrade'). Prevents file overwrites.")
    gen_parser.add_argument("--no-grade", action="store_true", help="Skip brand color grading")

    # Resize mode (no AI, just resize an existing image)
    resize_parser = subparsers.add_parser("resize", help="Resize an existing image to web sizes")
    resize_parser.add_argument("--input", required=True, help="Path to input image")
    resize_parser.add_argument("--page", required=True, choices=["homepage", "magic-mirror", "party-booth", "djs", "offerte"])
    resize_parser.add_argument("--usage", required=True, choices=list(SIZES.keys()))
    resize_parser.add_argument("--name", help="Asset name for output files")
    resize_parser.add_argument("--no-grade", action="store_true", help="Skip brand color grading")

    args = parser.parse_args()

    if not args.mode:
        parser.print_help()
        sys.exit(1)

    print(f"\n{'='*50}")
    print(f"PicYourBooth Asset Generator")
    print(f"Mode: {args.mode}")
    if hasattr(args, "name") and args.name:
        print(f"Name: {args.name}")
    print(f"{'='*50}\n")

    grade = not getattr(args, "no_grade", False)
    name = getattr(args, "name", None)

    if args.mode == "resize":
        files = resize_image(args.input, args.page, args.usage, name=name, grade=grade)
        print(f"\nGenerated {len(files)} files in {WEB_DIR}")
        return

    # AI modes need Gemini
    client = setup_gemini()

    if args.mode == "enhance":
        result = enhance_image(client, args.source, args.page, args.usage, args.scene, name=name)
    elif args.mode == "generate":
        result = generate_image(client, args.page, args.usage, args.scene, name=name)

    if result:
        print(f"\nResizing to web dimensions...")
        files = resize_image(result, args.page, args.usage, name=name, grade=grade)
        print(f"\nDone! Generated {len(files)} web-ready files in {WEB_DIR}")
    else:
        print("\nFailed to generate image.")
        sys.exit(1)


if __name__ == "__main__":
    main()
