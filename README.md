<!--
Project: Surveillance Video Dataset
Author: Molla Samser
Website: https://rskworld.in/
Contact: help@rskworld.in
Phone: +91 93305 39277
Address: Nutanhat, Mongolkote, Purba Burdwan, West Bengal, India, 713147
-->

# Surveillance Video Dataset

## Overview

This dataset contains surveillance camera footage with activity labels, person detection, and anomaly events. Perfect for security monitoring, activity recognition, and video surveillance applications.

## Project Details

- **ID**: 28
- **Title**: Surveillance Video Dataset
- **Category**: Video Data
- **Difficulty**: Advanced
- **Technologies**: MP4, AVI, OpenCV, YOLO, Video Processing
- **Year**: 2026

## Features

- **Security Camera Footage**: High-quality surveillance video recordings
- **Activity Labels**: Comprehensive activity annotations
- **Person Detection**: Pre-labeled person detection data
- **Anomaly Events**: Marked anomaly detection events
- **Ready for Surveillance AI**: Optimized for AI model training

## Quick Start

### Installation

1. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run setup script:**
   ```bash
   python setup.py
   ```

### Basic Usage

#### 1. Process a Video
```bash
python process_video.py
```

#### 2. Detect Persons in Video
```bash
python detect_persons.py
```

#### 3. Detect Anomalies
```bash
python detect_anomalies.py
```

#### 4. Extract Frames
```bash
python extract_frames.py --video videos/sample.mp4 --interval 30
```

#### 5. Create Sample Videos
```bash
python create_sample_video.py
```

## Dataset Structure

```
surveillance-video/
├── index.html                      # Main demo page
├── analytics_dashboard.html        # Advanced analytics dashboard
├── styles.css                      # Main stylesheet
├── script.js                       # Main JavaScript
├── analytics.js                    # Analytics dashboard JavaScript
│
├── process_video.py                # Basic video processing
├── detect_persons.py              # Person detection
├── detect_anomalies.py            # Anomaly detection
├── extract_frames.py              # Frame extraction
│
├── api_server.py                  # Flask REST API server
├── batch_processor.py             # Batch processing system
├── train_ml_model.py              # ML model training
├── video_quality_analyzer.py      # Video quality analysis
├── multi_camera_system.py         # Multi-camera system
├── video_search.py                # Video search engine
├── alert_system.py                # Alert/notification system
│
├── videos/                        # Video files directory
│   ├── sample.mp4                  # Main sample video
│   ├── sample2.mp4                # Secondary sample video
│   └── video_metadata.json         # Video metadata
│
├── annotations/                   # Annotation files
│   ├── annotations.json           # Activity annotations
│   ├── person_detections.json     # Person detections
│   └── anomalies.json             # Anomaly events
│
├── frames/                        # Extracted frames directory
│   └── extracted_frames/          # Extracted video frames
│
├── output/                        # Output files directory
├── config/                        # Configuration files directory
└── models/                        # Trained ML models directory
```

## Usage Examples

### Basic Video Processing

```python
import cv2
import json

# Load video
cap = cv2.VideoCapture('videos/sample.mp4')

# Load annotations
with open('annotations/annotations.json', 'r') as f:
    annotations = json.load(f)

# Process video
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    
    # Your processing code here
    cv2.imshow('Frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
```

### Person Detection with YOLO

```python
from ultralytics import YOLO
import cv2

# Load YOLO model
model = YOLO('yolov8n.pt')

# Process surveillance video
results = model('videos/sample.mp4')

# Display results
for result in results:
    annotated_frame = result.plot()
    cv2.imshow('Detection', annotated_frame)
    cv2.waitKey(1)
```

### Anomaly Detection

