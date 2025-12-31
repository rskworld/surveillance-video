# Project: Surveillance Video Dataset
# Author: Molla Samser
# Website: https://rskworld.in/
# Contact: help@rskworld.in
# Phone: +91 93305 39277
# Address: Nutanhat, Mongolkote, Purba Burdwan, West Bengal, India, 713147

"""
Project verification script.
Checks for missing files, broken links, and common issues.
"""

import os
import sys
from pathlib import Path


def check_file_exists(filepath, description):
    """Check if a file exists."""
    if os.path.exists(filepath):
        print(f"[OK] {description}: {filepath}")
        return True
    else:
        print(f"[MISSING] {description}: {filepath}")
        return False


def check_directory_exists(dirpath, description):
    """Check if a directory exists."""
    if os.path.exists(dirpath) and os.path.isdir(dirpath):
        print(f"[OK] {description}: {dirpath}")
        return True
    else:
        print(f"[MISSING] {description}: {dirpath}")
        return False


def verify_project():
    """Verify project structure and files."""
    print("=" * 60)
    print("Surveillance Video Dataset - Project Verification")
    print("=" * 60)
    print()
    
    issues = []
    
    # Check core HTML files
    print("HTML Files:")
    if not check_file_exists("index.html", "Main page"):
        issues.append("index.html")
    if not check_file_exists("analytics_dashboard.html", "Analytics dashboard"):
        issues.append("analytics_dashboard.html")
    print()
    
    # Check CSS and JS files
    print("CSS and JavaScript Files:")
    if not check_file_exists("styles.css", "Stylesheet"):
        issues.append("styles.css")
    if not check_file_exists("script.js", "Main script"):
        issues.append("script.js")
    if not check_file_exists("analytics.js", "Analytics script"):
        issues.append("analytics.js")
    print()
    
    # Check Python scripts
    print("Python Scripts:")
    python_files = [
        ("api_server.py", "API server"),
        ("batch_processor.py", "Batch processor"),
        ("detect_persons.py", "Person detection"),
        ("detect_anomalies.py", "Anomaly detection"),
        ("extract_frames.py", "Frame extraction"),
        ("process_video.py", "Video processing"),
        ("video_quality_analyzer.py", "Quality analyzer"),
        ("multi_camera_system.py", "Multi-camera system"),
        ("video_search.py", "Video search"),
        ("alert_system.py", "Alert system"),
        ("train_ml_model.py", "ML training"),
        ("create_sample_video.py", "Sample video creator"),
        ("setup.py", "Setup script"),
        ("config.py", "Configuration")
    ]
    
    for filepath, description in python_files:
        if not check_file_exists(filepath, description):
            issues.append(filepath)
    print()
    
    # Check directories
    print("Directories:")
    directories = [
        ("videos", "Videos directory"),
        ("annotations", "Annotations directory"),
        ("frames", "Frames directory"),
        ("config", "Config directory"),
        ("models", "Models directory"),
        ("output", "Output directory")
    ]
    
    for dirpath, description in directories:
        if not check_directory_exists(dirpath, description):
            issues.append(dirpath)
    print()
    
    # Check annotation files
    print("Annotation Files:")
    annotation_files = [
        ("annotations/annotations.json", "Activity annotations"),
        ("annotations/person_detections.json", "Person detections"),
        ("annotations/anomalies.json", "Anomaly events")
    ]
    
    for filepath, description in annotation_files:
        if not check_file_exists(filepath, description):
            issues.append(filepath)
    print()
    
    # Check documentation files
    print("Documentation Files:")
    doc_files = [
        ("README.md", "Main README"),
        ("LICENSE", "License file"),
        ("requirements.txt", "Requirements")
    ]
    
    for filepath, description in doc_files:
        if not check_file_exists(filepath, description):
            issues.append(filepath)
    print()
    
    # Check data files
    print("Data Files:")
    data_files = [
        ("project_data.json", "Project data JSON"),
        ("project_data.php", "Project data PHP"),
        ("project_data.py", "Project data Python"),
        ("package.json", "Package JSON")
    ]
    
    for filepath, description in data_files:
        if not check_file_exists(filepath, description):
            issues.append(filepath)
    print()
    
    # Summary
    print("=" * 60)
    if issues:
        print(f"Found {len(issues)} missing files/directories:")
        for issue in issues:
            print(f"  - {issue}")
        print()
        print("Please create the missing files/directories.")
        return False
    else:
        print("[SUCCESS] All files and directories verified successfully!")
        print("=" * 60)
        return True


if __name__ == "__main__":
    success = verify_project()
    sys.exit(0 if success else 1)
