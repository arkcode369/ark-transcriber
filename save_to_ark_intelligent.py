#!/usr/bin/env python3
"""
Save processed transcripts to ark-intelligent/.agents/docs/transcripts/
Format optimized for LLM indexing and retrieval
"""

import os
import json
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional
import hashlib

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Paths
ARK_INTELLIGENT_DOCS = Path("/workspace/main/ark-intelligent/.agents/docs")
TRANSCRIPTS_DIR = ARK_INTELLIGENT_DOCS / "transcripts"


def slugify(text: str) -> str:
    """Convert text to URL-friendly slug"""
    import re
    text = text.lower().strip()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[-\s]+', '-', text)
    return text[:50]  # Limit length


def save_youtube_playlist(
    playlist_id: str,
    title: str,
    videos: list,
    combined_summary: str,
    language: str = "id",
    total_duration: int = 0,
    source_url: str = ""
) -> Path:
    """Save YouTube playlist to ark-intelligent docs"""
    
    # Create directory structure
    playlist_dir = TRANSCRIPTS_DIR / "youtube" / playlist_id
    playlist_dir.mkdir(parents=True, exist_ok=True)
    
    videos_dir = playlist_dir / "videos"
    videos_dir.mkdir(parents=True, exist_ok=True)
    
    diagrams_dir = playlist_dir / "diagrams"
    diagrams_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate metadata
    now = datetime.utcnow()
    metadata = {
        "source_type": "youtube_playlist",
        "source_id": playlist_id,
        "title": title,
        "created_at": now.isoformat() + "Z",
        "language": language,
        "total_videos": len(videos),
        "total_duration_seconds": total_duration,
        "source_url": source_url,
        "video_ids": [v.get("video_id") for v in videos],
        "tags": extract_tags_from_summary(combined_summary),
        "processing_notes": f"Playlist with {len(videos)} videos"
    }
    
    # Save metadata.json
    with open(playlist_dir / "metadata.json", "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)
    
    # Save combined_summary.md
    combined_content = f"""# {title} - Combined Summary

**Source:** YouTube Playlist - {playlist_id}  
**Created:** {now.strftime('%Y-%m-%d %H:%M UTC')}  
**Language:** {language}  
**Total Videos:** {len(videos)}  
**Total Duration:** {total_duration} seconds

---

## Executive Summary

{combined_summary}

---

## Key Points

{generate_key_points(combined_summary)}

---

## Actionable Insights

{generate_actionable_insights(combined_summary)}

---

## Tags

{', '.join(metadata['tags'])}

---

## Individual Videos

{chr(10).join([f"- [Video {i+1}: {v.get('title', v.get('video_id'))}](./videos/{v.get('video_id')}/summary.md)" for i, v in enumerate(videos)])}

---

## Related Content

- [Full Combined Transcript](./transcript.md)
- [Diagrams](./diagrams/)

---

**Metadata:**
- Source URL: {source_url}
- Processed At: {now.isoformat()}Z
- Total Videos: {len(videos)}
- Total Duration: {total_duration} seconds
"""
    
    with open(playlist_dir / "combined_summary.md", "w", encoding="utf-8") as f:
        f.write(combined_content)
    
    # Save full transcript
    transcript_lines = []
    transcript_lines.append(f"# {title} - Full Combined Transcript\n")
    transcript_lines.append(f"**Source:** YouTube Playlist - {playlist_id}  \n")
    transcript_lines.append(f"**Created:** {now.strftime('%Y-%m-%d %H:%M UTC')}  \n")
    transcript_lines.append(f"**Language:** {language}\n")
    transcript_lines.append("\n---\n")
    transcript_lines.append("## All Videos Transcript\n")
    
    for i, v in enumerate(videos):
        transcript_lines.append(f"\n\n=== Video {i+1}: {v.get('video_id')} ===")
        transcript_lines.append(v.get('full_text', ''))
    
    transcript_lines.append("\n---\n")
    transcript_lines.append("## Metadata\n")
    transcript_lines.append(f"- **Source URL:** {source_url}\n")
    transcript_lines.append(f"- **Processed At:** {now.isoformat()}Z\n")
    transcript_lines.append(f"- **Total Videos:** {len(videos)}\n")
    transcript_lines.append(f"- **Total Duration:** {total_duration} seconds\n")
    
    transcript_content = "\n".join(transcript_lines)
    
    with open(playlist_dir / "transcript.md", "w", encoding="utf-8") as f:
        f.write(transcript_content)
    
    # Save individual video summaries
    for video in videos:
        video_id = video.get("video_id")
        if video_id:
            video_dir = videos_dir / video_id
            video_dir.mkdir(parents=True, exist_ok=True)
            
            # Save individual metadata
            video_metadata = {
                "source_type": "youtube",
                "source_id": video_id,
                "playlist_id": playlist_id,
                "title": video.get("title", f"Video {video_id}"),
                "created_at": now.isoformat() + "Z",
                "language": language,
                "duration_seconds": video.get("duration_seconds", 0),
                "tags": extract_tags_from_summary(video.get("summary", ""))
            }
            
            with open(video_dir / "metadata.json", "w", encoding="utf-8") as f:
                json.dump(video_metadata, f, indent=2, ensure_ascii=False)
            
            # Save individual transcript
            transcript_file = video_dir / "transcript.md"
            with open(transcript_file, "w", encoding="utf-8") as f:
                f.write(f"""# {video.get('title', video_id)}

**Source:** YouTube - {video_id}  
**Playlist:** {playlist_id}  
**Created:** {now.strftime('%Y-%m-%d %H:%M UTC')}  
**Language:** {language}  
**Duration:** {video.get('duration_seconds', 0)} seconds

---

## Full Transcript

{video.get('full_text', '')}

---

## Metadata
- **Source URL:** {video.get('source_url', '')}
- **Processed At:** {now.isoformat()}Z
""")
            
            # Save individual summary
            summary_file = video_dir / "summary.md"
            with open(summary_file, "w", encoding="utf-8") as f:
                f.write(f"""# {video.get('title', video_id)} - Summary

**Source:** YouTube - {video_id}  
**Playlist:** {playlist_id}  
**Created:** {now.strftime('%Y-%m-%d %H:%M UTC')}  
**Language:** {language}

---

## Executive Summary

{video.get('summary', 'No summary available')}

---

## Key Points

{generate_key_points(video.get('summary', ''))}

---

## Actionable Insights

{generate_actionable_insights(video.get('summary', ''))}

---

## Tags

{', '.join(video_metadata['tags'])}

---

## Related Content

- [Full Transcript](./transcript.md)

---

**Metadata:**
- Source URL: {video.get('source_url', '')}
- Processed At: {now.isoformat()}Z
""")
    
    logger.info(f"Saved YouTube playlist to: {playlist_dir}")
    return playlist_dir


def save_youtube_transcript(
    video_id: str,
    title: str,
    transcript_text: str,
    summary: str,
    diagrams: Dict[str, Any],
    language: str = "id",
    duration_seconds: int = 0,
    source_url: str = "",
    playlist_id: Optional[str] = None
) -> Path:
    """Save YouTube transcript to ark-intelligent docs"""
    
    # If part of playlist, save to playlist directory
    if playlist_id:
        # This will be handled by save_youtube_playlist
        return TRANSCRIPTS_DIR / "youtube" / playlist_id / "videos" / video_id
    
    # Create directory structure for standalone video
    video_dir = TRANSCRIPTS_DIR / "youtube" / video_id
    video_dir.mkdir(parents=True, exist_ok=True)
    
    diagrams_dir = video_dir / "diagrams"
    diagrams_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate metadata
    now = datetime.utcnow()
    metadata = {
        "source_type": "youtube",
        "source_id": video_id,
        "title": title,
        "created_at": now.isoformat() + "Z",
        "language": language,
        "duration_seconds": duration_seconds,
        "source_url": source_url,
        "tags": extract_tags_from_summary(summary),
        "processing_notes": "YouTube transcript"
    }
    
    # Save metadata.json
    with open(video_dir / "metadata.json", "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)
    
    # Save transcript.md
    transcript_content = f"""# {title}

**Source Type:** YouTube  
**Video ID:** {video_id}  
**Created:** {now.strftime('%Y-%m-%d %H:%M UTC')}  
**Language:** {language}  
**Duration:** {duration_seconds} seconds

---

## Full Transcript

{transcript_text}

---

## Metadata
- **Source URL:** {source_url}
- **Processed At:** {now.isoformat()}Z
- **Duration:** {duration_seconds} seconds
"""
    
    with open(video_dir / "transcript.md", "w", encoding="utf-8") as f:
        f.write(transcript_content)
    
    # Save summary.md
    summary_content = f"""# {title} - Summary

**Source:** YouTube - {video_id}  
**Created:** {now.strftime('%Y-%m-%d %H:%M UTC')}  
**Language:** {language}

---

## Executive Summary

{summary}

---

## Key Points

{generate_key_points(summary)}

---

## Actionable Insights

{generate_actionable_insights(summary)}

---

## Tags

{', '.join(metadata['tags'])}

---

## Related Content

- [Full Transcript](./transcript.md)
- [Diagrams](./diagrams/)

---

**Metadata:**
- Source URL: {source_url}
- Processed At: {now.isoformat()}Z
"""
    
    with open(video_dir / "summary.md", "w", encoding="utf-8") as f:
        f.write(summary_content)
    
    # Save diagrams
    if diagrams:
        if "flowchart" in diagrams:
            with open(diagrams_dir / "flowchart.md", "w", encoding="utf-8") as f:
                f.write(f"# Flowchart Diagram\n\n```mermaid\n{diagrams['flowchart']}\n```\n")
        
        if "mindmap" in diagrams:
            with open(diagrams_dir / "mindmap.md", "w", encoding="utf-8") as f:
                f.write(f"# Mindmap Diagram\n\n```mermaid\n{diagrams['mindmap']}\n```\n")
        
        if "timeline" in diagrams:
            with open(diagrams_dir / "timeline.md", "w", encoding="utf-8") as f:
                f.write(f"# Timeline Diagram\n\n```mermaid\n{diagrams['timeline']}\n```\n")
    
    logger.info(f"Saved YouTube transcript to: {video_dir}")
    return video_dir


def save_pdf_transcript(
    filename: str,
    full_text: str,
    summary: str,
    diagrams: Dict[str, Any],
    language: str = "id",
    total_pages: int = 0,
    text_pages: int = 0,
    image_pages: int = 0,
    ocr_used: bool = False,
    ocr_pages: int = 0,
    source_url: str = ""
) -> Path:
    """Save PDF transcript to ark-intelligent docs"""
    
    # Create slug from filename
    slug = slugify(filename.replace(".pdf", ""))
    pdf_dir = TRANSCRIPTS_DIR / "pdf" / slug
    pdf_dir.mkdir(parents=True, exist_ok=True)
    
    diagrams_dir = pdf_dir / "diagrams"
    diagrams_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate metadata
    now = datetime.utcnow()
    metadata = {
        "source_type": "pdf",
        "source_id": filename,
        "title": filename.replace(".pdf", ""),
        "created_at": now.isoformat() + "Z",
        "language": language,
        "page_count": total_pages,
        "text_pages": text_pages,
        "image_pages": image_pages,
        "source_url": source_url,
        "tags": extract_tags_from_summary(summary),
        "processing_notes": f"OCR used: {ocr_used}, OCR pages: {ocr_pages}"
    }
    
    # Save metadata.json
    with open(pdf_dir / "metadata.json", "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)
    
    # Save full_text.md
    text_content = f"""# {filename}

**Source Type:** PDF  
**Filename:** {filename}  
**Created:** {now.strftime('%Y-%m-%d %H:%M UTC')}  
**Language:** {language}  
**Pages:** {total_pages} (Text: {text_pages}, Images: {image_pages})

---

## Full Extracted Text

{full_text}

---

## Metadata
- **Source URL:** {source_url}
- **Processed At:** {now.isoformat()}Z
- **OCR Used:** {ocr_used}
- **OCR Pages:** {ocr_pages}
- **Total Pages:** {total_pages}
"""
    
    with open(pdf_dir / "full_text.md", "w", encoding="utf-8") as f:
        f.write(text_content)
    
    # Save summary.md
    summary_content = f"""# {filename} - Summary

**Source:** PDF - {filename}  
**Created:** {now.strftime('%Y-%m-%d %H:%M UTC')}  
**Language:** {language}

---

## Executive Summary

{summary}

---

## Key Points

{generate_key_points(summary)}

---

## Actionable Insights

{generate_actionable_insights(summary)}

---

## Tags

{', '.join(metadata['tags'])}

---

## Related Content

- [Full Text](./full_text.md)
- [Diagrams](./diagrams/)

---

**Metadata:**
- Source URL: {source_url}
- Processed At: {now.isoformat()}Z
- OCR Used: {ocr_used}
- OCR Pages: {ocr_pages}
- Total Pages: {total_pages}
"""
    
    with open(pdf_dir / "summary.md", "w", encoding="utf-8") as f:
        f.write(summary_content)
    
    # Save diagrams
    if diagrams:
        if "flowchart" in diagrams:
            with open(diagrams_dir / "flowchart.md", "w", encoding="utf-8") as f:
                f.write(f"# Flowchart Diagram\n\n```mermaid\n{diagrams['flowchart']}\n```\n")
        
        if "mindmap" in diagrams:
            with open(diagrams_dir / "mindmap.md", "w", encoding="utf-8") as f:
                f.write(f"# Mindmap Diagram\n\n```mermaid\n{diagrams['mindmap']}\n```\n")
        
        if "timeline" in diagrams:
            with open(diagrams_dir / "timeline.md", "w", encoding="utf-8") as f:
                f.write(f"# Timeline Diagram\n\n```mermaid\n{diagrams['timeline']}\n```\n")
    
    logger.info(f"Saved PDF transcript to: {pdf_dir}")
    return pdf_dir


def extract_tags_from_summary(summary: str) -> list:
    """Extract potential tags from summary (simple heuristic)"""
    # Common trading/education tags
    keywords = [
        "trading", "strategy", "risk", "management", "entry", "exit",
        "psychology", "discipline", "pattern", "indicator", "analysis",
        "market", "price", "volume", "trend", "reversal", "breakout"
    ]
    
    summary_lower = summary.lower()
    tags = []
    
    for keyword in keywords:
        if keyword in summary_lower:
            tags.append(keyword)
    
    # Add generic tags if none found
    if not tags:
        tags = ["general", "education"]
    
    return tags[:10]  # Limit to 10 tags


def generate_key_points(summary: str) -> str:
    """Generate key points section from summary"""
    # Simple heuristic: extract sentences
    sentences = [s.strip() for s in summary.replace('\n', ' ').split('.') if len(s.strip()) > 20]
    
    key_points = ""
    for i, sentence in enumerate(sentences[:5], 1):  # Top 5 points
        key_points += f"{i}. {sentence}.\n"
    
    return key_points if key_points else "- Key points will be extracted from summary"


def generate_actionable_insights(summary: str) -> str:
    """Generate actionable insights from summary"""
    # Simple heuristic
    insights = [
        "- Review the full transcript for detailed examples",
        "- Practice the strategies mentioned in simulated trading",
        "- Create a trading journal based on the rules learned",
        "- Set up alerts for the patterns discussed",
        "- Backtest the strategies on historical data"
    ]
    
    return "\n".join(insights)


def get_transcript_path(video_id: str, source_type: str = "youtube") -> Path:
    """Get path to existing transcript if it exists"""
    if source_type == "youtube":
        return TRANSCRIPTS_DIR / "youtube" / video_id
    else:
        return TRANSCRIPTS_DIR / "pdf" / video_id


def list_all_transcripts() -> list:
    """List all transcripts in the docs"""
    transcripts = []
    
    # YouTube transcripts
    youtube_dir = TRANSCRIPTS_DIR / "youtube"
    if youtube_dir.exists():
        for video_id in youtube_dir.iterdir():
            if video_id.is_dir():
                metadata_file = video_id / "metadata.json"
                if metadata_file.exists():
                    with open(metadata_file, "r") as f:
                        transcripts.append(json.load(f))
    
    # PDF transcripts
    pdf_dir = TRANSCRIPTS_DIR / "pdf"
    if pdf_dir.exists():
        for pdf_slug in pdf_dir.iterdir():
            if pdf_slug.is_dir():
                metadata_file = pdf_slug / "metadata.json"
                if metadata_file.exists():
                    with open(metadata_file, "r") as f:
                        transcripts.append(json.load(f))
    
    return transcripts


if __name__ == "__main__":
    # Test
    print(f"Transcripts directory: {TRANSCRIPTS_DIR}")
    print(f"Exists: {TRANSCRIPTS_DIR.exists()}")
