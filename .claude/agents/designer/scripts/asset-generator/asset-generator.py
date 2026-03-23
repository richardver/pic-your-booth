#!/usr/bin/env python3
"""
PicYourBooth Asset Generator

Two modes:
  1. enhance — Real photo as reference + Gemini AI styling
  2. generate — Text prompt only, Gemini creates from scratch

Then: resize/crop to all needed dimensions, convert to WebP.

Usage:
  python asset-generator.py enhance --source path/to/photo.jpg --page magic-mirror --usage hero
  python asset-generator.py generate --page magic-mirror --usage hero --scene "Custom scene description"
  python asset-generator.py resize --input path/to/image.png --page magic-mirror --usage hero
"""

import os
import sys
import argparse
from pathlib import Path
from dotenv import load_dotenv

# Load .env from project root
PROJECT_ROOT = Path(__file__).resolve().parents[5]  # up from scripts/asset-generator/ to project root
load_dotenv(PROJECT_ROOT / ".env")

try:
    from PIL import Image
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


def setup_gemini():
    """Configure Gemini API."""
    api_key = os.getenv("GOOGLE_AI_API_KEY")
    if not api_key or api_key == "your_api_key_here":
        print("Error: GOOGLE_AI_API_KEY not set in .env")
        sys.exit(1)
    client = genai.Client(api_key=api_key)
    return client


def enhance_image(client, source_path, page, usage, scene_override=None):
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

    # Read source image
    print("Reading source photo...")
    source_image = Image.open(source)

    # Generate with Gemini
    print("Generating styled image with Gemini...")
    response = client.models.generate_content(
        model="gemini-3-pro-image-preview",
        contents=[prompt, source_image],
        config=types.GenerateContentConfig(
            response_modalities=["IMAGE", "TEXT"],
        ),
    )

    # Save generated image
    output_name = f"{page}-{usage}-generated.png"
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


def generate_image(client, page, usage, scene_override=None):
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

    output_name = f"{page}-{usage}-generated.png"
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


def resize_image(input_path, page, usage):
    """Resize a master image to all needed dimensions and convert to WebP."""
    input_path = Path(input_path)
    if not input_path.exists():
        print(f"Error: Input image not found: {input_path}")
        sys.exit(1)

    WEB_DIR.mkdir(parents=True, exist_ok=True)

    img = Image.open(input_path)
    if img.mode == "RGBA":
        img = img.convert("RGB")

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

        # Save WebP
        webp_name = f"{page}-{usage}-{width}x{height}.webp"
        webp_path = WEB_DIR / webp_name
        resized.save(webp_path, "WEBP", quality=WEBP_QUALITY)
        output_files.append(webp_path)
        print(f"  WebP: {webp_name}")

        # Also save PNG for OG images
        if usage == "og":
            png_name = f"{page}-{usage}-{width}x{height}.png"
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

    # Generate mode
    gen_parser = subparsers.add_parser("generate", help="Generate image from scratch")
    gen_parser.add_argument("--page", required=True, choices=["homepage", "magic-mirror", "party-booth", "djs", "offerte"])
    gen_parser.add_argument("--usage", required=True, choices=list(SIZES.keys()))
    gen_parser.add_argument("--scene", help="Custom scene description (overrides default)")

    # Resize mode (no AI, just resize an existing image)
    resize_parser = subparsers.add_parser("resize", help="Resize an existing image to web sizes")
    resize_parser.add_argument("--input", required=True, help="Path to input image")
    resize_parser.add_argument("--page", required=True, choices=["homepage", "magic-mirror", "party-booth", "djs", "offerte"])
    resize_parser.add_argument("--usage", required=True, choices=list(SIZES.keys()))

    args = parser.parse_args()

    if not args.mode:
        parser.print_help()
        sys.exit(1)

    print(f"\n{'='*50}")
    print(f"PicYourBooth Asset Generator")
    print(f"Mode: {args.mode}")
    print(f"{'='*50}\n")

    if args.mode == "resize":
        files = resize_image(args.input, args.page, args.usage)
        print(f"\nGenerated {len(files)} files in {WEB_DIR}")
        return

    # AI modes need Gemini
    client = setup_gemini()

    if args.mode == "enhance":
        result = enhance_image(client, args.source, args.page, args.usage, args.scene)
    elif args.mode == "generate":
        result = generate_image(client, args.page, args.usage, args.scene)

    if result:
        print(f"\nResizing to web dimensions...")
        files = resize_image(result, args.page, args.usage)
        print(f"\nDone! Generated {len(files)} web-ready files in {WEB_DIR}")
    else:
        print("\nFailed to generate image.")
        sys.exit(1)


if __name__ == "__main__":
    main()
