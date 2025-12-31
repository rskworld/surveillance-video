# Project: Surveillance Video Dataset
# Author: Molla Samser
# Website: https://rskworld.in/
# Contact: help@rskworld.in
# Phone: +91 93305 39277
# Address: Nutanhat, Mongolkote, Purba Burdwan, West Bengal, India, 713147

"""
Setup script for Surveillance Video Dataset project.
Creates necessary directories and checks dependencies.
"""

import os
import sys
from pathlib import Path


def create_directories():
    """Create necessary directories for the project."""
    directories = [
        'videos',
        'annotations',
        'frames/extracted_frames',
        'output'
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"Created directory: {directory}")


def check_dependencies():
    """Check if required Python packages are installed."""
    required_packages = {
        'cv2': 'opencv-python',
        'numpy': 'numpy',
        'ultralytics': 'ultralytics'
    }
    
    missing_packages = []
    
    for module, package in required_packages.items():
        try:
            __import__(module)
            print(f"✓ {package} is installed")
        except ImportError:
            print(f"✗ {package} is NOT installed")
            missing_packages.append(package)
    
    if missing_packages:
        print("\nTo install missing packages, run:")
        print(f"pip install {' '.join(missing_packages)}")
        return False
    
    return True


def main():
    """Main setup function."""
    print("=" * 50)
    print("Surveillance Video Dataset - Setup")
    print("=" * 50)
    print("\nCreating directories...")
    create_directories()
    
    print("\nChecking dependencies...")
    deps_ok = check_dependencies()
    
    print("\n" + "=" * 50)
    if deps_ok:
        print("Setup complete! All dependencies are installed.")
    else:
        print("Setup complete! Please install missing dependencies.")
    print("=" * 50)


if __name__ == "__main__":
    main()

