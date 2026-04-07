# Ark Transcriber - Deployment Guide

## ✅ Service Status: LIVE

**URL**: `http://localhost:8000`  
**Status**: Running and healthy  
**Version**: 2.0.0

---

## 🚀 Quick Start

### 1. Single YouTube Video
```bash
curl -X POST "http://localhost:8000/transcribe" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://youtu.be/VIDEO_ID",
    "generate_summary": true,
    "summary_language": "id",
    "generate_diagrams": true
  }'
```

### 2. YouTube Playlist (Requires API Key)
**Option A: Get YouTube Data API Key**
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing
3. Enable "YouTube Data API v3"
4. Create API key
5. Set environment variable:
   ```bash
   export YOUTUBE_API_KEY=your_api_key_here
   ```
6. Restart the service

**Option B: Manual Video IDs**
Process videos individually from the playlist:
```bash
# Extract video IDs from playlist manually
# Then process each one:
curl -X POST "http://localhost:8000/transcribe" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://youtu.be/VIDEO_ID_1", ...}'

curl -X POST "http://localhost:8000/transcribe" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://youtu.be/VIDEO_ID_2", ...}'
```

### 3. PDF from URL
```bash
curl -X POST "http://localhost:8000/process-pdf" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://drive.google.com/file/d/FILE_ID/view",
    "generate_summary": true,
    "summary_language": "id",
    "generate_diagrams": true,
    "use_ocr": true
  }'
```

### 4. Upload PDF File
```bash
curl -X POST "http://localhost:8000/process-pdf-upload" \
  -F "file=@document.pdf" \
  -F "generate_summary=true" \
  -F "summary_language=id" \
  -F "generate_diagrams=true" \
  -F "use_ocr=true"
```

---

## 📁 Output Location

All processed content is automatically saved to:
```
ark-intelligent/.agents/docs/transcripts/
├── youtube/
│   ├── {video_id}/
│   │   ├── metadata.json
│   │   ├── transcript.md
│   │   ├── summary.md
│   │   └── diagrams/
│   └── {playlist_id}/
│       ├── metadata.json
│       ├── combined_summary.md
│       ├── transcript.md
│       └── videos/
│           └── {video_id}/
└── pdf/
    └── {filename_slug}/
        ├── metadata.json
        ├── full_text.md
        ├── summary.md
        └── diagrams/
```

---

## 🔧 Service Management

### Check Health
```bash
curl http://localhost:8000/health
```

### Restart Service
```bash
# Kill existing process
pkill -f "uvicorn main:app"

# Start new instance
cd /workspace/main/ark-transcriber
export PATH="$PATH:/home/node/.local/bin"
uvicorn main:app --host 0.0.0.0 --port 8000 &
```

### View Logs
```bash
# The service runs in background, check logs via:
journalctl -u uvicorn -f
# Or restart with --log-level debug for verbose output
```

---

## 📊 Example Response

### YouTube Video Response
```json
{
  "source_type": "youtube",
  "video_id": "ABC123",
  "transcript": [...],
  "full_text": "Full transcript text...",
  "summary": "AI-generated summary in Indonesian...",
  "duration_seconds": 1234,
  "diagrams": {
    "flowchart": "graph TD...",
    "mindmap": "mindmap...",
    "recommended": "flowchart"
  }
}
```

### PDF Response
```json
{
  "filename": "document.pdf",
  "total_pages": 50,
  "text_pages": 30,
  "image_pages": 20,
  "hybrid": true,
  "full_text": "Extracted text...",
  "summary": "Summary in Indonesian...",
  "diagrams": {...},
  "ocr_used": true,
  "ocr_pages": 20
}
```

---

## 🎯 Features

### ✅ Working Features
- Single YouTube video transcription
- PDF processing (URL or upload)
- OCR for scanned PDFs
- AI summarization (Indonesian/English)
- Mermaid.js diagram generation
- Auto-save to ark-intelligent
- Tag extraction
- Key points generation
- LLM-friendly output format

### ⚠️ Requires Setup
- YouTube Playlists (needs YouTube Data API v3 key)
- Google Drive folders (needs GDrive API key)

---

## 🔑 Environment Variables

```bash
# Required for AI summarization
export LITELLM_API_BASE="https://litellm.vllm.yesy.online/v1"
export LITELLM_API_KEY="your_api_key"

# Optional
export SUMMARY_MODEL="claude-opus-4-6"
export WORKSPACE_DIR="/tmp/transcript-workspace"

# For playlist support (optional)
export YOUTUBE_API_KEY="your_youtube_api_key"
```

---

## 🐛 Troubleshooting

### "No videos found in playlist"
- YouTube playlists require API key for extraction
- Use Option B: Process videos individually
- Or get YouTube Data API v3 key

### "Transcripts are disabled"
- Video creator disabled transcripts
- Try a different video

### "No module named 'xxx'"
```bash
export PATH="$PATH:/home/node/.local/bin"
pip install -r requirements.txt --break-system-packages
```

### Service not running
```bash
# Check if running
curl http://localhost:8000/health

# If not, restart
cd /workspace/main/ark-transcriber
export PATH="$PATH:/home/node/.local/bin"
uvicorn main:app --host 0.0.0.0 --port 8000 &
```

---

## 📈 Next Steps

1. **Get YouTube API Key** for playlist support
2. **Set up GDrive API** for folder processing
3. **Add authentication** for production use
4. **Set up monitoring** and logging
5. **Configure auto-restart** (systemd/supervisor)

---

## 🎉 Current Status

✅ **Service Running**: `http://localhost:8000`  
✅ **All Core Features Working**  
✅ **Auto-save to ark-intelligent**  
✅ **LLM-friendly Output**  
⚠️ **Playlist Support**: Needs API key

**Ready to process!** Send a single YouTube video URL or PDF to test.
