# Project: Surveillance Video Dataset
# Author: Molla Samser
# Website: https://rskworld.in/
# Contact: help@rskworld.in
# Phone: +91 93305 39277
# Address: Nutanhat, Mongolkote, Purba Burdwan, West Bengal, India, 713147

"""
Multi-camera surveillance system.
Supports synchronized processing of multiple camera feeds, camera switching, and unified analytics.
"""

import os
import json
import cv2
import numpy as np
from datetime import datetime
from pathlib import Path
import argparse
from concurrent.futures import ThreadPoolExecutor


class MultiCameraSystem:
    """Multi-camera surveillance system."""
    
    def __init__(self, camera_configs=None):
        self.cameras = {}
        self.camera_configs = camera_configs or []
        self.sync_data = {}
    
    def add_camera(self, camera_id, video_path, name=None, location=None):
        """Add a camera to the system."""
        self.cameras[camera_id] = {
            'id': camera_id,
            'video_path': video_path,
            'name': name or f"Camera {camera_id}",
            'location': location or "Unknown",
            'status': 'active',
            'fps': 0,
            'resolution': (0, 0)
        }
    
    def load_camera_config(self, config_file):
        """Load camera configuration from JSON file."""
        if os.path.exists(config_file):
            with open(config_file, 'r') as f:
                configs = json.load(f)
                for config in configs.get('cameras', []):
                    self.add_camera(
                        config['id'],
                        config['video_path'],
                        config.get('name'),
                        config.get('location')
                    )
    
    def get_camera_info(self, camera_id):
        """Get information about a camera."""
        if camera_id in self.cameras:
            camera = self.cameras[camera_id]
            video_path = camera['video_path']
            
            if os.path.exists(video_path):
                cap = cv2.VideoCapture(video_path)
                if cap.isOpened():
                    camera['fps'] = cap.get(cv2.CAP_PROP_FPS)
                    camera['resolution'] = (
                        int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
                        int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                    )
                    camera['total_frames'] = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
                    cap.release()
            
            return camera
        return None
    
    def process_camera(self, camera_id, operations=['detection', 'anomaly']):
        """Process a single camera feed."""
        if camera_id not in self.cameras:
            return {'error': f'Camera {camera_id} not found'}
        
        camera = self.cameras[camera_id]
        video_path = camera['video_path']
        
        if not os.path.exists(video_path):
            return {'error': f'Video file not found: {video_path}'}
        
        results = {
            'camera_id': camera_id,
            'camera_name': camera['name'],
            'video_path': video_path,
            'operations': {},
            'start_time': datetime.now().isoformat()
        }
        
        # Import processing functions
        try:
            from detect_persons import detect_persons_yolo
            from detect_anomalies import detect_anomalies_motion
            
            if 'detection' in operations:
                try:
                    output_file = f"annotations/camera_{camera_id}_detections.json"
                    detect_persons_yolo(video_path, output_file=output_file)
                    results['operations']['detection'] = 'completed'
                except Exception as e:
                    results['operations']['detection'] = f'error: {str(e)}'
            
            if 'anomaly' in operations:
                try:
                    output_file = f"annotations/camera_{camera_id}_anomalies.json"
                    detect_anomalies_motion(video_path, output_file=output_file)
                    results['operations']['anomaly'] = 'completed'
                except Exception as e:
                    results['operations']['anomaly'] = f'error: {str(e)}'
        
        except ImportError as e:
            results['error'] = f'Import error: {str(e)}. Make sure all dependencies are installed.'
        except Exception as e:
            results['error'] = str(e)
        
        results['end_time'] = datetime.now().isoformat()
        return results
    
    def process_all_cameras(self, operations=['detection', 'anomaly'], parallel=True):
        """Process all cameras in the system."""
        camera_ids = list(self.cameras.keys())
        
        if parallel:
            with ThreadPoolExecutor(max_workers=len(camera_ids)) as executor:
                futures = {
                    executor.submit(self.process_camera, cam_id, operations): cam_id
                    for cam_id in camera_ids
                }
                
                results = []
                for future in futures:
                    result = future.result()
                    results.append(result)
                
                return results
        else:
            results = []
            for camera_id in camera_ids:
                result = self.process_camera(camera_id, operations)
                results.append(result)
            return results
    
    def synchronize_cameras(self, timestamp):
        """Synchronize multiple camera feeds at a specific timestamp."""
        synchronized_frames = {}
        
        for camera_id, camera in self.cameras.items():
            video_path = camera['video_path']
            if os.path.exists(video_path):
                cap = cv2.VideoCapture(video_path)
                fps = cap.get(cv2.CAP_PROP_FPS)
                frame_number = int(timestamp * fps)
                
                cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
                ret, frame = cap.read()
                
                if ret:
                    synchronized_frames[camera_id] = {
                        'frame': frame,
                        'timestamp': timestamp,
                        'camera_name': camera['name']
                    }
                
                cap.release()
        
        return synchronized_frames
    
    def generate_unified_report(self):
        """Generate unified analytics report for all cameras."""
        report = {
            'total_cameras': len(self.cameras),
            'cameras': [],
            'summary': {
                'total_detections': 0,
                'total_anomalies': 0,
                'active_cameras': 0
            },
            'timestamp': datetime.now().isoformat()
        }
        
        for camera_id, camera in self.cameras.items():
            camera_info = self.get_camera_info(camera_id)
            report['cameras'].append(camera_info)
            
            if camera_info.get('status') == 'active':
                report['summary']['active_cameras'] += 1
            
            # Load detection and anomaly data
            detections_file = f"annotations/camera_{camera_id}_detections.json"
            anomalies_file = f"annotations/camera_{camera_id}_anomalies.json"
            
            if os.path.exists(detections_file):
                with open(detections_file, 'r') as f:
                    detections = json.load(f)
                    report['summary']['total_detections'] += len(detections.get('detections', []))
            
            if os.path.exists(anomalies_file):
                with open(anomalies_file, 'r') as f:
                    anomalies = json.load(f)
                    report['summary']['total_anomalies'] += len(anomalies.get('anomalies', []))
        
        return report
    
    def create_camera_grid_view(self, timestamp=None):
        """Create a grid view of all camera feeds."""
        if timestamp is None:
            timestamp = 0.0
        
        synchronized_frames = self.synchronize_cameras(timestamp)
        
        if not synchronized_frames:
            return None
        
        # Determine grid layout
        num_cameras = len(synchronized_frames)
        cols = int(np.ceil(np.sqrt(num_cameras)))
        rows = int(np.ceil(num_cameras / cols))
        
        # Get frame dimensions from first camera
        first_frame = list(synchronized_frames.values())[0]['frame']
        h, w = first_frame.shape[:2]
        
        # Create grid
        grid = np.zeros((rows * h, cols * w, 3), dtype=np.uint8)
        
        for idx, (camera_id, data) in enumerate(synchronized_frames.items()):
            frame = data['frame']
            frame = cv2.resize(frame, (w, h))
            
            row = idx // cols
            col = idx % cols
            
            y1 = row * h
            y2 = y1 + h
            x1 = col * w
            x2 = x1 + w
            
            grid[y1:y2, x1:x2] = frame
            
            # Add camera label
            cv2.putText(grid, data['camera_name'], (x1 + 10, y1 + 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        return grid


def create_sample_camera_config():
    """Create sample camera configuration file."""
    config = {
        'cameras': [
            {
                'id': 'cam001',
                'name': 'Main Entrance',
                'location': 'Building A - Front Door',
                'video_path': 'videos/sample.mp4'
            },
            {
                'id': 'cam002',
                'name': 'Parking Lot',
                'location': 'Building A - Parking Area',
                'video_path': 'videos/sample2.mp4'
            }
        ]
    }
    
    os.makedirs('config', exist_ok=True)
    with open('config/cameras.json', 'w') as f:
        json.dump(config, f, indent=2)
    
    print("Sample camera configuration created: config/cameras.json")


def main():
    parser = argparse.ArgumentParser(description='Multi-camera surveillance system')
    parser.add_argument('--config', '-c', default='config/cameras.json',
                       help='Camera configuration file')
    parser.add_argument('--create-config', action='store_true',
                       help='Create sample camera configuration')
    parser.add_argument('--process', '-p', nargs='+',
                       choices=['detection', 'anomaly', 'all'],
                       default=['all'],
                       help='Operations to perform')
    parser.add_argument('--sync', '-s', type=float, help='Synchronize cameras at timestamp')
    parser.add_argument('--grid', '-g', action='store_true',
                       help='Create grid view of all cameras')
    
    args = parser.parse_args()
    
    if args.create_config:
        create_sample_camera_config()
        return
    
    system = MultiCameraSystem()
    
    if os.path.exists(args.config):
        system.load_camera_config(args.config)
    else:
        print(f"Configuration file not found: {args.config}")
        print("Use --create-config to create a sample configuration")
        return
    
    print(f"Loaded {len(system.cameras)} cameras")
    
    # Process operations
    operations = args.process
    if 'all' in operations:
        operations = ['detection', 'anomaly']
    
    if args.sync is not None:
        # Synchronize cameras
        frames = system.synchronize_cameras(args.sync)
        print(f"Synchronized {len(frames)} cameras at timestamp {args.sync}")
    
    if args.grid:
        # Create grid view
        grid = system.create_camera_grid_view(args.sync or 0.0)
        if grid is not None:
            output_path = 'output/camera_grid.jpg'
            os.makedirs('output', exist_ok=True)
            cv2.imwrite(output_path, grid)
            print(f"Camera grid saved to: {output_path}")
    
    # Process all cameras
    results = system.process_all_cameras(operations)
    
    # Generate report
    report = system.generate_unified_report()
    
    report_file = 'output/multi_camera_report.json'
    os.makedirs('output', exist_ok=True)
    with open(report_file, 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"\nMulti-camera processing complete!")
    print(f"Report saved to: {report_file}")
    print(f"Summary: {report['summary']}")


if __name__ == '__main__':
    main()

