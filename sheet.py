#!/usr/bin/env python3
"""
Game Boy Camera Contact Sheet Generator
Creates overview sheets showing all palette variations for each image
"""

import os
import sys
from PIL import Image, ImageDraw, ImageFont
import numpy as np
from datetime import datetime
import glob
from palettes import PALETTES

def create_contact_sheet_for_image(base_dir, image_name):
    """
    Create a contact sheet for a single image showing all palette variations
    """
    # Calculate grid dimensions - use 3x3 grid
    num_palettes = len(PALETTES)
    cols = 3  # 3x3 grid layout
    rows = 3

    # Load first image to get dimensions
    first_palette = list(PALETTES.keys())[0]
    sample_path = f"{base_dir}/{first_palette}/{image_name}.png"

    if not os.path.exists(sample_path):
        print(f"Warning: {sample_path} not found, skipping contact sheet for {image_name}")
        return None

    # Get image dimensions
    with Image.open(sample_path) as sample_img:
        img_width, img_height = sample_img.size

    # Scale down for contact sheet (original is 400%, we'll use 200% for contact)
    scale_factor = 0.5
    thumb_width = int(img_width * scale_factor)
    thumb_height = int(img_height * scale_factor)

    # Contact sheet dimensions
    padding = 20
    label_height = 30
    cell_width = thumb_width + padding
    cell_height = thumb_height + label_height + padding

    contact_width = cols * cell_width + padding
    contact_height = rows * cell_height + padding

    # Create contact sheet canvas
    contact_sheet = Image.new('RGB', (contact_width, contact_height), (240, 240, 240))

    # Try to load a font for labels
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 12)
    except:
        font = ImageFont.load_default()

    draw = ImageDraw.Draw(contact_sheet)

    # Place each palette variation
    palette_names = list(PALETTES.keys())
    for i, palette_name in enumerate(palette_names):
        # Calculate grid position
        row = i // cols
        col = i % cols

        # Load the image for this palette
        img_path = f"{base_dir}/{palette_name}/{image_name}.png"

        if os.path.exists(img_path):
            # Load and resize image
            with Image.open(img_path) as img:
                img_resized = img.resize((thumb_width, thumb_height), Image.NEAREST)

            # Calculate position
            x = col * cell_width + padding
            y = row * cell_height + padding

            # Paste image
            contact_sheet.paste(img_resized, (x, y))

            # Add label
            label_y = y + thumb_height + 5
            draw.text((x, label_y), palette_name, fill=(0, 0, 0), font=font)

    # Save contact sheet
    contact_path = f"{base_dir}/{image_name}_contact.png"
    contact_sheet.save(contact_path)

    return contact_path

def create_all_contact_sheets(base_dir=None):
    """
    Create contact sheets for all processed images
    """
    # Get current date directory if not specified
    if base_dir is None:
        current_date = datetime.now().strftime("%Y-%m-%d")
        base_dir = current_date

    if not os.path.exists(base_dir):
        print(f"No processed images found in {base_dir}/")
        print("Run convert.py first to process images.")
        return

    # Find all processed images by checking the first palette directory
    first_palette = list(PALETTES.keys())[0]
    first_palette_dir = f"{base_dir}/{first_palette}"

    if not os.path.exists(first_palette_dir):
        print(f"No palette directories found in {base_dir}/")
        return

    # Get list of processed images
    processed_images = []
    for file in os.listdir(first_palette_dir):
        if file.endswith('.png'):
            image_name = file[:-4]  # Remove .png extension
            processed_images.append(image_name)

    if not processed_images:
        print("No processed PNG files found")
        return

    print(f"Creating contact sheets for {len(processed_images)} images...")
    print(f"Grid: 3 columns × 3 rows")
    print()

    created_count = 0
    for image_name in sorted(processed_images):
        print(f"Creating contact sheet for: {image_name}")
        contact_path = create_contact_sheet_for_image(base_dir, image_name)

        if contact_path:
            print(f"  ✓ Saved: {contact_path}")
            created_count += 1
        else:
            print(f"  ✗ Failed")

    print()
    print(f"📋 Contact sheet generation complete!")
    print(f"📁 Saved {created_count} contact sheets to: {base_dir}/")
    print(f"🎨 Each sheet shows {len(PALETTES)} palette variations in a 3×3 grid")

    return created_count

if __name__ == "__main__":
    create_all_contact_sheets()