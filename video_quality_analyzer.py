# Project: Surveillance Video Dataset
# Author: Molla Samser
# Website: https://rskworld.in/
# Contact: help@rskworld.in
# Phone: +91 93305 39277
# Address: Nutanhat, Mongolkote, Purba Burdwan, West Bengal, India, 713147

"""
Advanced video quality analysis tool.
Analyzes video quality metrics including sharpness, brightness, contrast, noise, and stability.
"""

import cv2
import numpy as np
import json
import os
from pathlib import Path
import argparse
from datetime import datetime


class VideoQualityAnalyzer:
    """Analyze video quality metrics."""
    
    def __init__(self):
        self.metrics = {}
    
    def analyze_sharpness(self, frame):
        """Calculate frame sharpness using Laplacian variance."""
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
        return laplacian_var
    
    def analyze_brightness(self, frame):
        """Calculate average brightness."""
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        return np.mean(gray)
    
    def analyze_contrast(self, frame):
        """Calculate contrast using standard deviation."""
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        return np.std(gray)
    
    def analyze_noise(self, frame):
        """Estimate noise level."""
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # Use median filter to estimate noise
        filtered = cv2.medianBlur(gray, 5)
        noise = np.mean(np.abs(gray.astype(float) - filtered.astype(float)))
        return noise
    
    def analyze_color_balance(self, frame):
        """Analyze color balance."""
        b, g, r = cv2.split(frame)
        return {
            'blue': np.mean(b),
            'green': np.mean(g),
            'red': np.mean(r),
            'balance': np.std([np.mean(b), np.mean(g), np.mean(r)])
        }
    
    def analyze_frame_stability(self, frame1, frame2):
        """Analyze frame-to-frame stability using optical flow."""
        gray1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
        
        flow = cv2.calcOpticalFlowFarneback(gray1, gray2, None, 0.5, 3, 15, 3, 5, 1.2, 0)
        magnitude = np.sqrt(flow[..., 0]**2 + flow[..., 1]**2)
        
        return {
            'avg_motion': np.mean(magnitude),
            'max_motion': np.max(magnitude),
            'stability_score': 100 - min(100, np.mean(magnitude) * 10)
        }
    
    def analyze_video(self, video_path, sample_frames=30):
        """
        Analyze video quality comprehensively.
        
        Args:
            video_path: Path to video file
            sample_frames: Number of frames to sample for analysis
        """
        cap = cv2.VideoCapture(video_path)
        
        if not cap.isOpened():
            return {'error': 'Could not open video file'}
        
        # Get video properties
        fps = cap.get(cv2.CAP_PROP_FPS)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        duration = total_frames / fps if fps > 0 else 0
        
        # Sample frames evenly
        frame_indices = np.linspace(0, total_frames - 1, sample_frames, dtype=int)
        
        sharpness_scores = []
        brightness_scores = []
        contrast_scores = []
        noise_scores = []
        color_balances = []
        stability_scores = []
        
        prev_frame = None
        frame_count = 0
        
        print(f"Analyzing video: {os.path.basename(video_path)}")
        print(f"Sampling {sample_frames} frames from {total_frames} total frames...")
        
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            
            if frame_count in frame_indices:
                # Analyze frame
                sharpness_scores.append(self.analyze_sharpness(frame))
                brightness_scores.append(self.analyze_brightness(frame))
                contrast_scores.append(self.analyze_contrast(frame))
                noise_scores.append(self.analyze_noise(frame))
                color_balances.append(self.analyze_color_balance(frame))
                
                # Analyze stability
                if prev_frame is not None:
                    stability = self.analyze_frame_stability(prev_frame, frame)
                    stability_scores.append(stability['stability_score'])
                
                prev_frame = frame.copy()
            
            frame_count += 1
        
        cap.release()
        
        # Calculate overall metrics
        overall_sharpness = np.mean(sharpness_scores)
        overall_brightness = np.mean(brightness_scores)
        overall_contrast = np.mean(contrast_scores)
        overall_noise = np.mean(noise_scores)
        overall_stability = np.mean(stability_scores) if stability_scores else 0
        
        # Normalize scores (0-100)
        sharpness_score = min(100, (overall_sharpness / 500) * 100)
        brightness_score = min(100, abs(overall_brightness - 128) / 128 * 100)
        contrast_score = min(100, (overall_contrast / 50) * 100)
        noise_score = max(0, 100 - (overall_noise / 10) * 100)
        
        # Overall quality score
        quality_score = (sharpness_score * 0.3 + 
                        brightness_score * 0.2 + 
                        contrast_score * 0.2 + 
                        noise_score * 0.2 + 
                        overall_stability * 0.1)
        
        # Determine quality level
        if quality_score >= 80:
            quality_level = 'Excellent'
        elif quality_score >= 60:
            quality_level = 'Good'
        elif quality_score >= 40:
            quality_level = 'Fair'
        else:
            quality_level = 'Poor'
        
        results = {
            'video_path': video_path,
            'filename': os.path.basename(video_path),
            'properties': {
                'resolution': f"{width}x{height}",
                'width': width,
                'height': height,
                'fps': fps,
                'total_frames': total_frames,
                'duration': round(duration, 2)
            },
            'quality_metrics': {
                'overall_score': round(quality_score, 2),
                'quality_level': quality_level,
                'sharpness': round(sharpness_score, 2),
                'brightness': round(brightness_score, 2),
                'contrast': round(contrast_score, 2),
                'noise': round(noise_score, 2),
                'stability': round(overall_stability, 2)
            },
            'detailed_metrics': {
                'avg_sharpness': round(overall_sharpness, 2),
                'avg_brightness': round(overall_brightness, 2),
                'avg_contrast': round(overall_contrast, 2),
                'avg_noise': round(overall_noise, 2)
            },
            'timestamp': datetime.now().isoformat()
        }
        
        return results
    
    def analyze_batch(self, video_paths):
        """Analyze multiple videos."""
        results = []
        
        for video_path in video_paths:
            result = self.analyze_video(video_path)
            if 'error' not in result:
                results.append(result)
        
        return results


