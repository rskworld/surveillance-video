# Project: Surveillance Video Dataset
# Author: Molla Samser
# Website: https://rskworld.in/
# Contact: help@rskworld.in
# Phone: +91 93305 39277
# Address: Nutanhat, Mongolkote, Purba Burdwan, West Bengal, India, 713147

"""
Script to create ZIP file of the surveillance video dataset project.
"""

import os
import zipfile
from pathlib import Path
from datetime import datetime


def create_project_zip(output_filename='surveillance-video.zip', exclude_patterns=None):
    """
    Create a ZIP file of the project.
    
    Args:
        output_filename: Name of the output ZIP file
        exclude_patterns: List of patterns to exclude
    """
    if exclude_patterns is None:
        exclude_patterns = [
            '__pycache__',
            '*.pyc',
            '.git',
            '*.zip',
            'node_modules',
            '.DS_Store',
            'Thumbs.db',
            'output/*',
            'models/*.pt',
            'models/*.pth',
            'frames/extracted_frames/*'
        ]
    
    print(f"Creating ZIP file: {output_filename}")
    print("=" * 60)
    
    with zipfile.ZipFile(output_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # Get all files in current directory
        for root, dirs, files in os.walk('.'):
            # Skip certain directories
            dirs[:] = [d for d in dirs if d not in ['.git', '__pycache__', 'node_modules']]
            
            for file in files:
                file_path = os.path.join(root, file)
                
                # Skip if matches exclude patterns
                skip = False
                for pattern in exclude_patterns:
                    if pattern in file_path or file_path.endswith(pattern.replace('*', '')):
                        skip = True
                        break
                
                if skip:
                    continue
                
                # Skip the ZIP file itself
                if file_path == output_filename:
                    continue
                
                # Add file to ZIP
                arcname = os.path.relpath(file_path, '.')
                zipf.write(file_path, arcname)
                print(f"Added: {arcname}")
    
    file_size = os.path.getsize(output_filename) / (1024 * 1024)  # Size in MB
    print("=" * 60)
    print(f"ZIP file created successfully!")
    print(f"File: {output_filename}")
    print(f"Size: {file_size:.2f} MB")
    print(f"Created: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")


if __name__ == '__main__':
    create_project_zip()

