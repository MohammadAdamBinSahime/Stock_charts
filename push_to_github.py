#!/usr/bin/env python3
"""
Git Push Automation Script
Automates the process of adding, committing, and pushing changes to GitHub
"""

import subprocess
import sys
from datetime import datetime

def run_command(command, description=""):
    """Run a shell command and return the result"""
    try:
        print(f"Running: {description if description else command}")
        result = subprocess.run(command, shell=True, capture_output=True, text=True, check=True)
        if result.stdout:
            print(result.stdout.strip())
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {command}")
        print(f"Error output: {e.stderr}")
        return False

def check_git_status():
    """Check if there are any changes to commit"""
    try:
        result = subprocess.run("git status --porcelain", shell=True, capture_output=True, text=True)
        return len(result.stdout.strip()) > 0
    except subprocess.CalledProcessError:
        return False

def main():
    """Main function to handle git push process"""
    print("=== Git Push Automation Script ===")
    
    # Check if there are changes to commit
    if not check_git_status():
        print("No changes to commit. Repository is up to date.")
        return
    
    # Show current status
    if not run_command("git status", "Checking git status"):
        print("Failed to check git status")
        sys.exit(1)
    
    # Add all changes
    if not run_command("git add .", "Adding all changes"):
        print("Failed to add changes")
        sys.exit(1)
    
    # Get commit message from user or use default
    commit_message = input("\nEnter commit message (or press Enter for default): ").strip()
    if not commit_message:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        commit_message = f"Updated repository - {timestamp}"
    
    # Commit changes
    commit_command = f'git commit -m "{commit_message}"'
    if not run_command(commit_command, "Committing changes"):
        print("Failed to commit changes")
        sys.exit(1)
    
    # Push to GitHub
    if not run_command("git push origin main", "Pushing to GitHub"):
        print("Failed to push to GitHub")
        sys.exit(1)
    
    print("\n✅ Successfully pushed changes to GitHub!")
    
    # Show recent commits
    run_command("git log --oneline -5", "Recent commits")

if __name__ == "__main__":
    main()