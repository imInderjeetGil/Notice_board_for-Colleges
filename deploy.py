#!/usr/bin/env python3
"""
Deployment script for College Digital Notice Board
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
    print("🚀 College Digital Notice Board - Deployment Preparation")
    print("=" * 60)
    
    # Check if we're in the right directory
    if not os.path.exists('manage.py'):
        print("❌ Error: manage.py not found. Please run this script from the project root.")
        sys.exit(1)
    
    print("📋 Preparing for deployment...")
    
    # Install production dependencies
    print("\n1. Installing production dependencies...")
    run_command("pip install -r requirements.txt")
    
    # Collect static files
    print("\n2. Collecting static files...")
    run_command("python manage.py collectstatic --noinput")
    
    # Run migrations
    print("\n3. Running database migrations...")
    run_command("python manage.py migrate")
    
    # Create superuser (optional)
    print("\n4. Creating superuser...")
    print("You can create a superuser manually with: python manage.py createsuperuser")
    
    print("\n✅ Deployment preparation complete!")
    print("\n📋 Next steps:")
    print("1. Choose a deployment platform (Railway, Render, Heroku, etc.)")
    print("2. Set up environment variables")
    print("3. Configure database")
    print("4. Deploy!")
    
    print("\n🌐 Recommended platforms:")
    print("- Railway: https://railway.app (Easy, free tier)")
    print("- Render: https://render.com (Free tier available)")
    print("- Heroku: https://heroku.com (Paid, reliable)")

if __name__ == "__main__":
    main()
