#!/usr/bin/env python3
"""
Image compression script for web optimization.
Compresses PNG images to reduce file size while maintaining good quality for web display.

Usage:
    python compress_images.py
"""

import os
import sys
from pathlib import Path
from PIL import Image, ImageOps
import shutil

def compress_image(input_path, output_path, max_width=1200, quality=85, optimize=True):
    """
    Compress an image for web use.
    
    Args:
        input_path: Path to input image
        output_path: Path to save compressed image
        max_width: Maximum width in pixels (height will be scaled proportionally)
        quality: JPEG quality (85 is good balance of quality/size)
        optimize: Whether to optimize the image
    """
    try:
        print(f"📸 Compressing: {input_path.name}")
        
        # Open and process image
        with Image.open(input_path) as img:
            # Get original size
            original_width, original_height = img.size
            original_size = input_path.stat().st_size
            
            print(f"   Original: {original_width}x{original_height} ({original_size / 1024 / 1024:.1f} MB)")
            
            # Convert to RGB if necessary (for JPEG output)
            if img.mode in ('RGBA', 'LA', 'P'):
                # Create white background for transparency
                background = Image.new('RGB', img.size, (255, 255, 255))
                if img.mode == 'P':
                    img = img.convert('RGBA')
                background.paste(img, mask=img.split()[-1] if img.mode in ('RGBA', 'LA') else None)
                img = background
            elif img.mode != 'RGB':
                img = img.convert('RGB')
            
            # Resize if image is too wide
            if original_width > max_width:
                # Calculate new height maintaining aspect ratio
                new_height = int((max_width * original_height) / original_width)
                img = img.resize((max_width, new_height), Image.Resampling.LANCZOS)
                print(f"   Resized to: {max_width}x{new_height}")
            
            # Auto-orient image
            img = ImageOps.exif_transpose(img)
            
            # Save as optimized JPEG
            img.save(
                output_path,
                'JPEG',
                quality=quality,
                optimize=optimize,
                progressive=True  # Progressive JPEG for better web loading
            )
            
            # Get compressed size
            compressed_size = output_path.stat().st_size
            compression_ratio = (1 - compressed_size / original_size) * 100
            
            print(f"   Compressed: {img.size[0]}x{img.size[1]} ({compressed_size / 1024 / 1024:.1f} MB)")
            print(f"   Saved: {compression_ratio:.1f}% smaller")
            
            return True
            
    except Exception as e:
        print(f"❌ Error compressing {input_path.name}: {e}")
        return False

def main():
    """Main compression function."""
    print("🗜️  Image Compression Tool")
    print("=" * 50)
    
    # Paths
    input_dir = Path("individual_pages")
    output_dir = Path("individual_pages_compressed")
    
    # Check if input directory exists
    if not input_dir.exists():
        print(f"❌ Input directory '{input_dir}' not found!")
        sys.exit(1)
    
    # Create output directory
    output_dir.mkdir(exist_ok=True)
    print(f"📁 Input: {input_dir}")
    print(f"📁 Output: {output_dir}")
    print()
    
    # Get all PNG files
    png_files = list(input_dir.glob("*.png"))
    
    if not png_files:
        print("❌ No PNG files found in input directory!")
        sys.exit(1)
    
    print(f"📊 Found {len(png_files)} images to compress")
    print()
    
    # Compression settings
    MAX_WIDTH = 1200  # Good for web display, smaller than original
    QUALITY = 85      # Good balance of quality and file size
    
    print(f"⚙️  Settings: Max width = {MAX_WIDTH}px, Quality = {QUALITY}")
    print()
    
    # Process each image
    successful = 0
    failed = 0
    total_original_size = 0
    total_compressed_size = 0
    
    for png_file in sorted(png_files):
        # Create output filename (change extension to .jpg)
        output_file = output_dir / (png_file.stem + ".jpg")
        
        # Track sizes
        original_size = png_file.stat().st_size
        total_original_size += original_size
        
        # Compress
        if compress_image(png_file, output_file, MAX_WIDTH, QUALITY):
            successful += 1
            total_compressed_size += output_file.stat().st_size
        else:
            failed += 1
        
        print()
    
    # Summary
    print("=" * 50)
    print("📊 COMPRESSION SUMMARY")
    print(f"✅ Successful: {successful}")
    print(f"❌ Failed: {failed}")
    print(f"📦 Original total size: {total_original_size / 1024 / 1024:.1f} MB")
    print(f"📦 Compressed total size: {total_compressed_size / 1024 / 1024:.1f} MB")
    
    if total_original_size > 0:
        overall_reduction = (1 - total_compressed_size / total_original_size) * 100
        print(f"💾 Overall size reduction: {overall_reduction:.1f}%")
    
    print()
    print("🎉 Compression complete!")
    print(f"📁 Compressed images saved to: {output_dir}")
    
    # Ask if user wants to replace original files
    print()
    replace = input("🔄 Replace original images with compressed versions? (y/N): ").lower().strip()
    
    if replace in ('y', 'yes'):
        print("🔄 Replacing original images...")
        
        # Backup original directory
        backup_dir = Path("individual_pages_backup")
        if backup_dir.exists():
            shutil.rmtree(backup_dir)
        shutil.copytree(input_dir, backup_dir)
        print(f"💾 Original images backed up to: {backup_dir}")
        
        # Replace files
        for jpg_file in output_dir.glob("*.jpg"):
            # Convert back to PNG filename for consistency
            png_name = jpg_file.stem + ".png"
            target_path = input_dir / png_name
            
            # Remove original PNG
            if target_path.exists():
                target_path.unlink()
            
            # Copy compressed JPG as PNG (just rename extension)
            shutil.copy2(jpg_file, target_path.with_suffix('.jpg'))
            
        print("✅ Original images replaced with compressed versions!")
        print("⚠️  Note: Images are now JPEG format but may have .png extension")
        print("   This is fine for web browsers, they detect format by content.")
    else:
        print("👍 Original images kept unchanged.")
        print(f"   Use compressed images from: {output_dir}")

if __name__ == "__main__":
    main()