```python
import cv2
import json

# Load anomaly events
with open('annotations/anomalies.json', 'r') as f:
    anomalies = json.load(f)

# Process video with anomaly detection
cap = cv2.VideoCapture('videos/sample.mp4')
fps = cap.get(cv2.CAP_PROP_FPS)
frame_count = 0

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    
    current_time = frame_count / fps
    
    # Check for anomalies at current time
    for anomaly in anomalies['anomalies']:
        if anomaly['start_time'] <= current_time <= anomaly['end_time']:
            # Mark anomaly in frame
            cv2.putText(frame, 'ANOMALY DETECTED', (10, 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    
    cv2.imshow('Anomaly Detection', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
    frame_count += 1

cap.release()
cv2.destroyAllWindows()
```

## Advanced Features

### 1. Analytics Dashboard

**File:** `analytics_dashboard.html`

Real-time analytics dashboard with:
- Statistics cards (videos, detections, anomalies, hours)
- Interactive charts (detections over time, anomaly distribution, activity types)
- Real-time event timeline
- Video quality metrics
- Export capabilities (JSON, CSV, PDF)

**Usage:**
```bash
# Open in browser
open analytics_dashboard.html
```

### 2. REST API Server

**File:** `api_server.py`

Flask-based REST API with endpoints:
- `GET /api/health` - Health check
- `GET /api/analytics` - Get analytics data
- `GET /api/videos` - List all videos
- `GET /api/videos/<filename>` - Get video info
- `POST /api/process` - Process a video
- `POST /api/batch/process` - Batch process videos
- `POST /api/search` - Search videos
- `GET /api/annotations/<filename>` - Get annotations
- `GET /api/quality/<filename>` - Get quality metrics

**Usage:**
```bash
python api_server.py
# API available at http://localhost:5000
```

### 3. Batch Processing System

**File:** `batch_processor.py`

Advanced batch processing with:
- Parallel processing of multiple videos
- Progress tracking
- Error handling and reporting
- Support for multiple operations (detection, anomaly, frames)
- Comprehensive processing reports

**Usage:**
```bash
# Process all videos in directory
python batch_processor.py --directory videos --operations all --workers 4

# Process specific videos
python batch_processor.py --videos sample.mp4 sample2.mp4 --operations detection anomaly
```

### 4. ML Model Training

**File:** `train_ml_model.py`

Machine learning model training for:
- Custom YOLO model fine-tuning
- Activity recognition (CNN-based)
- Anomaly detection (Autoencoder-based)
- Support for PyTorch models

**Usage:**
```bash
# Train all models
python train_ml_model.py --model all --epochs 20

# Train specific model
python train_ml_model.py --model yolo --epochs 50
```

### 5. Video Quality Analyzer

**File:** `video_quality_analyzer.py`

Comprehensive video quality analysis:
- Sharpness analysis (Laplacian variance)
- Brightness and contrast metrics
- Noise estimation
- Color balance analysis
- Frame stability (optical flow)
- Overall quality scoring

**Usage:**
```bash
# Analyze single video
python video_quality_analyzer.py videos/sample.mp4 --output output/quality_report.json

# Batch analyze all videos
python video_quality_analyzer.py videos --batch --output output/quality_report.json
```

### 6. Multi-Camera System

**File:** `multi_camera_system.py`

Multi-camera surveillance system:
- Support for multiple camera feeds
- Synchronized processing
- Camera grid view
- Unified analytics
- Parallel processing

**Usage:**
```bash
# Create sample config
python multi_camera_system.py --create-config

# Process all cameras
python multi_camera_system.py --config config/cameras.json --process all

# Create synchronized grid view
python multi_camera_system.py --config config/cameras.json --grid --sync 10.0
```

### 7. Video Search Engine

**File:** `video_search.py`

Advanced search and filtering:
- Text-based search
- Metadata filtering
- Timestamp-based search
- Event type filtering
- Activity type filtering
- Duration and resolution filters

**Usage:**
```bash
# Search videos
python video_search.py --query "sample" --event-type anomaly

# Filter by timestamp
python video_search.py --video sample.mp4 --timestamp 10.5

# Complex search
python video_search.py --query "sample" --min-duration 10 --max-duration 20 --event-type detection
```

