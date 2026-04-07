# Ark Transcriber → Ark Intelligent Workflow

## Overview

This workflow automatically saves processed transcripts from `ark-transcriber` to `ark-intelligent/.agents/docs/transcripts/` in a format optimized for LLM indexing and retrieval.

## How It Works

### 1. User Sends Content
- **YouTube Video/Playlist**: Send URL via Telegram/Chat
- **PDF**: Send URL (GDrive/direct) or upload file

### 2. Processing (ark-transcriber)
```
Input → Extract/OCR → Summarize → Generate Diagrams → Save to ark-intelligent
```

### 3. Storage (ark-intelligent)
All results saved to: `ark-intelligent/.agents/docs/transcripts/`

## Directory Structure

```
ark-intelligent/.agents/docs/
├── TRANSCRIPTS_INDEX.md          # Index and search guide
└── transcripts/
    ├── youtube/
    │   ├── {video_id}/           # Single video
    │   │   ├── metadata.json     # Structured metadata
    │   │   ├── transcript.md     # Full transcript
    │   │   ├── summary.md        # AI summary + key points
    │   │   └── diagrams/
    │   │       ├── flowchart.md
    │   │       ├── mindmap.md
    │   │       └── timeline.md
    │   └── {playlist_id}/        # Playlist (multiple videos)
    │       ├── metadata.json
    │       ├── combined_summary.md   # Overall playlist summary
    │       ├── transcript.md         # All videos combined
    │       ├── diagrams/
    │       └── videos/
    │           └── {video_id}/   # Individual video
    │               ├── metadata.json
    │               ├── transcript.md
    │               └── summary.md
    └── pdf/
        └── {filename_slug}/
            ├── metadata.json
            ├── full_text.md
            ├── summary.md
            └── diagrams/
```

## File Formats

### metadata.json
```json
{
  "source_type": "youtube|pdf",
  "source_id": "video_id or filename",
  "title": "Document Title",
  "created_at": "2026-04-07T17:00:00Z",
  "language": "id",
  "duration_seconds": 1234,
  "page_count": 50,
  "tags": ["trading", "strategy", "risk-management"],
  "processing_notes": "OCR used for 20 pages"
}
```

### summary.md
- **Executive Summary**: High-level overview
- **Key Points**: Top 5 extracted points
- **Actionable Insights**: What to do next
- **Tags**: Searchable keywords
- **Metadata**: Source info, OCR status

### Full Text Files
- Clean Markdown format
- Section headers preserved
- Tables converted to Markdown
- Page breaks marked with `---`

### Diagrams
- Mermaid.js source code
- Stored as `.md` files with code blocks
- Easy to render or read by LLM

## LLM Indexing Benefits

### 1. **Structured Metadata**
- `metadata.json` for quick filtering
- Tags for semantic search
- Timestamps for temporal queries

### 2. **Hierarchical Organization**
- Source type → ID → files
- Easy to navigate
- Clear relationships