def main():
    parser = argparse.ArgumentParser(description='Analyze video quality')
    parser.add_argument('video_path', help='Path to video file or directory')
    parser.add_argument('--output', '-o', default='output/quality_report.json',
                      help='Output file for quality report')
    parser.add_argument('--sample-frames', '-s', type=int, default=30,
                      help='Number of frames to sample')
    parser.add_argument('--batch', '-b', action='store_true',
                      help='Process all videos in directory')
    
    args = parser.parse_args()
    
    analyzer = VideoQualityAnalyzer()
    os.makedirs('output', exist_ok=True)
    
    if args.batch or os.path.isdir(args.video_path):
        # Batch processing
        video_dir = args.video_path if os.path.isdir(args.video_path) else 'videos'
        video_paths = []
        
        for ext in ['.mp4', '.avi', '.mov', '.mkv']:
            video_paths.extend(Path(video_dir).glob(f'*{ext}'))
        
        print(f"Found {len(video_paths)} videos to analyze")
        results = analyzer.analyze_batch([str(p) for p in video_paths])
    else:
        # Single video
        result = analyzer.analyze_video(args.video_path, args.sample_frames)
        results = [result] if 'error' not in result else []
    
    # Save results
    if results:
        with open(args.output, 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"\nQuality analysis complete!")
        print(f"Results saved to: {args.output}")
        
        # Print summary
        print("\n" + "=" * 60)
        print("Quality Analysis Summary")
        print("=" * 60)
        for result in results:
            print(f"\n{result['filename']}:")
            print(f"  Overall Score: {result['quality_metrics']['overall_score']}/100")
            print(f"  Quality Level: {result['quality_metrics']['quality_level']}")
            print(f"  Resolution: {result['properties']['resolution']}")
            print(f"  FPS: {result['properties']['fps']}")


if __name__ == '__main__':
    main()