### 8. Alert System

**File:** `alert_system.py`

Real-time alert and notification system:
- Anomaly detection alerts
- Person count threshold alerts
- Video quality alerts
- Multiple notification channels (console, file, email)
- Alert management and reporting

**Usage:**
```bash
# Create config
python alert_system.py --create-config

# Check all alerts
python alert_system.py --check-all

# Generate report
python alert_system.py --check-all --report
```

## File Formats

### Annotations JSON Format

```json
{
    "video_id": "sample.mp4",
    "activities": [
        {
            "id": 1,
            "type": "walking",
            "start_time": 0.0,
            "end_time": 5.2,
            "person_id": 1
        }
    ]
}
```

### Person Detection JSON Format

```json
{
    "video_id": "sample.mp4",
    "detections": [
        {
            "frame": 0,
            "timestamp": 0.0,
            "persons": [
                {
                    "id": 1,
                    "bbox": [100, 150, 200, 300],
                    "confidence": 0.95
                }
            ]
        }
    ]
}
```

### Anomaly Events JSON Format

```json
{
    "video_id": "sample.mp4",
    "anomalies": [
        {
            "id": 1,
            "type": "unusual_movement",
            "start_time": 10.5,
            "end_time": 12.3,
            "description": "Rapid movement detected"
        }
    ]
}
```

## Video Files

### Creating Sample Videos

#### Option 1: Generate Synthetic Videos

Run the Python script to create synthetic sample videos:

```bash
python create_sample_video.py
```

This will create:
- `videos/sample.mp4` - Basic surveillance video with moving object
- `videos/sample2.mp4` - Video with multiple objects and anomaly events

#### Option 2: Add Your Own Videos

1. Place your surveillance video files in the `videos/` directory
2. Name them `sample.mp4` and `sample2.mp4`
3. Ensure they are in MP4 format
4. Recommended: 640x480 or 1920x1080 resolution, 30 fps

### Video Specifications

- **Format**: MP4 (H.264 codec recommended)
- **Resolution**: 640x480 or higher
- **Frame Rate**: 30 fps
- **Duration**: 10-15 seconds for samples

## Dependencies

### Required

```bash
pip install -r requirements.txt
```

**Core Dependencies:**
- opencv-python>=4.8.0
- numpy>=1.24.0
- ultralytics>=8.0.0
- Pillow>=10.0.0

**Advanced Features:**
- flask>=2.3.0
- flask-cors>=4.0.0
- torch>=2.0.0 (for ML training)
- torchvision>=0.15.0 (for ML training)

## Configuration

### Configuration Files

- `config.py` - General project configuration
- `config/alert_config.json` - Alert system configuration (create with `python alert_system.py --create-config`)
- `config/cameras.json` - Multi-camera configuration (create with `python multi_camera_system.py --create-config`)

## Output Files

All processing results are saved to the `output/` directory:
- `batch_report_*.json` - Batch processing reports
- `quality_report.json` - Quality analysis results
- `multi_camera_report.json` - Multi-camera analytics
- `search_results.json` - Search results
- `alert_report.json` - Alert reports
- `alerts_*.json` - Daily alert logs

## Verification

Run the verification script to check project status:

```bash
python verify_project.py
```

This will verify:
- All required directories exist
- All required files are present
- Python dependencies are installed
- Project structure is complete

## Demo

Visit the demo page at `index.html` to see the dataset in action.

## Download

Download the complete dataset: [surveillance-video.zip](./surveillance-video.zip)

## License

This dataset is provided for research and educational purposes. See `LICENSE` file for details.

## Contact

- **Author**: Molla Samser
- **Website**: https://rskworld.in/
- **Email**: help@rskworld.in
- **Phone**: +91 93305 39277
- **Address**: Nutanhat, Mongolkote, Purba Burdwan, West Bengal, India, 713147

## Acknowledgments

Created by Molla Samser - rskworld.in
