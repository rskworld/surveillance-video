# Project: Surveillance Video Dataset
# Author: Molla Samser
# Website: https://rskworld.in/
# Contact: help@rskworld.in
# Phone: +91 93305 39277
# Address: Nutanhat, Mongolkote, Purba Burdwan, West Bengal, India, 713147

"""
Person detection script using YOLO for surveillance video dataset.
This script detects persons in video frames and saves detection results.
"""

import cv2
import json
import os
from pathlib import Path

try:
    from ultralytics import YOLO
    YOLO_AVAILABLE = True
except ImportError:
    YOLO_AVAILABLE = False
    print("Warning: ultralytics not installed. Install with: pip install ultralytics")


def detect_persons_yolo(video_path, model_path='yolov8n.pt', output_file='annotations/person_detections.json'):
    """
    Detect persons in video using YOLO model.
    
    Args:
        video_path: Path to the input video file
        model_path: Path to YOLO model file
        output_file: Path to save detection results
    """
    if not YOLO_AVAILABLE:
        print("Error: YOLO is not available. Please install ultralytics.")
        return
    
    # Create output directory if it doesn't exist
    os.makedirs(os.path.dirname(output_file) if os.path.dirname(output_file) else '.', exist_ok=True)
    
    # Load YOLO model
    print(f"Loading YOLO model: {model_path}")
    model = YOLO(model_path)
    
    # Open video
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Error: Could not open video file {video_path}")
        return
    
    fps = cap.get(cv2.CAP_PROP_FPS)
    detections = []
    frame_count = 0
    
    print("Processing video for person detection...")
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        # Run YOLO detection
        results = model(frame, verbose=False)
        
        # Process results
        persons = []
        for result in results:
            boxes = result.boxes
            for box in boxes:
                # Check if detected object is a person (class 0 in COCO dataset)
                if int(box.cls) == 0:  # Person class
                    x1, y1, x2, y2 = box.xyxy[0].tolist()
                    confidence = float(box.conf[0])
                    
                    persons.append({
                        'bbox': [int(x1), int(y1), int(x2), int(y2)],
                        'confidence': round(confidence, 4)
                    })
        
        # Save detection for this frame
        if persons:
            detections.append({
                'frame': frame_count,
                'timestamp': round(frame_count / fps, 2),
                'persons': persons
            })
        
        # Display frame with detections
        annotated_frame = results[0].plot()
        cv2.imshow('Person Detection', annotated_frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
        frame_count += 1
    
    cap.release()
    cv2.destroyAllWindows()
    
    # Save detections to JSON
    output_data = {
        'video_id': os.path.basename(video_path),
        'total_frames': frame_count,
        'fps': fps,
        'detections': detections
    }
    
    with open(output_file, 'w') as f:
        json.dump(output_data, f, indent=2)
    
    print(f"Detection complete. Found persons in {len(detections)} frames.")
    print(f"Results saved to {output_file}")


def detect_persons_opencv(video_path, output_file='annotations/person_detections.json'):
    """
    Detect persons using OpenCV's HOG descriptor (alternative to YOLO).
    
    Args:
        video_path: Path to the input video file
        output_file: Path to save detection results
    """
    # Initialize HOG descriptor for person detection
    hog = cv2.HOGDescriptor()
    hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
    
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Error: Could not open video file {video_path}")
        return
    
    fps = cap.get(cv2.CAP_PROP_FPS)
    detections = []
    frame_count = 0
    
    print("Processing video for person detection using OpenCV HOG...")
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        # Detect persons
        boxes, weights = hog.detectMultiScale(frame, winStride=(8, 8), padding=(32, 32), scale=1.05)
        
        persons = []
        for (x, y, w, h), weight in zip(boxes, weights):
            if weight > 0.5:  # Confidence threshold
                persons.append({
                    'bbox': [int(x), int(y), int(x + w), int(y + h)],
                    'confidence': round(float(weight), 4)
                })
                
                # Draw bounding box
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        
        if persons:
            detections.append({
                'frame': frame_count,
                'timestamp': round(frame_count / fps, 2),
                'persons': persons
            })
        
        cv2.imshow('Person Detection (OpenCV)', frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
        frame_count += 1
    
    cap.release()
    cv2.destroyAllWindows()
    
    # Save detections
    os.makedirs(os.path.dirname(output_file) if os.path.dirname(output_file) else '.', exist_ok=True)
    
    output_data = {
        'video_id': os.path.basename(video_path),
        'total_frames': frame_count,
        'fps': fps,
        'detections': detections
    }
    
    with open(output_file, 'w') as f:
        json.dump(output_data, f, indent=2)
    
    print(f"Detection complete. Found persons in {len(detections)} frames.")
    print(f"Results saved to {output_file}")


if __name__ == "__main__":
    video_path = "videos/sample.mp4"
    
    if os.path.exists(video_path):
        # Try YOLO first, fallback to OpenCV
        if YOLO_AVAILABLE:
            detect_persons_yolo(video_path)
        else:
            print("Using OpenCV HOG detector (YOLO not available)")
            detect_persons_opencv(video_path)
    else:
        print(f"Video file not found: {video_path}")
        print("Please place your video files in the 'videos' directory")

