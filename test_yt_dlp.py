#!/usr/bin/env python3
"""
Test yt-dlp for transcript extraction
"""
import subprocess
import json
import sys

VIDEO_URL = "https://youtu.be/C90xGr3kW8Y"

def extract_transcript(url):
    """Try to extract transcript using yt-dlp"""
    try:
        # Try to get transcript data
        cmd = [
            "yt-dlp",
            "--dump-json",
            "--no-download",
            "--write-auto-srt",
            "--skip-download",
            url
        ]
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=60
        )
        
        print("STDOUT:", result.stdout[:500] if result.stdout else "None")
        print("STDERR:", result.stderr[:500] if result.stderr else "None")
        
        # Check if SRT file was created
        import os
        srt_file = url.split("/")[-1] + ".id.srt"
        if os.path.exists(srt_file):
            print(f"✅ Found transcript file: {srt_file}")
            with open(srt_file, 'r') as f:
                print(f.read()[:500])
            return True
        else:
            print("❌ No transcript file created")
            return False
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

if __name__ == "__main__":
    print(f"Testing transcript extraction for: {VIDEO_URL}")
    extract_transcript(VIDEO_URL)
