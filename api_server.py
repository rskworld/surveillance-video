# Project: Surveillance Video Dataset
# Author: Molla Samser
# Website: https://rskworld.in/
# Contact: help@rskworld.in
# Phone: +91 93305 39277
# Address: Nutanhat, Mongolkote, Purba Burdwan, West Bengal, India, 713147

"""
Flask API server for Surveillance Video Dataset.
Provides RESTful endpoints for video processing, analytics, and management.
"""

from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
import json
import os
from datetime import datetime
import cv2
import numpy as np

app = Flask(__name__)
CORS(app)

# API Routes

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'service': 'Surveillance Video Dataset API'
    })

@app.route('/api/analytics', methods=['GET'])
def get_analytics():
    """Get analytics data."""
    try:
        # Load analytics from files or calculate
        analytics_data = {
            'totalVideos': count_videos(),
            'totalDetections': count_detections(),
            'totalAnomalies': count_anomalies(),
            'totalHours': calculate_total_hours(),
            'detections': [45, 52, 38, 21],
            'anomalies': {'unusual_movement': 2, 'rapid_change': 0},
            'activities': {'walking': 45, 'standing': 38, 'running': 12},
            'events': get_recent_events()
        }
        return jsonify(analytics_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/videos', methods=['GET'])
def list_videos():
    """List all videos in the dataset."""
    videos_dir = 'videos'
    videos = []
    
    if os.path.exists(videos_dir):
        for filename in os.listdir(videos_dir):
            if filename.endswith(('.mp4', '.avi', '.mov', '.mkv')):
                video_path = os.path.join(videos_dir, filename)
                video_info = get_video_info(video_path)
                videos.append({
                    'filename': filename,
                    'path': video_path,
                    **video_info
                })
    
    return jsonify({'videos': videos})

@app.route('/api/videos/<filename>', methods=['GET'])
def get_video_info_endpoint(filename):
    """Get information about a specific video."""
    video_path = os.path.join('videos', filename)
    
    if not os.path.exists(video_path):
        return jsonify({'error': 'Video not found'}), 404
    
    info = get_video_info(video_path)
    return jsonify(info)

@app.route('/api/process', methods=['POST'])
def process_video():
    """Process a video file."""
    data = request.json
    video_path = data.get('video_path')
    process_type = data.get('type', 'all')  # all, detection, anomaly, frames
    
    if not video_path or not os.path.exists(video_path):
        return jsonify({'error': 'Video file not found'}), 404
    
    try:
        result = {
            'video_path': video_path,
            'process_type': process_type,
            'status': 'processing',
            'timestamp': datetime.now().isoformat()
        }
        
        # Process video based on type
        if process_type in ['all', 'detection']:
            result['detections'] = process_detections(video_path)
        
        if process_type in ['all', 'anomaly']:
            result['anomalies'] = process_anomalies(video_path)
        
        if process_type in ['all', 'frames']:
            result['frames_extracted'] = extract_frames_count(video_path)
        
        result['status'] = 'completed'
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/batch/process', methods=['POST'])
def batch_process():
    """Process multiple videos in batch."""
    data = request.json
    video_paths = data.get('video_paths', [])
    process_type = data.get('type', 'all')
    
    results = []
    for video_path in video_paths:
        try:
            result = process_video_internal(video_path, process_type)
            results.append(result)
        except Exception as e:
            results.append({
                'video_path': video_path,
                'status': 'failed',
                'error': str(e)
            })
    
    return jsonify({
        'total': len(video_paths),
        'processed': len([r for r in results if r.get('status') == 'completed']),
        'failed': len([r for r in results if r.get('status') == 'failed']),
        'results': results
    })

@app.route('/api/search', methods=['POST'])
def search_videos():
    """Search videos by criteria."""
    data = request.json
    query = data.get('query', '')
    filters = data.get('filters', {})
    
    # Search logic
    results = []
    videos_dir = 'videos'
    
    if os.path.exists(videos_dir):
        for filename in os.listdir(videos_dir):
            if filename.endswith(('.mp4', '.avi', '.mov', '.mkv')):
                if query.lower() in filename.lower():
                    video_path = os.path.join(videos_dir, filename)
                    video_info = get_video_info(video_path)
                    results.append({
                        'filename': filename,
                        'path': video_path,
                        **video_info
                    })
    
    return jsonify({'results': results, 'count': len(results)})

@app.route('/api/annotations/<filename>', methods=['GET'])
def get_annotations(filename):
    """Get annotations for a video."""
    annotation_file = f'annotations/annotations.json'
    
    if os.path.exists(annotation_file):
        with open(annotation_file, 'r') as f:
            annotations = json.load(f)
        return jsonify(annotations)
    
    return jsonify({'error': 'Annotations not found'}), 404

@app.route('/api/quality/<filename>', methods=['GET'])
def get_video_quality(filename):
    """Analyze video quality metrics."""
    video_path = os.path.join('videos', filename)
    
    if not os.path.exists(video_path):
        return jsonify({'error': 'Video not found'}), 404
    
    quality_metrics = analyze_video_quality(video_path)
    return jsonify(quality_metrics)

# Helper Functions

def count_videos():
    """Count total videos."""
    videos_dir = 'videos'
    if os.path.exists(videos_dir):
        return len([f for f in os.listdir(videos_dir) 
                   if f.endswith(('.mp4', '.avi', '.mov', '.mkv'))])
    return 0

def count_detections():
    """Count total detections."""
    detection_file = 'annotations/person_detections.json'
    if os.path.exists(detection_file):
        with open(detection_file, 'r') as f:
            data = json.load(f)
            return len(data.get('detections', []))
    return 0

def count_anomalies():
    """Count total anomalies."""
    anomaly_file = 'annotations/anomalies.json'
    if os.path.exists(anomaly_file):
        with open(anomaly_file, 'r') as f:
            data = json.load(f)
            return len(data.get('anomalies', []))
    return 0

def calculate_total_hours():
    """Calculate total hours of footage."""
    total_seconds = 0
    videos_dir = 'videos'
    
    if os.path.exists(videos_dir):
        for filename in os.listdir(videos_dir):
            if filename.endswith(('.mp4', '.avi', '.mov', '.mkv')):
                video_path = os.path.join(videos_dir, filename)
                cap = cv2.VideoCapture(video_path)
                if cap.isOpened():
                    fps = cap.get(cv2.CAP_PROP_FPS)
                    frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
                    total_seconds += frame_count / fps if fps > 0 else 0
                    cap.release()
    
    return round(total_seconds / 3600, 2)

def get_video_info(video_path):
    """Get video information."""
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        return {}
    
    info = {
        'fps': cap.get(cv2.CAP_PROP_FPS),
        'width': int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
        'height': int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
        'total_frames': int(cap.get(cv2.CAP_PROP_FRAME_COUNT)),
        'duration': int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) / cap.get(cv2.CAP_PROP_FPS) if cap.get(cv2.CAP_PROP_FPS) > 0 else 0
    }
    cap.release()
    return info

