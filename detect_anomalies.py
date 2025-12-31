# Project: Surveillance Video Dataset
# Author: Molla Samser
# Website: https://rskworld.in/
# Contact: help@rskworld.in
# Phone: +91 93305 39277
# Address: Nutanhat, Mongolkote, Purba Burdwan, West Bengal, India, 713147

"""
Anomaly detection script for surveillance video dataset.
This script detects anomalies such as unusual movements, rapid changes, etc.
"""

import cv2
import json
import numpy as np
import os
from pathlib import Path


def detect_anomalies_motion(video_path, output_file='annotations/anomalies.json', threshold=5000):
    """
    Detect anomalies based on motion detection.
    
    Args:
        video_path: Path to the input video file
        output_file: Path to save anomaly results
        threshold: Motion threshold for anomaly detection
    """
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Error: Could not open video file {video_path}")
        return
    
    fps = cap.get(cv2.CAP_PROP_FPS)
    
    # Initialize background subtractor
    back_sub = cv2.createBackgroundSubtractorMOG2(history=500, varThreshold=50, detectShadows=True)
    
    anomalies = []
    frame_count = 0
    motion_history = []
    window_size = int(fps * 2)  # 2 seconds window
    
    print("Processing video for anomaly detection...")
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        # Apply background subtraction
        fg_mask = back_sub.apply(frame)
        
        # Calculate motion amount
        motion_amount = np.sum(fg_mask > 0)
        motion_history.append(motion_amount)
        
        # Keep only recent history
        if len(motion_history) > window_size:
            motion_history.pop(0)
        
        # Calculate average motion
        if len(motion_history) >= window_size:
            avg_motion = np.mean(motion_history)
            std_motion = np.std(motion_history)
            
            # Detect anomaly: motion significantly above average
            if motion_amount > avg_motion + 2 * std_motion and motion_amount > threshold:
                current_time = frame_count / fps
                
                # Check if this is continuation of previous anomaly
                if anomalies and current_time - anomalies[-1]['end_time'] < 1.0:
                    anomalies[-1]['end_time'] = current_time
                else:
                    anomalies.append({
                        'id': len(anomalies) + 1,
                        'type': 'unusual_movement',
                        'start_time': round(current_time, 2),
                        'end_time': round(current_time, 2),
                        'description': f'Rapid movement detected (motion: {motion_amount:.0f})'
                    })
        
        # Visualize
        cv2.imshow('Anomaly Detection', fg_mask)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
        frame_count += 1
    
    cap.release()
    cv2.destroyAllWindows()
    
    # Save anomalies
    os.makedirs(os.path.dirname(output_file) if os.path.dirname(output_file) else '.', exist_ok=True)
    
    output_data = {
        'video_id': os.path.basename(video_path),
        'total_frames': frame_count,
        'fps': fps,
        'anomalies': anomalies
    }
    
    with open(output_file, 'w') as f:
        json.dump(output_data, f, indent=2)
    
    print(f"Anomaly detection complete. Found {len(anomalies)} anomaly events.")
    print(f"Results saved to {output_file}")


def detect_anomalies_optical_flow(video_path, output_file='annotations/anomalies.json'):
    """
    Detect anomalies using optical flow.
    
    Args:
        video_path: Path to the input video file
        output_file: Path to save anomaly results
    """
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Error: Could not open video file {video_path}")
        return
    
    fps = cap.get(cv2.CAP_PROP_FPS)
    
    # Read first frame
    ret, old_frame = cap.read()
    old_gray = cv2.cvtColor(old_frame, cv2.COLOR_BGR2GRAY)
    
    anomalies = []
    frame_count = 0
    flow_history = []
    window_size = int(fps * 2)
    
    print("Processing video for anomaly detection using optical flow...")
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Calculate optical flow
        flow = cv2.calcOpticalFlowFarneback(old_gray, frame_gray, None, 0.5, 3, 15, 3, 5, 1.2, 0)
        
        # Calculate magnitude of flow
        magnitude = np.sqrt(flow[..., 0]**2 + flow[..., 1]**2)
        avg_magnitude = np.mean(magnitude)
        flow_history.append(avg_magnitude)
        
        if len(flow_history) > window_size:
            flow_history.pop(0)
        
        # Detect anomaly
        if len(flow_history) >= window_size:
            avg_flow = np.mean(flow_history)
            std_flow = np.std(flow_history)
            
            if avg_magnitude > avg_flow + 2 * std_flow:
                current_time = frame_count / fps
                
                if anomalies and current_time - anomalies[-1]['end_time'] < 1.0:
                    anomalies[-1]['end_time'] = current_time
                else:
                    anomalies.append({
                        'id': len(anomalies) + 1,
                        'type': 'unusual_movement',
                        'start_time': round(current_time, 2),
                        'end_time': round(current_time, 2),
                        'description': f'Unusual optical flow detected'
                    })
        
        # Visualize optical flow
        hsv = np.zeros_like(frame)
        hsv[..., 1] = 255
        mag, ang = cv2.cartToPolar(flow[..., 0], flow[..., 1])
        hsv[..., 0] = ang * 180 / np.pi / 2
        hsv[..., 2] = cv2.normalize(mag, None, 0, 255, cv2.NORM_MINMAX)
        bgr = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
        
        cv2.imshow('Optical Flow', bgr)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
        old_gray = frame_gray.copy()
        frame_count += 1
    
    cap.release()
    cv2.destroyAllWindows()
    
    # Save anomalies
    os.makedirs(os.path.dirname(output_file) if os.path.dirname(output_file) else '.', exist_ok=True)
    
    output_data = {
        'video_id': os.path.basename(video_path),
        'total_frames': frame_count,
        'fps': fps,
        'anomalies': anomalies
    }
    
    with open(output_file, 'w') as f:
        json.dump(output_data, f, indent=2)
    
    print(f"Anomaly detection complete. Found {len(anomalies)} anomaly events.")
    print(f"Results saved to {output_file}")


if __name__ == "__main__":
    video_path = "videos/sample.mp4"
    
    if os.path.exists(video_path):
        # Use motion-based detection
        detect_anomalies_motion(video_path)
        
        # Alternative: Use optical flow
        # detect_anomalies_optical_flow(video_path)
    else:
        print(f"Video file not found: {video_path}")
        print("Please place your video files in the 'videos' directory")

