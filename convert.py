#!/usr/bin/env python3
"""
Game Boy Camera Image Converter
Converts BMP files to PNG with Game Boy color palettes and upscaling
"""

import os
import sys
import shutil
from PIL import Image
import numpy as np
from datetime import datetime
import glob
from palettes import PALETTES

def read_gameboy_bmp(filepath):
    """
    Read Game Boy Camera BMP file and extract raw pixel data
    Returns numpy array with pixel values
    """
    try:
        # Open BMP file with PIL
        with Image.open(filepath) as img:
            # Convert to grayscale if not already
            if img.mode != 'L':
                img = img.convert('L')

            # Convert to numpy array
            pixel_data = np.array(img)

            # Game Boy Camera uses 4 distinct levels
            # Find unique values and map to 4 levels
            unique_vals = np.unique(pixel_data)
            print(f"  Found {len(unique_vals)} unique pixel values: {unique_vals}")

            # Map to 4 levels (0, 1, 2, 3)
            if len(unique_vals) <= 4:
                # If already 4 or fewer levels, use direct mapping
                level_map = {}
                for i, val in enumerate(sorted(unique_vals)):
                    level_map[val] = i
            else:
                # Quantize to 4 levels
                level_map = {}
                for val in unique_vals:
                    level = int((val / 255.0) * 3)  # Map to 0-3
                    level_map[val] = level

            # Apply mapping
            result = np.zeros_like(pixel_data, dtype=np.uint8)
            for old_val, new_level in level_map.items():
                result[pixel_data == old_val] = new_level

            return result

    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return None

def apply_palette(pixel_data, palette_colors):
    """
    Apply a 4-color palette to the pixel data
    pixel_data: numpy array with values 0-3
    palette_colors: list of 4 RGB tuples
    """
    height, width = pixel_data.shape
    result = np.zeros((height, width, 3), dtype=np.uint8)

    for level in range(4):
        if level < len(palette_colors):
            mask = pixel_data == level
            result[mask] = palette_colors[level]

    return result

def upscale_pixelart(image_array, scale_factor=4):
    """
    Upscale image using nearest neighbor to preserve pixel art look
    """
    height, width = image_array.shape[:2]
    new_height = height * scale_factor
    new_width = width * scale_factor

    if len(image_array.shape) == 3:
        # Color image
        result = np.zeros((new_height, new_width, 3), dtype=np.uint8)
        for y in range(height):
            for x in range(width):
                pixel = image_array[y, x]
                result[y*scale_factor:(y+1)*scale_factor,
                       x*scale_factor:(x+1)*scale_factor] = pixel
    else:
        # Grayscale image
        result = np.zeros((new_height, new_width), dtype=np.uint8)
        for y in range(height):
            for x in range(width):
                pixel = image_array[y, x]
                result[y*scale_factor:(y+1)*scale_factor,
                       x*scale_factor:(x+1)*scale_factor] = pixel

    return result

def convert_gameboy_images():
    """
    Convert all BMP files from _inbox folder to PNG with Game Boy palettes
    """
    # Check if _inbox folder exists
    inbox_dir = "_inbox"
    if not os.path.exists(inbox_dir):
        print("No _inbox folder found. Please create _inbox/ and add BMP files to process.")
        return None

    # Create output directory with date inside _processed folder
    current_date = datetime.now().strftime("%Y-%m-%d")
    base_output_dir = f"_processed/{current_date}"

    # Find all BMP files in _inbox
    bmp_files = glob.glob(f"{inbox_dir}/*.bmp")
    if not bmp_files:
        print("No BMP files found in _inbox/ folder")
        return base_output_dir

    print(f"Found {len(bmp_files)} BMP files to convert...")
    print(f"Output directory: {base_output_dir}")
    print(f"Palettes: {len(PALETTES)}")
    print()

    # Create palette directories and _original directory
    for palette_name in PALETTES.keys():
        os.makedirs(f"{base_output_dir}/{palette_name}", exist_ok=True)
    os.makedirs(f"{base_output_dir}/_original", exist_ok=True)

    processed_count = 0

    for bmp_file in sorted(bmp_files):
        print(f"Converting: {os.path.basename(bmp_file)}")

        # Read and extract pixel data
        pixel_data = read_gameboy_bmp(bmp_file)
        if pixel_data is None:
            continue

        # Get filename without extension and path
        filename = os.path.splitext(os.path.basename(bmp_file))[0]

        # Process with each palette
        for palette_name, palette_colors in PALETTES.items():
            # Apply palette
            colored_image = apply_palette(pixel_data, palette_colors)

            # Upscale 400%
            upscaled_image = upscale_pixelart(colored_image, 4)

            # Save as PNG
            output_path = f"{base_output_dir}/{palette_name}/{filename}.png"
            Image.fromarray(upscaled_image).save(output_path)

            print(f"  ✓ {palette_name}")

        # Move original BMP file to _original folder
        original_dest = f"{base_output_dir}/_original/{os.path.basename(bmp_file)}"
        shutil.move(bmp_file, original_dest)
        print(f"  📁 Moved to: {original_dest}")

        processed_count += 1
        print(f"  Completed ({processed_count}/{len(bmp_files)})")
        print()

    print("🎮 Game Boy Camera conversion complete!")
    print(f"📁 Results saved to: {base_output_dir}/")
    print(f"🎨 Palettes processed: {len(PALETTES)}")
    print(f"📸 Images converted: {processed_count}")
    print(f"📦 Original files moved to: {base_output_dir}/_original/")

    return base_output_dir

if __name__ == "__main__":
    convert_gameboy_images()