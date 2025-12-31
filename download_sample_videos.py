# Project: Surveillance Video Dataset
# Author: Molla Samser
# Website: https://rskworld.in/
# Contact: help@rskworld.in
# Phone: +91 93305 39277
# Address: Nutanhat, Mongolkote, Purba Burdwan, West Bengal, India, 713147

"""
Script to download sample surveillance videos from public sources.
This provides an alternative to creating synthetic videos.
"""

import os
import urllib.request
from pathlib import Path


def download_sample_video(url, output_path):
    """
    Download a video from URL.
    
    Args:
        url: URL of the video to download
        output_path: Path to save the video
    """
    try:
        os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else '.', exist_ok=True)
        
        print(f"Downloading video from: {url}")
        print(f"Saving to: {output_path}")
        
        urllib.request.urlretrieve(url, output_path)
        
        file_size = os.path.getsize(output_path) / (1024 * 1024)
        print(f"Download complete! File size: {file_size:.2f} MB")
        return True
    except Exception as e:
        print(f"Error downloading video: {e}")
        return False


def get_sample_video_sources():
    """
    Returns list of sample video sources (public domain or free to use).
    Note: Replace these with actual URLs to sample surveillance videos.
    """
    return [
        {
            "name": "sample.mp4",
            "url": "https://sample-videos.com/video123/mp4/720/big_buck_bunny_720p_1mb.mp4",
            "description": "Sample video 1 (replace with actual surveillance video URL)"
        },
        {
            "name": "sample2.mp4",
            "url": "https://sample-videos.com/video123/mp4/720/big_buck_bunny_720p_2mb.mp4",
            "description": "Sample video 2 (replace with actual surveillance video URL)"
        }
    ]


if __name__ == "__main__":
    print("=" * 60)
    print("Sample Video Downloader")
    print("=" * 60)
    print("\nNote: This script requires actual video URLs.")
    print("Replace the URLs in get_sample_video_sources() with real surveillance video links.")
    print("\nAlternatively, use create_sample_video.py to generate synthetic videos.")
    print("=" * 60)
    
    # Uncomment to download (after adding real URLs):
    # sources = get_sample_video_sources()
    # for source in sources:
    #     output_path = f"videos/{source['name']}"
    #     download_sample_video(source['url'], output_path)

