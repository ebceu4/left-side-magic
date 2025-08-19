#!/usr/bin/env python3
"""
Fix page numbering by removing blank page_001.png and renaming all subsequent pages.

This script:
1. Removes the blank page_001.png
2. Renames all pages to be sequential (cover, 001, 002, etc.)
3. Updates the total page count
"""

import os
import shutil
import sys

def main():
    """Fix the page numbering."""
    print("🔄 Starting page numbering fix...")
    
    pages_dir = "individual_pages"
    if not os.path.exists(pages_dir):
        print(f"❌ Directory {pages_dir} not found!")
        sys.exit(1)
    
    # List all current pages
    current_pages = sorted([f for f in os.listdir(pages_dir) if f.endswith('.png')])
    print(f"📋 Current pages: {len(current_pages)}")
    for page in current_pages[:5]:  # Show first 5
        file_path = os.path.join(pages_dir, page)
        file_size = os.path.getsize(file_path) / (1024 * 1024)  # MB
        print(f"  • {page} ({file_size:.1f} MB)")
    if len(current_pages) > 5:
        print(f"  ... and {len(current_pages) - 5} more pages")
    
    # Check if page_001.png exists and is small/blank
    page_001_path = os.path.join(pages_dir, "page_001.png")
    if os.path.exists(page_001_path):
        file_size = os.path.getsize(page_001_path) / (1024 * 1024)  # MB
        print(f"\n🔍 Found page_001.png: {file_size:.1f} MB")
        
        if file_size < 0.1:  # Less than 0.1 MB, likely blank
            print("🗑️ Removing blank page_001.png...")
            os.remove(page_001_path)
            print("✅ Removed blank page")
        else:
            print("⚠️ page_001.png is not blank, keeping it")
            return
    else:
        print("ℹ️ page_001.png not found, nothing to remove")
        return
    
    # Create temporary directory for renaming
    temp_dir = "temp_pages"
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
    os.makedirs(temp_dir)
    
    print(f"\n🔄 Renaming pages to fix numbering...")
    
    # Copy cover page as-is
    cover_src = os.path.join(pages_dir, "page_000_cover.png")
    cover_dst = os.path.join(temp_dir, "page_000_cover.png")
    if os.path.exists(cover_src):
        shutil.copy2(cover_src, cover_dst)
        print(f"✅ Kept cover: page_000_cover.png")
    
    # Rename all pages starting from page_002.png -> page_001.png
    page_counter = 1
    for i in range(2, 50):  # Check up to page_049
        old_page = f"page_{i:03d}.png"
        old_path = os.path.join(pages_dir, old_page)
        
        if os.path.exists(old_path):
            new_page = f"page_{page_counter:03d}.png"
            new_path = os.path.join(temp_dir, new_page)
            
            shutil.copy2(old_path, new_path)
            print(f"✅ Renamed: {old_page} -> {new_page}")
            page_counter += 1
        else:
            break  # No more pages
    
    # Replace original directory with fixed pages
    print(f"\n🔄 Replacing original pages...")
    shutil.rmtree(pages_dir)
    shutil.move(temp_dir, pages_dir)
    
    # List final pages
    final_pages = sorted([f for f in os.listdir(pages_dir) if f.endswith('.png')])
    print(f"\n✅ Final pages: {len(final_pages)}")
    for page in final_pages:
        file_path = os.path.join(pages_dir, page)
        file_size = os.path.getsize(file_path) / (1024 * 1024)  # MB
        print(f"  • {page} ({file_size:.1f} MB)")
    
    print(f"\n🎉 Page numbering fixed!")
    print(f"📊 Total pages now: {len(final_pages)}")
    print(f"📖 Structure: 1 cover + {len(final_pages) - 1} content pages")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n🛑 Process interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")
        sys.exit(1)
