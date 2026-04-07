#!/usr/bin/env python3
"""
Extract video IDs from YouTube playlist by scraping
"""
import re
import httpx
from bs4 import BeautifulSoup

PLAYLIST_ID = "PLo_kZR9jsafgVXE75C33_cZilf27LN8IA"
PLAYLIST_URL = f"https://www.youtube.com/playlist?list={PLAYLIST_ID}"

def extract_video_ids():
    """Extract video IDs from playlist page"""
    print(f"Fetching playlist: {PLAYLIST_URL}")
    
    try:
        with httpx.Client(timeout=30.0) as client:
            response = client.get(
                PLAYLIST_URL,
                headers={
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
                }
            )
            
            if response.status_code != 200:
                print(f"❌ Failed to fetch playlist: {response.status_code}")
                return []
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Try multiple patterns to find video IDs
            video_ids = set()
            
            # Pattern 1: Look in <a> tags with watch?v=
            for link in soup.find_all('a', href=True):
                href = link['href']
                if 'watch?v=' in href:
                    match = re.search(r'v=([a-zA-Z0-9_-]{11})', href)
                    if match:
                        video_ids.add(match.group(1))
            
            # Pattern 2: Look in script tags for JSON data
            for script in soup.find_all('script'):
                if script.string:
                    # Look for video IDs in various JSON patterns
                    ids = re.findall(r'"videoId":"([a-zA-Z0-9_-]{11})"', script.string)
                    video_ids.update(ids)
                    
                    # Also try without quotes
                    ids = re.findall(r'videoId[:\s]+["\']?([a-zA-Z0-9_-]{11})["\']?', script.string)
                    video_ids.update(ids)
            
            # Pattern 3: Look for standalone 11-char video ID patterns
            all_text = response.text
            potential_ids = re.findall(r'[a-zA-Z0-9_-]{11}', all_text)
            
            # Filter likely video IDs (YouTube IDs have specific characteristics)
            valid_chars = set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-')
            for pid in potential_ids:
                if all(c in valid_chars for c in pid):
                    # Skip common non-video IDs
                    if pid not in ['list', 'watch', 'feature', 'related', 'context', 'params']:
                        if len(pid) == 11:
                            video_ids.add(pid)
            
            # Remove duplicates and limit to reasonable number
            video_ids = list(video_ids)[:50]  # Limit to 50 to avoid false positives
            
            print(f"✅ Found {len(video_ids)} potential video IDs")
            
            # Filter out obvious non-video IDs
            filtered_ids = []
            for vid in video_ids:
                # Skip if it looks like a playlist ID or other non-video ID
                if not vid.startswith('PL') and not vid.startswith('UU') and not vid.startswith('MC'):
                    filtered_ids.append(vid)
            
            print(f"✅ Filtered to {len(filtered_ids)} likely video IDs")
            
            return filtered_ids[:20]  # Return first 20 to start
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return []

if __name__ == "__main__":
    video_ids = extract_video_ids()
    
    if video_ids:
        print("\n📹 Video IDs found:")
        for i, vid in enumerate(video_ids, 1):
            print(f"  {i}. {vid}")
        
        print(f"\n📝 To process these videos:")
        print(f"   python3 process_playlist.py")
        print(f"\nOr manually add to process_playlist.py SAMPLE_VIDEO_IDS list")
    else:
        print("\n⚠️  No video IDs found. YouTube may be using dynamic loading.")
        print("   Try getting YouTube Data API key for reliable playlist extraction.")
