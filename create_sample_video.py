# Project: Surveillance Video Dataset
# Author: Molla Samser
# Website: https://rskworld.in/
# Contact: help@rskworld.in
# Phone: +91 93305 39277
# Address: Nutanhat, Mongolkote, Purba Burdwan, West Bengal, India, 713147

"""
Script to create sample surveillance video for testing purposes.
This creates a simple synthetic video with moving objects.
"""

import cv2
import numpy as np
import os


def create_sample_video(output_path='videos/sample.mp4', duration=12, fps=30, width=640, height=480):
    """
    Create a sample surveillance video with moving objects.
    
    Args:
        output_path: Path to save the video
        duration: Duration in seconds
        fps: Frames per second
        width: Video width
        height: Video height
    """
    # Create output directory if it doesn't exist
    os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else '.', exist_ok=True)
    
    # Define codec and create VideoWriter
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
    
    total_frames = int(duration * fps)
    
    print(f"Creating sample video: {output_path}")
    print(f"Duration: {duration}s, FPS: {fps}, Resolution: {width}x{height}")
    print(f"Total frames: {total_frames}")
    
    # Create background (simulating surveillance camera view)
    background_color = (40, 40, 40)  # Dark gray
    
    # Object properties (simulating a person)
    obj_size = 50
    obj_color = (0, 255, 0)  # Green
    start_x = 50
    start_y = height // 2
    end_x = width - 50
    end_y = height // 2
    
    for frame_num in range(total_frames):
        # Create frame
        frame = np.full((height, width, 3), background_color, dtype=np.uint8)
        
        # Add grid pattern (simulating surveillance camera)
        for i in range(0, width, 50):
            cv2.line(frame, (i, 0), (i, height), (60, 60, 60), 1)
        for i in range(0, height, 50):
            cv2.line(frame, (0, i), (width, i), (60, 60, 60), 1)
        
        # Add timestamp
        timestamp = frame_num / fps
        cv2.putText(frame, f"Time: {timestamp:.2f}s", (10, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        cv2.putText(frame, "Sample Surveillance Video", (10, height - 20),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 200, 200), 1)
        
        # Animate moving object (person)
        progress = frame_num / total_frames
        x = int(start_x + (end_x - start_x) * progress)
        y = int(start_y + (end_y - start_y) * progress)
        
        # Draw object (rectangle representing person)
        cv2.rectangle(frame, (x - obj_size//2, y - obj_size), 
                     (x + obj_size//2, y), obj_color, -1)
        cv2.circle(frame, (x, y - obj_size//2), obj_size//4, (0, 200, 0), -1)
        
        # Add some variation (walking animation)
        if frame_num % 10 < 5:
            cv2.line(frame, (x - obj_size//2, y), (x - obj_size//2, y + 10), obj_color, 3)
            cv2.line(frame, (x + obj_size//2, y), (x + obj_size//2, y + 10), obj_color, 3)
        else:
            cv2.line(frame, (x - obj_size//2, y), (x - obj_size//2, y + 15), obj_color, 3)
            cv2.line(frame, (x + obj_size//2, y), (x + obj_size//2, y + 5), obj_color, 3)
        
        # Write frame
        out.write(frame)
        
        if frame_num % 30 == 0:
            print(f"Progress: {frame_num}/{total_frames} frames ({progress*100:.1f}%)")
    
    out.release()
    print(f"Sample video created successfully: {output_path}")
    print(f"File size: {os.path.getsize(output_path) / (1024*1024):.2f} MB")


def create_sample_video_2(output_path='videos/sample2.mp4', duration=15, fps=30, width=640, height=480):
    """
    Create a second sample video with multiple objects and anomalies.
    """
    os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else '.', exist_ok=True)
    
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
    
    total_frames = int(duration * fps)
    
    print(f"Creating sample video 2: {output_path}")
    print(f"Duration: {duration}s, FPS: {fps}, Resolution: {width}x{height}")
    
    background_color = (40, 40, 40)
    
    for frame_num in range(total_frames):
        frame = np.full((height, width, 3), background_color, dtype=np.uint8)
        
        # Grid pattern
        for i in range(0, width, 50):
            cv2.line(frame, (i, 0), (i, height), (60, 60, 60), 1)
        for i in range(0, height, 50):
            cv2.line(frame, (0, i), (width, i), (60, 60, 60), 1)
        
        timestamp = frame_num / fps
        cv2.putText(frame, f"Time: {timestamp:.2f}s", (10, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        cv2.putText(frame, "Sample Surveillance Video 2", (10, height - 20),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 200, 200), 1)
        
        # First object (person 1)
        obj1_size = 50
        obj1_color = (0, 255, 0)
        progress1 = min(frame_num / (total_frames * 0.4), 1.0)
        x1 = int(50 + (width - 100) * progress1)
        y1 = height // 3
        
        cv2.rectangle(frame, (x1 - obj1_size//2, y1 - obj1_size), 
                     (x1 + obj1_size//2, y1), obj1_color, -1)
        cv2.circle(frame, (x1, y1 - obj1_size//2), obj1_size//4, (0, 200, 0), -1)
        
        # Second object (person 2) - appears later
        if frame_num > total_frames * 0.3:
            obj2_size = 50
            obj2_color = (255, 0, 0)
            progress2 = min((frame_num - total_frames * 0.3) / (total_frames * 0.4), 1.0)
            x2 = int(width - 50 - (width - 100) * progress2)
            y2 = 2 * height // 3
            
            cv2.rectangle(frame, (x2 - obj2_size//2, y2 - obj2_size), 
                         (x2 + obj2_size//2, y2), obj2_color, -1)
            cv2.circle(frame, (x2, y2 - obj2_size//2), obj2_size//4, (200, 0, 0), -1)
        
        # Anomaly: rapid movement (around 10-12 seconds)
        if 10.0 <= timestamp <= 12.3:
            anomaly_color = (0, 0, 255)
            cv2.putText(frame, "ANOMALY DETECTED", (width//2 - 150, height//2),
                       cv2.FONT_HERSHEY_SIMPLEX, 1, anomaly_color, 3)
            # Rapid movement
            x_anomaly = int(width//2 + 100 * np.sin(frame_num * 0.5))
            y_anomaly = int(height//2 + 50 * np.cos(frame_num * 0.5))
            cv2.circle(frame, (x_anomaly, y_anomaly), 30, anomaly_color, -1)
        
        out.write(frame)
        
        if frame_num % 30 == 0:
            print(f"Progress: {frame_num}/{total_frames} frames")
    
    out.release()
    print(f"Sample video 2 created successfully: {output_path}")
    print(f"File size: {os.path.getsize(output_path) / (1024*1024):.2f} MB")


if __name__ == "__main__":
    print("=" * 60)
    print("Creating Sample Surveillance Videos")
    print("=" * 60)
    
    # Create sample video 1
    create_sample_video('videos/sample.mp4', duration=12, fps=30, width=640, height=480)
    
    print("\n" + "-" * 60 + "\n")
    
    # Create sample video 2
    create_sample_video_2('videos/sample2.mp4', duration=15, fps=30, width=640, height=480)
    
    print("\n" + "=" * 60)
    print("All sample videos created successfully!")
    print("=" * 60)

