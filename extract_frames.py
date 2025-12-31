# Project: Surveillance Video Dataset
# Author: Molla Samser
# Website: https://rskworld.in/
# Contact: help@rskworld.in
# Phone: +91 93305 39277
# Address: Nutanhat, Mongolkote, Purba Burdwan, West Bengal, India, 713147

"""
Frame extraction script for surveillance video dataset.
This script extracts frames from video files at specified intervals.
"""

import cv2
import os
import argparse
from pathlib import Path


def extract_frames(video_path, output_dir='frames/extracted_frames', interval=30, start_frame=0, end_frame=None):
    """
    Extract frames from video at specified intervals.
    
    Args:
        video_path: Path to the input video file
        output_dir: Directory to save extracted frames
        interval: Extract every Nth frame
        start_frame: Starting frame number
        end_frame: Ending frame number (None for all frames)
    """
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Open video
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Error: Could not open video file {video_path}")
        return
    
    # Get video properties
    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    if end_frame is None:
        end_frame = total_frames
    
    print(f"Video: {video_path}")
    print(f"Total frames: {total_frames}")
    print(f"FPS: {fps}")
    print(f"Extracting frames {start_frame} to {end_frame} (interval: {interval})")
    
    frame_count = 0
    saved_count = 0
    
    # Seek to start frame
    cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
    
    while cap.isOpened() and frame_count < end_frame:
        ret, frame = cap.read()
        if not ret:
            break
        
        current_frame = start_frame + frame_count
        
        # Save frame at specified interval
        if current_frame % interval == 0:
            frame_filename = os.path.join(output_dir, f"frame_{current_frame:06d}.jpg")
            cv2.imwrite(frame_filename, frame)
            saved_count += 1
            
            if saved_count % 10 == 0:
                print(f"Extracted {saved_count} frames...")
        
        frame_count += 1
    
    cap.release()
    print(f"Extraction complete. Saved {saved_count} frames to {output_dir}")


def extract_all_frames(video_path, output_dir='frames/extracted_frames'):
    """
    Extract all frames from video.
    
    Args:
        video_path: Path to the input video file
        output_dir: Directory to save extracted frames
    """
    extract_frames(video_path, output_dir, interval=1)


def extract_by_time_interval(video_path, output_dir='frames/extracted_frames', time_interval=1.0):
    """
    Extract frames at specified time intervals.
    
    Args:
        video_path: Path to the input video file
        output_dir: Directory to save extracted frames
        time_interval: Extract frame every N seconds
    """
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Error: Could not open video file {video_path}")
        return
    
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_interval = int(fps * time_interval)
    
    print(f"Extracting frames every {time_interval} seconds (every {frame_interval} frames)")
    extract_frames(video_path, output_dir, interval=frame_interval)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Extract frames from surveillance video')
    parser.add_argument('--video', type=str, default='videos/sample.mp4', help='Path to video file')
    parser.add_argument('--output', type=str, default='frames/extracted_frames', help='Output directory')
    parser.add_argument('--interval', type=int, default=30, help='Extract every Nth frame')
    parser.add_argument('--start', type=int, default=0, help='Starting frame number')
    parser.add_argument('--end', type=int, default=None, help='Ending frame number')
    parser.add_argument('--time-interval', type=float, default=None, help='Extract every N seconds')
    
    args = parser.parse_args()
    
    if os.path.exists(args.video):
        if args.time_interval:
            extract_by_time_interval(args.video, args.output, args.time_interval)
        else:
            extract_frames(args.video, args.output, args.interval, args.start, args.end)
    else:
        print(f"Video file not found: {args.video}")
        print("Usage: python extract_frames.py --video <video_path> [options]")

