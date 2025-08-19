#!/usr/bin/env python3
"""
Split book spread images into individual left and right pages for Turn.js

This script takes the extracted PDF spread images and splits them down the middle
to create individual page images that Turn.js can use properly.
"""

from PIL import Image
import os
import sys

def split_spread_image(input_path, output_dir, page_number):
    """
    Split a spread image into left and right pages.
    
    Args:
        input_path: Path to the spread image
        output_dir: Directory to save split pages
        page_number: The spread number (1-based)
    
    Returns:
        Tuple of (left_page_path, right_page_path)
    """
    try:
        # Open the spread image
        with Image.open(input_path) as img:
            width, height = img.size
            
            print(f"📖 Processing spread {page_number}: {width}x{height}")
            
            # Calculate split point (middle of image)
            split_x = width // 2
            
            # Split into left and right halves
            left_half = img.crop((0, 0, split_x, height))
            right_half = img.crop((split_x, 0, width, height))
            
            # Generate output filenames
            if page_number == 1:
                # First spread: cover (right) and first content page (left)
                left_path = os.path.join(output_dir, "page_000_cover.png")  # Cover
                right_path = os.path.join(output_dir, "page_001.png")      # Page 1
                
                # For cover, we want the right half (actual cover)
                # For page 1, we want the left half (first content page)
                right_half.save(left_path, 'PNG', optimize=True)
                left_half.save(right_path, 'PNG', optimize=True)
                
                print(f"  ✅ Cover saved: {left_path}")
                print(f"  ✅ Page 1 saved: {right_path}")
                
                return left_path, right_path
            else:
                # Regular spreads: calculate page numbers
                left_page_num = (page_number - 1) * 2
                right_page_num = left_page_num + 1
                
                left_path = os.path.join(output_dir, f"page_{left_page_num:03d}.png")
                right_path = os.path.join(output_dir, f"page_{right_page_num:03d}.png")
                
                # Save left and right pages
                left_half.save(left_path, 'PNG', optimize=True)
                right_half.save(right_path, 'PNG', optimize=True)
                
                print(f"  ✅ Page {left_page_num} saved: {left_path}")
                print(f"  ✅ Page {right_page_num} saved: {right_path}")
                
                return left_path, right_path
                
    except Exception as e:
        print(f"❌ Error processing spread {page_number}: {e}")
        raise

def main():
    """Main function to split all spread images."""
    print("🔄 Starting page splitting process...")
    
    # Create output directory for individual pages
    output_dir = "individual_pages"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"📁 Created output directory: {output_dir}")
    
    # Process all spread images
    total_spreads = 11
    total_pages_created = 0
    
    for i in range(1, total_spreads + 1):
        input_path = f"book_images/page_{i:03d}_img_001.png"
        
        if not os.path.exists(input_path):
            print(f"⚠️ Warning: Spread image not found: {input_path}")
            continue
            
        try:
            left_path, right_path = split_spread_image(input_path, output_dir, i)
            total_pages_created += 2
            
        except Exception as e:
            print(f"❌ Failed to process spread {i}: {e}")
            continue
    
    print("\n" + "="*50)
    print(f"🎉 Page splitting completed!")
    print(f"📊 Total spreads processed: {total_spreads}")
    print(f"📄 Total individual pages created: {total_pages_created}")
    print(f"📁 Pages saved in: {output_dir}/")
    print("="*50)
    
    # List all created pages
    if os.path.exists(output_dir):
        pages = sorted([f for f in os.listdir(output_dir) if f.endswith('.png')])
        print(f"\n📋 Created pages:")
        for page in pages:
            file_path = os.path.join(output_dir, page)
            file_size = os.path.getsize(file_path) / (1024 * 1024)  # MB
            print(f"  • {page} ({file_size:.1f} MB)")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n🛑 Process interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")
        sys.exit(1)
