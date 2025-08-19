#!/usr/bin/env python3
"""
PDF Image Extraction Script

This script extracts all images from a PDF file and saves them to a designated folder.
It uses PyMuPDF (fitz) library for efficient PDF processing.
"""

import fitz  # PyMuPDF
import os
import sys
from pathlib import Path
from typing import List, Tuple


def create_output_directory(pdf_path: str) -> str:
    """Create output directory for extracted images."""
    pdf_name = Path(pdf_path).stem
    output_dir = f"{pdf_name}_images"
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created directory: {output_dir}")
    else:
        print(f"Using existing directory: {output_dir}")
    
    return output_dir


def extract_images_from_pdf(pdf_path: str) -> Tuple[int, List[str]]:
    """
    Extract all images from a PDF file.
    
    Args:
        pdf_path: Path to the PDF file
        
    Returns:
        Tuple of (total_images_extracted, list_of_saved_files)
    """
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")
    
    # Create output directory
    output_dir = create_output_directory(pdf_path)
    
    # Open PDF
    doc = fitz.open(pdf_path)
    total_images = 0
    saved_files = []
    
    print(f"Processing PDF: {pdf_path}")
    print(f"Total pages: {len(doc)}")
    print("-" * 50)
    
    # Iterate through each page
    for page_num in range(len(doc)):
        page = doc[page_num]
        
        # Get list of images on the page
        image_list = page.get_images()
        
        if image_list:
            print(f"Page {page_num + 1}: Found {len(image_list)} image(s)")
        
        # Extract each image
        for img_index, img in enumerate(image_list):
            # Get image data
            xref = img[0]  # xref number
            pix = fitz.Pixmap(doc, xref)
            
            # Skip if image is too small (likely decorative elements)
            if pix.width < 10 or pix.height < 10:
                print(f"  Skipping small image: {pix.width}x{pix.height}")
                pix = None
                continue
            
            # Determine image format and extension
            if pix.n - pix.alpha < 4:  # GRAY or RGB
                img_ext = "png"
            else:  # CMYK: convert to RGB first
                pix_rgb = fitz.Pixmap(fitz.csRGB, pix)
                pix = pix_rgb
                img_ext = "png"
            
            # Create filename
            img_filename = f"page_{page_num + 1:03d}_img_{img_index + 1:03d}.{img_ext}"
            img_path = os.path.join(output_dir, img_filename)
            
            # Save image
            pix.save(img_path)
            saved_files.append(img_path)
            total_images += 1
            
            print(f"  Saved: {img_filename} ({pix.width}x{pix.height})")
            
            # Clean up
            pix = None
    
    doc.close()
    
    print("-" * 50)
    print(f"Extraction complete!")
    print(f"Total images extracted: {total_images}")
    print(f"Images saved to: {output_dir}/")
    
    return total_images, saved_files


def main():
    """Main function to run the image extraction."""
    if len(sys.argv) != 2:
        print("Usage: python extract_images.py <pdf_file>")
        print("Example: python extract_images.py book.pdf")
        sys.exit(1)
    
    pdf_file = sys.argv[1]
    
    try:
        total_images, saved_files = extract_images_from_pdf(pdf_file)
        
        if total_images == 0:
            print("No images found in the PDF file.")
        else:
            print(f"\nSuccessfully extracted {total_images} images!")
            print(f"All images have been saved to the '{Path(pdf_file).stem}_images' directory.")
            
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