def process_detections(video_path):
    """Process video for detections."""
    # This would call the actual detection script
    return {'count': 0, 'message': 'Processing detections'}

def process_anomalies(video_path):
    """Process video for anomalies."""
    # This would call the actual anomaly detection script
    return {'count': 0, 'message': 'Processing anomalies'}

def extract_frames_count(video_path):
    """Extract frames and return count."""
    # This would call the actual frame extraction script
    return 0

def process_video_internal(video_path, process_type):
    """Internal video processing."""
    return {
        'video_path': video_path,
        'status': 'completed',
        'process_type': process_type
    }

def get_recent_events():
    """Get recent events."""
    return [
        {
            'time': datetime.now().strftime('%H:%M:%S'),
            'type': 'detection',
            'message': 'Person detected in frame',
            'video': 'sample.mp4'
        }
    ]

def analyze_video_quality(video_path):
    """Analyze video quality metrics."""
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        return {}
    
    # Get video properties before processing
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    
    # Sample frames for quality analysis
    frames_to_analyze = 10
    quality_scores = []
    
    for i in range(frames_to_analyze):
        ret, frame = cap.read()
        if ret:
            # Calculate quality metrics (simplified)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
            quality_scores.append(laplacian_var)
    
    cap.release()
    
    avg_quality = np.mean(quality_scores) if quality_scores else 0
    quality_percentage = min(100, (avg_quality / 100) * 100)
    
    return {
        'quality_score': round(quality_percentage, 2),
        'resolution': f"{width}x{height}",
        'fps': fps,
        'status': 'high' if quality_percentage > 70 else 'medium' if quality_percentage > 40 else 'low'
    }

if __name__ == '__main__':
    print("Starting Surveillance Video Dataset API Server...")
    print("API Documentation: http://localhost:5000/api/health")
    app.run(debug=True, port=5000)

