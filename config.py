# Project: Surveillance Video Dataset
# Author: Molla Samser
# Website: https://rskworld.in/
# Contact: help@rskworld.in
# Phone: +91 93305 39277
# Address: Nutanhat, Mongolkote, Purba Burdwan, West Bengal, India, 713147

"""
Configuration file for Surveillance Video Dataset project.
"""

# Project Information
PROJECT_NAME = "Surveillance Video Dataset"
AUTHOR = "Molla Samser"
WEBSITE = "https://rskworld.in/"
CONTACT_EMAIL = "help@rskworld.in"
PHONE = "+91 93305 39277"
ADDRESS = "Nutanhat, Mongolkote, Purba Burdwan, West Bengal, India, 713147"

# Directory Paths
VIDEOS_DIR = "videos"
ANNOTATIONS_DIR = "annotations"
FRAMES_DIR = "frames/extracted_frames"
OUTPUT_DIR = "output"

# Video Processing Settings
DEFAULT_FPS = 30.0
FRAME_EXTRACTION_INTERVAL = 30  # Extract every Nth frame
VIDEO_FORMATS = ['.mp4', '.avi', '.mov', '.mkv']

# Detection Settings
YOLO_MODEL = "yolov8n.pt"  # YOLO model path
PERSON_CLASS_ID = 0  # Person class ID in COCO dataset
CONFIDENCE_THRESHOLD = 0.5

# Anomaly Detection Settings
MOTION_THRESHOLD = 5000
ANOMALY_WINDOW_SIZE = 2.0  # seconds
ANOMALY_STD_MULTIPLIER = 2.0

# Output Settings
SAVE_ANNOTATIONS = True
SAVE_DETECTIONS = True
SAVE_ANOMALIES = True
VISUALIZE_RESULTS = True

