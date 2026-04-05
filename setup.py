"""
Jarvis Voice Assistant - Setup Script
Run this first to create the project structure and install dependencies.

Usage:
    python setup.py          # Interactive setup
    python setup.py --all    # Full setup with dependencies
    python setup.py --dirs   # Create directories only
"""

import os
import subprocess
import sys

def create_directories():
    """Create the project directory structure."""
    base_path = os.path.dirname(os.path.abspath(__file__))
    
    directories = [
        os.path.join(base_path, "jarvis"),
        os.path.join(base_path, "jarvis", "actions"),
        os.path.join(base_path, "jarvis", "utils"),
        os.path.join(base_path, "jarvis", "logs"),
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✓ Created: {directory}")

def install_dependencies():
    """Install required Python packages."""
    packages = [
        "SpeechRecognition",
        "pyttsx3",
        "selenium",
        "webdriver-manager",
        "pyautogui",
        "pyaudio",
    ]
    
    print("\n📦 Installing dependencies...")
    for package in packages:
        print(f"  Installing {package}...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package, "-q"])
        except subprocess.CalledProcessError:
            print(f"    ⚠ Failed to install {package}, try manually: pip install {package}")
    
    print("✓ Dependencies installation complete!")

def main():
    print("=" * 50)
    print("  JARVIS VOICE ASSISTANT - SETUP")
    print("=" * 50)
    
    # Check for command line args
    if len(sys.argv) > 1:
        if "--all" in sys.argv:
            print("\n📁 Creating directory structure...")
            create_directories()
            install_dependencies()
        elif "--dirs" in sys.argv:
            print("\n📁 Creating directory structure...")
            create_directories()
        else:
            print("Usage: python setup.py [--all | --dirs]")
            return
    else:
        print("\n📁 Creating directory structure...")
        create_directories()
        
        response = input("\n❓ Install Python dependencies? (y/n): ").strip().lower()
        if response == 'y':
            install_dependencies()
    
    print("\n" + "=" * 50)
    print("✅ Setup complete!")
    print("\nNext steps:")
    print("  1. cd jarvis")
    print("  2. python main.py")
    print("=" * 50)

if __name__ == "__main__":
    main()
