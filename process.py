#!/usr/bin/env python3
"""
Game Boy Camera Processor Orchestrator
Main script that coordinates conversion and contact sheet generation
"""

import sys
import argparse
from datetime import datetime
from palettes import PALETTES

def main():
    parser = argparse.ArgumentParser(
        description="Process Game Boy Camera BMP images with color palettes and create contact sheets"
    )
    parser.add_argument(
        "--convert-only",
        action="store_true",
        help="Only convert images, skip contact sheet generation"
    )
    parser.add_argument(
        "--contact-only",
        action="store_true",
        help="Only generate contact sheets, skip conversion"
    )
    parser.add_argument(
        "--quiet", "-q",
        action="store_true",
        help="Suppress output except errors"
    )

    args = parser.parse_args()

    if not args.quiet:
        print("🎮 Game Boy Camera Processor")
        print(f"📅 Date: {datetime.now().strftime('%Y-%m-%d')}")
        print(f"🎨 Palettes: {len(PALETTES)}")
        print(f"📥 Processing files from: _inbox/")
        print()

    base_dir = None

    # Step 1: Convert images (unless contact-only)
    if not args.contact_only:
        if not args.quiet:
            print("Step 1: Converting BMP images from _inbox/ to PNG with palettes...")

        try:
            from convert import convert_gameboy_images
            base_dir = convert_gameboy_images()

            if base_dir is None:
                print("❌ No _inbox folder or BMP files found")
                return 1

            if not args.quiet:
                print("✅ Conversion complete!")
                print()
        except Exception as e:
            print(f"❌ Error during conversion: {e}")
            return 1

    # Step 2: Generate contact sheets (unless convert-only)
    if not args.convert_only:
        if not args.quiet:
            print("Step 2: Generating contact sheets...")

        try:
            import importlib.util
            spec = importlib.util.spec_from_file_location("sheet", "sheet.py")
            contact_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(contact_module)
            created_count = contact_module.create_all_contact_sheets(base_dir)

            if not args.quiet:
                print("✅ Contact sheet generation complete!")
                print()
        except Exception as e:
            print(f"❌ Error during contact sheet generation: {e}")
            return 1

    if not args.quiet:
        print("🎉 All processing complete!")
        if base_dir:
            print(f"📁 Check results in: {base_dir}/")

    return 0

if __name__ == "__main__":
    sys.exit(main())