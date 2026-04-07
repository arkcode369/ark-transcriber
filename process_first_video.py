#!/usr/bin/env python3
"""
Process first valid video from playlist
"""
import asyncio
import httpx
import json
from pathlib import Path

# Valid video IDs from the playlist (manually filtered)
# These look like actual YouTube video IDs
VALID_VIDEO_IDS = [
    "paXIlCxzfSW",
    "uJi393dAaCN", 
    "rEmedjUJIj3",
    "0w7vmO1i4Gk",
    "D9ku7dc5bOP",
    "dcYRmIcQfda",
    "0igP5FUl8Kj",
    "CD0QxjQYYSI",
    "AOn4CLCHDGp",
    "AOn4CLAWUCn",
    "CPYDEI5iIhP"
]

async def process_video(video_id: str, api_url: str = "http://localhost:8000"):
    """Process a single video"""
    async with httpx.AsyncClient(timeout=180.0) as client:
        try:
            print(f"🔄 Processing: {video_id}")
            
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
                print(f"✅ Success: {video_id}")
                return data
            else:
                print(f"❌ Failed: {video_id} - {response.text[:200]}")
                return None
                
        except Exception as e:
            print(f"❌ Error processing {video_id}: {str(e)}")
            return None

async def main():
    """Process first 3 videos from playlist"""
    playlist_id = "PLo_kZR9jsafgVXE75C33_cZilf27LN8IA"
    
    print("=" * 60)
    print(f"Processing Playlist: {playlist_id}")
    print(f"Processing first 3 videos...")
    print("=" * 60)
    
    # Process first 3 videos
    videos_to_process = VALID_VIDEO_IDS[:3]
    results = []
    
    for i, video_id in enumerate(videos_to_process, 1):
        print(f"\n[{i}/{len(videos_to_process)}] Processing {video_id}...")
        result = await process_video(video_id)
        if result:
            results.append({
                "video_id": video_id,
                "result": result
            })
        # Delay to avoid rate limiting
        await asyncio.sleep(3)
    
    print("\n" + "=" * 60)
    print(f"✅ Completed: {len(results)}/{len(videos_to_process)} videos")
    print("=" * 60)
    
    # Save results
    output_file = Path(f"playlist_{playlist_id}_first3.json")
    with open(output_file, "w") as f:
        json.dump({
            "playlist_id": playlist_id,
            "processed_count": len(results),
            "videos": results
        }, f, indent=2)
    
    print(f"\n📄 Results saved to: {output_file}")
    print("\n📁 Transcripts saved to:")
    print("   ark-intelligent/.agents/docs/transcripts/youtube/")
    
    # List saved files
    transcripts_dir = Path("/workspace/main/ark-intelligent/.agents/docs/transcripts/youtube")
    if transcripts_dir.exists():
        dirs = [d for d in transcripts_dir.iterdir() if d.is_dir() and not d.name == 'templates']
        print(f"\n📂 Found {len(dirs)} video directories:")
        for d in dirs[-3:]:  # Show last 3
            print(f"   - {d.name}")

if __name__ == "__main__":
    asyncio.run(main())
