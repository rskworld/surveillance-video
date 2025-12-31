# Project: Surveillance Video Dataset
# Author: Molla Samser
# Website: https://rskworld.in/
# Contact: help@rskworld.in
# Phone: +91 93305 39277
# Address: Nutanhat, Mongolkote, Purba Burdwan, West Bengal, India, 713147

"""
Video processing script for surveillance video dataset.
This script provides basic video processing and frame extraction capabilities.
"""

import cv2
import json
import os
from pathlib import Path


def process_video(video_path, output_dir='output'):
    """
    Process a surveillance video file.
    
    Args:
        video_path: Path to the input video file
        output_dir: Directory to save processed output
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Open video file
    cap = cv2.VideoCapture(video_path)
    
    if not cap.isOpened():
        print(f"Error: Could not open video file {video_path}")
        return
    
    # Get video properties
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = total_frames / fps
    
    print(f"Video Properties:")
    print(f"  Resolution: {width}x{height}")
    print(f"  FPS: {fps}")
    print(f"  Total Frames: {total_frames}")
    print(f"  Duration: {duration:.2f} seconds")
    
    frame_count = 0
    
    # Process each frame
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        # Convert to grayscale for analysis
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # You can add your processing logic here
        # For example: background subtraction, motion detection, etc.
        
        # Display frame (optional)
        cv2.imshow('Processing Video', frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
        frame_count += 1
    
    cap.release()
    cv2.destroyAllWindows()
    
    print(f"Processed {frame_count} frames")


def extract_frames(video_path, output_dir='frames', interval=30):
    """
    Extract frames from video at specified intervals.
    
    Args:
        video_path: Path to the input video file
        output_dir: Directory to save extracted frames
        interval: Extract every Nth frame
    """
    os.makedirs(output_dir, exist_ok=True)
    
    cap = cv2.VideoCapture(video_path)
    
    if not cap.isOpened():
        print(f"Error: Could not open video file {video_path}")
        return
    
    frame_count = 0
    saved_count = 0
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        # Save frame at specified interval
        if frame_count % interval == 0:
            frame_filename = os.path.join(output_dir, f"frame_{frame_count:06d}.jpg")
            cv2.imwrite(frame_filename, frame)
            saved_count += 1
        
        frame_count += 1
    
    cap.release()
    print(f"Extracted {saved_count} frames to {output_dir}")


def get_video_info(video_path):
    """
    Get information about a video file.
    
    Args:
        video_path: Path to the video file
    
    Returns:
        Dictionary with video information
    """
    cap = cv2.VideoCapture(video_path)
    
    if not cap.isOpened():
        return None
    
    info = {
        'fps': cap.get(cv2.CAP_PROP_FPS),
        'width': int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
        'height': int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
        'total_frames': int(cap.get(cv2.CAP_PROP_FRAME_COUNT)),
        'duration': int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) / cap.get(cv2.CAP_PROP_FPS)
    }
    
    cap.release()
    return info


if __name__ == "__main__":
    # Example usage
    video_path = "videos/sample.mp4"
    
    if os.path.exists(video_path):
        # Get video information
        info = get_video_info(video_path)
        if info:
            print("Video Information:")
            print(json.dumps(info, indent=2))
        
        # Process video
        process_video(video_path)
        
        # Extract frames
        extract_frames(video_path, output_dir='frames/extracted_frames', interval=30)
    else:
        print(f"Video file not found: {video_path}")
        print("Please place your video files in the 'videos' directory")

