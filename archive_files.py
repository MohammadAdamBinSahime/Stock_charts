#!/usr/bin/env python3
"""
Archive script to move CSV and PNG files to their respective archive directories.
This script cleans up the workspace by moving generated files to archive folders.
"""

import os
import glob
import shutil
from datetime import datetime

def archive_files():
    """Move CSV and PNG files to their respective archive directories"""
    print("ARCHIVING FILES")
    print("=" * 50)
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Create archive directories if they don't exist
    csv_archive_dir = "stock_data/archive"
    png_archive_dir = "stock_png/archive"
    chartify_png_archive_dir = "chartify/stock_png/archive"
    
    os.makedirs(csv_archive_dir, exist_ok=True)
    os.makedirs(png_archive_dir, exist_ok=True)
    os.makedirs(chartify_png_archive_dir, exist_ok=True)
    
    # Archive CSV files from stock_data directory
    csv_files = [f for f in glob.glob("stock_data/*.csv") if not f.startswith("stock_data/archive")]
    csv_count = 0
    
    print(f"\nArchiving CSV files from stock_data/...")
    for csv_file in csv_files:
        try:
            csv_archive_path = os.path.join(csv_archive_dir, os.path.basename(csv_file))
            shutil.move(csv_file, csv_archive_path)
            print(f"  Moved: {os.path.basename(csv_file)}")
            csv_count += 1
        except Exception as e:
            print(f"  Error moving {csv_file}: {e}")
    
    # Archive PNG files from stock_png directory
    png_files = [f for f in glob.glob("stock_png/*.png") if not f.startswith("stock_png/archive")]
    png_count = 0
    
    print(f"\nArchiving PNG files from stock_png/...")
    for png_file in png_files:
        try:
            png_archive_path = os.path.join(png_archive_dir, os.path.basename(png_file))
            shutil.move(png_file, png_archive_path)
            print(f"  Moved: {os.path.basename(png_file)}")
            png_count += 1
        except Exception as e:
            print(f"  Error moving {png_file}: {e}")
    
    # Archive PNG files from chartify/stock_png directory
    chartify_png_files = [f for f in glob.glob("chartify/stock_png/*.png") if not f.startswith("chartify/stock_png/archive")]
    chartify_png_count = 0
    
    print(f"\nArchiving PNG files from chartify/stock_png/...")
    for png_file in chartify_png_files:
        try:
            png_archive_path = os.path.join(chartify_png_archive_dir, os.path.basename(png_file))
            shutil.move(png_file, png_archive_path)
            print(f"  Moved: {os.path.basename(png_file)}")
            chartify_png_count += 1
        except Exception as e:
            print(f"  Error moving {png_file}: {e}")
    
    # Archive HTML files
    html_files = glob.glob("*.html") + glob.glob("chartify/*.html")
    html_count = 0
    
    if html_files:
        html_archive_dir = "archive/html"
        os.makedirs(html_archive_dir, exist_ok=True)
        
        print(f"\nArchiving HTML files...")
        for html_file in html_files:
            try:
                html_archive_path = os.path.join(html_archive_dir, os.path.basename(html_file))
                shutil.move(html_file, html_archive_path)
                print(f"  Moved: {os.path.basename(html_file)}")
                html_count += 1
            except Exception as e:
                print(f"  Error moving {html_file}: {e}")
    
    # Summary
    print(f"\n" + "=" * 50)
    print("ARCHIVE SUMMARY")
    print(f"=" * 50)
    print(f"CSV files archived: {csv_count}")
    print(f"PNG files archived (root): {png_count}")
    print(f"PNG files archived (chartify): {chartify_png_count}")
    print(f"HTML files archived: {html_count}")
    print(f"Total files archived: {csv_count + png_count + chartify_png_count + html_count}")
    print(f"Archive completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    if csv_count + png_count + chartify_png_count + html_count == 0:
        print("No files to archive - workspace is already clean.")
    else:
        print("Workspace cleaned successfully!")

def main():
    """Main function"""
    archive_files()

if __name__ == "__main__":
    main()