# Project: Surveillance Video Dataset
# Author: Molla Samser
# Website: https://rskworld.in/
# Contact: help@rskworld.in
# Phone: +91 93305 39277
# Address: Nutanhat, Mongolkote, Purba Burdwan, West Bengal, India, 713147

"""
Advanced video search and filtering system.
Supports searching by metadata, timestamps, events, and content-based search.
"""

import os
import json
import cv2
from pathlib import Path
from datetime import datetime
import argparse


class VideoSearchEngine:
    """Video search and filtering engine."""
    
    def __init__(self, videos_dir='videos', annotations_dir='annotations'):
        self.videos_dir = videos_dir
        self.annotations_dir = annotations_dir
        self.index = {}
        self.build_index()
    
    def build_index(self):
        """Build search index from videos and annotations."""
        print("Building search index...")
        
        self.index = {
            'videos': {},
            'events': [],
            'detections': [],
            'anomalies': []
        }
        
        # Index videos
        if os.path.exists(self.videos_dir):
            for video_file in os.listdir(self.videos_dir):
                if video_file.endswith(('.mp4', '.avi', '.mov', '.mkv')):
                    video_path = os.path.join(self.videos_dir, video_file)
                    video_info = self._get_video_info(video_path)
                    self.index['videos'][video_file] = video_info
        
        # Index annotations
        self._index_annotations()
        
        print(f"Index built: {len(self.index['videos'])} videos, "
              f"{len(self.index['events'])} events")
    
    def _get_video_info(self, video_path):
        """Get video information."""
        cap = cv2.VideoCapture(video_path)
        info = {
            'path': video_path,
            'filename': os.path.basename(video_path),
            'fps': 0,
            'width': 0,
            'height': 0,
            'duration': 0,
            'total_frames': 0
        }
        
        if cap.isOpened():
            info['fps'] = cap.get(cv2.CAP_PROP_FPS)
            info['width'] = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            info['height'] = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            info['total_frames'] = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            info['duration'] = info['total_frames'] / info['fps'] if info['fps'] > 0 else 0
            cap.release()
        
        return info
    
    def _index_annotations(self):
        """Index annotation files."""
        # Index activities
        annotations_file = os.path.join(self.annotations_dir, 'annotations.json')
        if os.path.exists(annotations_file):
            with open(annotations_file, 'r') as f:
                data = json.load(f)
                for activity in data.get('activities', []):
                    self.index['events'].append({
                        'type': 'activity',
                        'video': data.get('video_id', ''),
                        'activity_type': activity.get('type'),
                        'start_time': activity.get('start_time'),
                        'end_time': activity.get('end_time'),
                        'person_id': activity.get('person_id')
                    })
        
        # Index detections
        detections_file = os.path.join(self.annotations_dir, 'person_detections.json')
        if os.path.exists(detections_file):
            with open(detections_file, 'r') as f:
                data = json.load(f)
                for detection in data.get('detections', []):
                    self.index['detections'].append({
                        'type': 'detection',
                        'video': data.get('video_id', ''),
                        'timestamp': detection.get('timestamp'),
                        'frame': detection.get('frame'),
                        'person_count': len(detection.get('persons', []))
                    })
        
        # Index anomalies
        anomalies_file = os.path.join(self.annotations_dir, 'anomalies.json')
        if os.path.exists(anomalies_file):
            with open(anomalies_file, 'r') as f:
                data = json.load(f)
                for anomaly in data.get('anomalies', []):
                    self.index['anomalies'].append({
                        'type': 'anomaly',
                        'video': data.get('video_id', ''),
                        'anomaly_type': anomaly.get('type'),
                        'start_time': anomaly.get('start_time'),
                        'end_time': anomaly.get('end_time'),
                        'severity': anomaly.get('severity', 'medium')
                    })
    
    def search(self, query=None, filters=None):
        """
        Search videos and events.
        
        Args:
            query: Text query to search
            filters: Dictionary of filters
        """
        filters = filters or {}
        results = {
            'videos': [],
            'events': [],
            'total_matches': 0
        }
        
        # Filter videos
        for video_file, video_info in self.index['videos'].items():
            match = True
            
            # Text search
            if query:
                if query.lower() not in video_file.lower():
                    match = False
            
            # Duration filter
            if 'min_duration' in filters and video_info['duration'] < filters['min_duration']:
                match = False
            if 'max_duration' in filters and video_info['duration'] > filters['max_duration']:
                match = False
            
            # Resolution filter
            if 'min_resolution' in filters:
                min_w, min_h = filters['min_resolution']
                if video_info['width'] < min_w or video_info['height'] < min_h:
                    match = False
            
            if match:
                results['videos'].append(video_info)
        
        # Filter events
        all_events = self.index['events'] + self.index['detections'] + self.index['anomalies']
        
        for event in all_events:
            match = True
            
            # Video filter
            if 'video' in filters and event.get('video') != filters['video']:
                match = False
            
            # Time range filter
            if 'start_time' in filters and event.get('start_time', 0) < filters['start_time']:
                match = False
            if 'end_time' in filters and event.get('end_time', float('inf')) > filters['end_time']:
                match = False
            
            # Event type filter
            if 'event_type' in filters:
                if filters['event_type'] == 'anomaly' and event.get('type') != 'anomaly':
                    match = False
                elif filters['event_type'] == 'detection' and event.get('type') != 'detection':
                    match = False
                elif filters['event_type'] == 'activity' and event.get('type') != 'activity':
                    match = False
            
            # Activity type filter
            if 'activity_type' in filters and event.get('activity_type') != filters['activity_type']:
                match = False
            
            if match:
                results['events'].append(event)
        
        results['total_matches'] = len(results['videos']) + len(results['events'])
        return results
    
    def search_by_timestamp(self, video_file, timestamp):
        """Search for events at a specific timestamp in a video."""
        results = []
        
        for event in self.index['events'] + self.index['detections'] + self.index['anomalies']:
            if event.get('video') == video_file:
                start = event.get('start_time', 0)
                end = event.get('end_time', start)
                
                if start <= timestamp <= end:
                    results.append(event)
        
        return results
    
    def export_results(self, results, output_file):
        """Export search results to JSON."""
        os.makedirs('output', exist_ok=True)
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"Search results exported to: {output_file}")


