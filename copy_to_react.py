#!/usr/bin/env python3
"""
Script to copy stock charts HTML file and images to React app's public folder
"""

import os
import shutil
from pathlib import Path

def copy_files_to_react():
    # Define source and destination paths
    base_dir = Path(__file__).parent
    html_source = base_dir / "stock_charts_collage.html"
    images_source = base_dir / "stock_png"
    react_public_dir = base_dir / "stock-app" / "public"
    
    # Check if source files exist
    if not html_source.exists():
        print(f"Error: HTML file not found at {html_source}")
        return False
    
    if not images_source.exists():
        print(f"Error: Images folder not found at {images_source}")
        return False
    
    if not react_public_dir.exists():
        print(f"Error: React public folder not found at {react_public_dir}")
        return False
    
    try:
        # Copy HTML file
        html_dest = react_public_dir / "stock_charts_collage.html"
        shutil.copy2(html_source, html_dest)
        print(f"[OK] Copied HTML file to {html_dest}")
        
        # Copy images folder
        images_dest = react_public_dir / "stock_png"
        
        # Remove existing folder if it exists
        if images_dest.exists():
            shutil.rmtree(images_dest)
            print(f"[OK] Removed existing {images_dest}")
        
        # Copy the entire folder
        shutil.copytree(images_source, images_dest)
        print(f"[OK] Copied images folder to {images_dest}")
        
        # Count copied files
        image_count = len(list(images_dest.glob("*.png")))
        print(f"[OK] Copied {image_count} PNG files")
        
        print("\nSuccess! Files copied to React app.")
        print("You can now run 'npm start' in the stock-app directory.")
        
        return True
        
    except Exception as e:
        print(f"Error copying files: {e}")
        return False

if __name__ == "__main__":
    print("Copying stock charts files to React app...")
    copy_files_to_react()