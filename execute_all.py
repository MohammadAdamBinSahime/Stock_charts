#!/usr/bin/env python3
"""
Execute all scripts in sequence by calling them as separate processes.
"""

import subprocess
import sys
import os
from datetime import datetime

def run_script(script_path):
    """Execute a Python script as a separate process"""
    print(f"\n{'='*50}")
    print(f"Executing: {script_path}")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*50}")
    
    try:
        result = subprocess.run([sys.executable, script_path], check=True)
        print(f"SUCCESS: {script_path} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"ERROR: {script_path} failed with exit code {e.returncode}")
        return False
    except Exception as e:
        print(f"ERROR: Error running {script_path}: {e}")
        return False

def main():
    print("Executing all scripts in sequence...")
    print(f"Start time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    scripts = [
        "archive_files.py",
        "top_volume_stocks.py",
        "download_top_volume_history.py", 
        "chartify/csv_candlestick_app.py",
        "chartify/generate_html_collage.py",
	"copy_to_react.py"
    ]
    
    success_count = 0
    
    for script in scripts:
        if os.path.exists(script):
            if run_script(script):
                success_count += 1
        else:
            print(f"Script not found: {script}")
    
    print(f"\n{'='*50}")
    print(f"Completed: {success_count}/{len(scripts)} scripts successful")
    print(f"End time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main()
