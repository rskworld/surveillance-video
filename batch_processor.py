# Project: Surveillance Video Dataset
# Author: Molla Samser
# Website: https://rskworld.in/
# Contact: help@rskworld.in
# Phone: +91 93305 39277
# Address: Nutanhat, Mongolkote, Purba Burdwan, West Bengal, India, 713147

"""
Advanced batch processing system for multiple surveillance videos.
Supports parallel processing, progress tracking, and error handling.
"""

import os
import json
import cv2
from pathlib import Path
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
import argparse


class BatchProcessor:
    """Batch processor for surveillance videos."""
    
    def __init__(self, max_workers=4):
        self.max_workers = max_workers
        self.results = []
        self.errors = []
    
    def process_video(self, video_path, operations=['detection', 'anomaly', 'frames']):
        """
        Process a single video with specified operations.
        
        Args:
            video_path: Path to video file
            operations: List of operations to perform
        """
        result = {
            'video_path': video_path,
            'filename': os.path.basename(video_path),
            'status': 'processing',
            'start_time': datetime.now().isoformat(),
            'operations': {}
        }
        
        try:
            # Import processing modules
            from detect_persons import detect_persons_yolo, detect_persons_opencv
            from detect_anomalies import detect_anomalies_motion
            from extract_frames import extract_frames
            
            # Person detection
            if 'detection' in operations:
                try:
                    output_file = f"annotations/person_detections_{os.path.basename(video_path).replace('.mp4', '')}.json"
                    detect_persons_yolo(video_path, output_file=output_file)
                    result['operations']['detection'] = 'completed'
                except Exception as e:
                    result['operations']['detection'] = f'error: {str(e)}'
            
            # Anomaly detection
            if 'anomaly' in operations:
                try:
                    output_file = f"annotations/anomalies_{os.path.basename(video_path).replace('.mp4', '')}.json"
                    detect_anomalies_motion(video_path, output_file=output_file)
                    result['operations']['anomaly'] = 'completed'
                except Exception as e:
                    result['operations']['anomaly'] = f'error: {str(e)}'
            
            # Frame extraction
            if 'frames' in operations:
                try:
                    output_dir = f"frames/extracted_frames_{os.path.basename(video_path).replace('.mp4', '')}"
                    extract_frames(video_path, output_dir=output_dir, interval=30)
                    result['operations']['frames'] = 'completed'
                except Exception as e:
                    result['operations']['frames'] = f'error: {str(e)}'
            
            result['status'] = 'completed'
            result['end_time'] = datetime.now().isoformat()
            
        except Exception as e:
            result['status'] = 'failed'
            result['error'] = str(e)
            result['end_time'] = datetime.now().isoformat()
            self.errors.append(result)
        
        return result
    
    def process_batch(self, video_paths, operations=['detection', 'anomaly', 'frames']):
        """
        Process multiple videos in parallel.
        
        Args:
            video_paths: List of video file paths
            operations: List of operations to perform on each video
        """
        print(f"Starting batch processing of {len(video_paths)} videos...")
        print(f"Operations: {', '.join(operations)}")
        print(f"Max workers: {self.max_workers}\n")
        
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Submit all tasks
            future_to_video = {
                executor.submit(self.process_video, video_path, operations): video_path
                for video_path in video_paths
            }
            
            # Process completed tasks
            completed = 0
            for future in as_completed(future_to_video):
                video_path = future_to_video[future]
                try:
                    result = future.result()
                    self.results.append(result)
                    completed += 1
                    
                    status_icon = "✓" if result['status'] == 'completed' else "✗"
                    print(f"{status_icon} [{completed}/{len(video_paths)}] {os.path.basename(video_path)} - {result['status']}")
                except Exception as e:
                    error_result = {
                        'video_path': video_path,
                        'status': 'failed',
                        'error': str(e)
                    }
                    self.errors.append(error_result)
                    completed += 1
                    print(f"✗ [{completed}/{len(video_paths)}] {os.path.basename(video_path)} - failed: {str(e)}")
        
        return self.generate_report()
    
    def generate_report(self):
        """Generate processing report."""
        total = len(self.results) + len(self.errors)
        completed = len([r for r in self.results if r.get('status') == 'completed'])
        failed = len(self.errors)
        
        report = {
            'summary': {
                'total_videos': total,
                'completed': completed,
                'failed': failed,
                'success_rate': round((completed / total * 100) if total > 0 else 0, 2)
            },
            'results': self.results,
            'errors': self.errors,
            'timestamp': datetime.now().isoformat()
        }
        
        # Save report
        report_file = f"output/batch_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        os.makedirs('output', exist_ok=True)
        
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        print("\n" + "=" * 60)
        print("Batch Processing Report")
        print("=" * 60)
        print(f"Total Videos: {total}")
        print(f"Completed: {completed}")
        print(f"Failed: {failed}")
        print(f"Success Rate: {report['summary']['success_rate']}%")
        print(f"Report saved to: {report_file}")
        print("=" * 60)
        
        return report


def find_videos(directory='videos', extensions=['.mp4', '.avi', '.mov', '.mkv']):
    """Find all video files in directory."""
    video_paths = []
    
    if os.path.exists(directory):
        for root, dirs, files in os.walk(directory):
            for file in files:
                if any(file.lower().endswith(ext) for ext in extensions):
                    video_paths.append(os.path.join(root, file))
    
    return video_paths


def main():
    parser = argparse.ArgumentParser(description='Batch process surveillance videos')
    parser.add_argument('--directory', '-d', default='videos', help='Directory containing videos')
    parser.add_argument('--operations', '-o', nargs='+', 
                       choices=['detection', 'anomaly', 'frames', 'all'],
                       default=['all'],
                       help='Operations to perform')
    parser.add_argument('--workers', '-w', type=int, default=4, 
                       help='Number of parallel workers')
    parser.add_argument('--videos', '-v', nargs='+', help='Specific video files to process')
    
    args = parser.parse_args()
    
    # Determine operations
    if 'all' in args.operations:
        operations = ['detection', 'anomaly', 'frames']
    else:
        operations = args.operations
    
    # Get video paths
    if args.videos:
        video_paths = [v if os.path.exists(v) else os.path.join(args.directory, v) 
                      for v in args.videos]
    else:
        video_paths = find_videos(args.directory)
    
    if not video_paths:
        print(f"No videos found in {args.directory}")
        return
    
    # Process batch
    processor = BatchProcessor(max_workers=args.workers)
    processor.process_batch(video_paths, operations)


if __name__ == '__main__':
    main()

