#!/usr/bin/env python3
"""
Script to commit and push all changes to GitHub with timestamp
"""

import subprocess
import sys
from datetime import datetime

def run_command(command, description):
    """Run a shell command and handle errors"""
    print(f"\n{description}...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, check=True)
        if result.stdout:
            print(result.stdout.strip())
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        if e.stderr:
            print(f"Error details: {e.stderr.strip()}")
        return False

def main():
    """Main function to commit and push to GitHub"""
    
    # Repository URL
    repo_url = "https://github.com/MohammadAdamBinSahime/Stock_charts.git"
    
    # Get current timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    commit_message = f"Updated repository - {timestamp}"
    
    print(f"Starting Git operations with commit message: '{commit_message}'")
    
    # Check if we're in a git repository
    if not run_command("git status", "Checking git status"):
        print("Error: Not in a git repository or git is not available")
        sys.exit(1)
    
    # Ensure we're on main branch
    print("\nEnsuring we're on main branch...")
    run_command("git checkout main", "Switching to main branch (if exists)")
    if not run_command("git branch -M main", "Renaming current branch to main"):
        print("Warning: Could not rename branch to main")
    
    # Set remote origin if not already set or update it
    print("\nSetting up remote repository...")
    run_command(f"git remote remove origin", "Removing existing origin (if any)")
    if not run_command(f"git remote add origin {repo_url}", "Adding remote origin"):
        print("Error: Failed to set remote origin")
        sys.exit(1)
    
    # Add all changes
    if not run_command("git add .", "Adding all changes"):
        print("Error: Failed to add changes")
        sys.exit(1)
    
    # Check if there are changes to commit
    result = subprocess.run("git diff --cached --quiet", shell=True)
    if result.returncode == 0:
        print("No changes to commit")
        return
    
    # Commit changes
    if not run_command(f'git commit -m "{commit_message}"', "Committing changes"):
        print("Error: Failed to commit changes")
        sys.exit(1)
    
    # Push to GitHub
    if not run_command("git push -u origin main", "Pushing to GitHub"):
        print("Error: Failed to push to GitHub")
        print("Note: Make sure you have push permissions and are authenticated")
        sys.exit(1)
    
    print(f"\n✅ Successfully committed and pushed all changes!")
    print(f"Commit message: '{commit_message}'")

if __name__ == "__main__":
    main()