### 3. **Multiple Abstraction Levels**
- **summary.md**: Quick overview
- **full_text.md**: Detailed analysis
- **diagrams/**: Visual concepts

### 4. **Search Optimization**
- Tags extracted automatically
- Key points bulleted
- Actionable insights highlighted

## Agent Query Examples

### Find all trading strategy content
```python
# Agent searches for:
- Tags containing "trading" AND "strategy"
- Source type: youtube OR pdf
- Language: id
```

### Get summary of specific video
```python
# Agent reads:
ark-intelligent/.agents/docs/transcripts/youtube/{video_id}/summary.md
```

### Find all content with risk management
```python
# Agent searches:
- Tags: "risk" AND "management"
- Reads executive summaries
- Extracts key points
```

### Get visual diagrams for a concept
```python
# Agent looks for:
ark-intelligent/.agents/docs/transcripts/youtube/{video_id}/diagrams/
```

## Usage Examples

### Example 1: YouTube Video
```
User: https://youtu.be/ABC123

→ Processed by ark-transcriber
→ Saved to: ark-intelligent/.agents/docs/transcripts/youtube/ABC123/
→ Files created:
  - metadata.json
  - transcript.md
  - summary.md
  - diagrams/flowchart.md
  - diagrams/mindmap.md
```

### Example 2: YouTube Playlist
```
User: https://youtube.com/playlist?list=PLxyz123

→ Processed by ark-transcriber
→ Saved to: ark-intelligent/.agents/docs/transcripts/youtube/PLxyz123/
→ Files created:
  
  # Playlist level
  - metadata.json (playlist info, all video IDs)
  - combined_summary.md (summary of ALL videos together)
  - transcript.md (all videos combined)
  - diagrams/ (playlist-level diagrams)
  
  # Individual videos
  - videos/
    ├── video1/
    │   ├── metadata.json
    │   ├── transcript.md
    │   └── summary.md
    ├── video2/
    │   ├── metadata.json
    │   ├── transcript.md
    │   └── summary.md
    └── video3/
        ├── metadata.json
        ├── transcript.md
        └── summary.md
```

### Example 2: PDF Document
```
User: [Upload trading-strategy.pdf]

→ Processed by ark-transcriber (OCR if needed)
→ Saved to: ark-intelligent/.agents/docs/transcripts/pdf/trading-strategy/
→ Files created:
  - metadata.json
  - full_text.md
  - summary.md
  - diagrams/flowchart.md
```

## API Endpoints

### Process YouTube
```bash
curl -X POST "http://localhost:8000/transcribe" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://youtu.be/ABC123",
    "generate_summary": true,
    "summary_language": "id",
    "generate_diagrams": true
  }'
```

### Process PDF from URL
```bash
curl -X POST "http://localhost:8000/process-pdf" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://drive.google.com/file/d/PDF_ID/view",
    "generate_summary": true,
    "summary_language": "id",
    "generate_diagrams": true,
    "use_ocr": true
  }'
```

### Upload PDF File
```bash
curl -X POST "http://localhost:8000/process-pdf-upload" \
  -F "file=@document.pdf" \
  -F "generate_summary=true" \
  -F "summary_language=id" \
  -F "generate_diagrams=true" \
  -F "use_ocr=true"
```

## Automatic Features

### Tag Extraction
- Scans summary for trading keywords
- Auto-tags: trading, strategy, risk, management, psychology, etc.
- Limits to 10 most relevant tags

### Key Points Generation
- Extracts top 5 sentences from summary
- Bulleted format
- Easy to scan

### Actionable Insights
- Pre-defined best practices
- Customized per content type
- Helps agents suggest next steps

## Maintenance

### List All Transcripts
```python
from save_to_ark_intelligent import list_all_transcripts
transcripts = list_all_transcripts()
```

### Get Transcript Path
```python
from save_to_ark_intelligent import get_transcript_path
path = get_transcript_path("ABC123", "youtube")
```

### Check if Exists
```python
from pathlib import Path
path = get_transcript_path("ABC123", "youtube")
if path.exists():
    print("Already processed!")
```

## Troubleshooting

### Files Not Saved?
1. Check logs for "Saving to ark-intelligent docs..."
2. Verify `ark-intelligent` path is correct
3. Check write permissions

### Tags Not Appearing?
- Tags are extracted from summary
- If summary is empty, default tags used
- Check summary generation first

### Diagrams Missing?
- Diagram generation is optional
- Check `generate_diagrams=true` in request
- Check logs for diagram errors

## Future Enhancements

- [ ] Automatic deduplication
- [ ] Cross-reference linking
- [ ] Full-text search index
- [ ] Vector embeddings for semantic search
- [ ] Auto-update on re-processing
- [ ] Export to other formats (Notion, Obsidian)

---

**Workflow Status**: ✅ Active  
**Last Updated**: 2026-04-07  
**Version**: 1.0.0
