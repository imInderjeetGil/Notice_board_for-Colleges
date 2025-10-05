#!/usr/bin/env python3
"""
GitHub Setup Script for College Digital Notice Board
"""

import os
import subprocess
import sys

def run_command(command):
    """Run a command and return the result"""
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {command}")
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"❌ {command}")
        print(f"Error: {e.stderr}")
        return None

def main():
    print("🐙 GitHub Setup for College Digital Notice Board")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not os.path.exists('manage.py'):
        print("❌ Error: manage.py not found. Please run this script from the project root.")
        sys.exit(1)
    
    print("📋 Setting up GitHub repository...")
    
    # Initialize git repository
    print("\n1. Initializing Git repository...")
    if not os.path.exists('.git'):
        run_command("git init")
    else:
        print("✅ Git repository already initialized")
    
    # Add all files
    print("\n2. Adding files to Git...")
    run_command("git add .")
    
    # Create initial commit
    print("\n3. Creating initial commit...")
    run_command('git commit -m "Initial commit: College Digital Notice Board"')
    
    print("\n✅ GitHub setup complete!")
    print("\n📋 Next steps:")
    print("1. Create a new repository on GitHub")
    print("2. Add remote origin: git remote add origin https://github.com/yourusername/notice-board-project.git")
    print("3. Push to GitHub: git push -u origin main")
    print("4. Deploy to Railway/Render using GitHub integration")
    
    print("\n🌐 GitHub Repository Setup:")
    print("1. Go to https://github.com/new")
    print("2. Repository name: notice-board-project")
    print("3. Description: College Digital Notice Board with Push Notifications")
    print("4. Make it public (for free hosting)")
    print("5. Don't initialize with README (we already have one)")
    print("6. Create repository")
    
    print("\n🚀 Deployment Options:")
    print("- Railway: https://railway.app (Connect GitHub repo)")
    print("- Render: https://render.com (Connect GitHub repo)")
    print("- Heroku: https://heroku.com (Connect GitHub repo)")

if __name__ == "__main__":
    main()
