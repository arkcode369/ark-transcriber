#!/usr/bin/env python3
"""
Process YouTube Playlist manually
Extract video IDs from playlist and process each one
"""

import asyncio
import json
import sys
from pathlib import Path

# Playlist ID from user
PLAYLIST_ID = "PLo_kZR9jsafgVXE75C33_cZilf27LN8IA"
PLAYLIST_URL = f"https://youtube.com/playlist?list={PLAYLIST_ID}"

# Sample video IDs (replace with actual IDs from the playlist)
# You can extract these by:
# 1. Opening the playlist in browser
# 2. Right-click -> View Page Source
# 3. Search for "videoId" or "watch?v="
# Or use YouTube Data API
SAMPLE_VIDEO_IDS = [
    # Add video IDs here manually
    # Example: "abc123DEF45", "xyz789GHI01", etc.
]

async def process_video(video_id: str, api_url: str = "http://localhost:8000"):
    """Process a single video"""
    import httpx
    
    async with httpx.AsyncClient(timeout=120.0) as client:
        try:
            response = await client.post(
                f"{api_url}/transcribe",
                json={
                    "url": f"https://youtu.be/{video_id}",
                    "generate_summary": True,
                    "summary_language": "id",
                    "generate_diagrams": True
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Processed: {video_id}")
                return data
            else:
                print(f"❌ Failed: {video_id} - {response.text}")
                return None
                
        except Exception as e:
            print(f"❌ Error processing {video_id}: {str(e)}")
            return None

async def main():
    """Main function"""
    print("=" * 60)
    print("Processing Playlist:", PLAYLIST_ID)
    print("Playlist URL:", PLAYLIST_URL)
    print("=" * 60)
    
    if not SAMPLE_VIDEO_IDS:
        print("\n⚠️  No video IDs found!")
        print("\nTo process this playlist:")
        print("1. Open the playlist in your browser")
        print("2. Extract video IDs from URLs (watch?v=XXXXX)")
        print("3. Add them to SAMPLE_VIDEO_IDS list in this script")
        print("4. Run: python3 process_playlist.py")
        print("\nExample video ID format: abc123DEF45 (11 characters)")
        return
    
    print(f"\n📹 Found {len(SAMPLE_VIDEO_IDS)} videos to process\n")
    
    results = []
    for i, video_id in enumerate(SAMPLE_VIDEO_IDS, 1):
        print(f"[{i}/{len(SAMPLE_VIDEO_IDS)}] Processing {video_id}...")
        result = await process_video(video_id)
        if result:
            results.append(result)
        # Small delay to avoid rate limiting
        await asyncio.sleep(2)
    
    print("\n" + "=" * 60)
    print(f"✅ Completed: {len(results)}/{len(SAMPLE_VIDEO_IDS)} videos")
    print("=" * 60)
    
    # Save results
    output_file = Path(f"playlist_{PLAYLIST_ID}_results.json")
    with open(output_file, "w") as f:
        json.dump({
            "playlist_id": PLAYLIST_ID,
            "playlist_url": PLAYLIST_URL,
            "processed_count": len(results),
            "total_videos": len(SAMPLE_VIDEO_IDS),
            "results": results
        }, f, indent=2)
    
    print(f"\n📄 Results saved to: {output_file}")
    print("\n📁 All transcripts saved to:")
    print("   ark-intelligent/.agents/docs/transcripts/youtube/")

if __name__ == "__main__":
    asyncio.run(main())