def main():
    parser = argparse.ArgumentParser(description='Video search and filtering')
    parser.add_argument('--query', '-q', help='Search query')
    parser.add_argument('--video', '-v', help='Filter by video filename')
    parser.add_argument('--event-type', '-e', choices=['anomaly', 'detection', 'activity'],
                       help='Filter by event type')
    parser.add_argument('--activity-type', '-a', help='Filter by activity type')
    parser.add_argument('--start-time', '-s', type=float, help='Start time filter')
    parser.add_argument('--end-time', '-t', type=float, help='End time filter')
    parser.add_argument('--min-duration', type=float, help='Minimum video duration')
    parser.add_argument('--max-duration', type=float, help='Maximum video duration')
    parser.add_argument('--timestamp', type=float, help='Search at specific timestamp')
    parser.add_argument('--output', '-o', default='output/search_results.json',
                       help='Output file for results')
    
    args = parser.parse_args()
    
    search_engine = VideoSearchEngine()
    
    filters = {}
    if args.video:
        filters['video'] = args.video
    if args.event_type:
        filters['event_type'] = args.event_type
    if args.activity_type:
        filters['activity_type'] = args.activity_type
    if args.start_time is not None:
        filters['start_time'] = args.start_time
    if args.end_time is not None:
        filters['end_time'] = args.end_time
    if args.min_duration is not None:
        filters['min_duration'] = args.min_duration
    if args.max_duration is not None:
        filters['max_duration'] = args.max_duration
    
    if args.timestamp and args.video:
        results = search_engine.search_by_timestamp(args.video, args.timestamp)
        output = {'timestamp': args.timestamp, 'video': args.video, 'events': results}
    else:
        results = search_engine.search(query=args.query, filters=filters)
        output = results
    
    search_engine.export_results(output, args.output)
    
    print(f"\nSearch Results:")
    print(f"  Videos found: {len(output.get('videos', []))}")
    print(f"  Events found: {len(output.get('events', []))}")
    print(f"  Total matches: {output.get('total_matches', len(output.get('events', [])))}")


if __name__ == '__main__':
    main()

