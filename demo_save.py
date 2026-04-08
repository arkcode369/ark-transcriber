#!/usr/bin/env python3
"""
Demo: Create sample transcript and save to ark-intelligent
"""
import sys
sys.path.insert(0, '/workspace/main/ark-transcriber')

from save_to_ark_intelligent import save_youtube_transcript
from pathlib import Path

# Sample content (simulating a processed video)
sample_transcript = """
Welcome to this trading masterclass. Today we'll cover the three pillars of successful trading.

First, risk management. Never risk more than 2% of your capital on a single trade. This ensures you can survive a string of losses without blowing up your account.

Second, entry strategy. Wait for price to reach key support or resistance levels. Look for confirmation signals like candlestick patterns or volume spikes before entering.

Third, psychology. Most traders fail because of emotional decisions. Stick to your plan, accept losses as part of the game, and focus on long-term consistency.

Remember: trading is a marathon, not a sprint. Discipline and patience are your greatest weapons.
"""

sample_summary = """
Video ini membahas tiga pilar utama dalam trading sukses:

1. **Manajemen Risiko**: Jangan pernah risiko lebih dari 2% modal per trade. Ini memastikan Anda bisa bertahan dari serangkaian kerugian tanpa kehilangan seluruh akun.

2. **Strategi Entry**: Tunggu harga mencapai level support atau resistance kunci. Cari sinyal konfirmasi seperti pola candlestick atau lonjakan volume sebelum masuk.

3. **Psikologi**: Kebanyakan trader gagal karena keputusan emosional. Tetap pada rencana Anda, terima kerugian sebagai bagian dari permainan, dan fokus pada konsistensi jangka panjang.

Kesimpulan: Trading adalah maraton, bukan sprint. Disiplin dan kesabaran adalah senjata terbesar Anda.
"""

sample_diagrams = {
    "flowchart": """
graph TD
    A[Start Trading] --> B{Risk Management}
    B -->|2% Rule| C[Entry Strategy]
    C -->|Key Levels| D{Confirmation Signals}
    D -->|Yes| E[Enter Trade]
    D -->|No| F[Wait]
    E --> G[Psychology]
    G -->|Discipline| H[Exit with Profit]
    G -->|Emotion| I[Loss]
    H --> J[Review Trade]
    I --> J
    J --> A
    """,
    "mindmap": """
mindmap
  root((Trading Success))
    Risk Management
      2% Rule
      Stop Loss
      Position Sizing
    Entry Strategy
      Key Levels
      Confirmation
      Multiple Timeframes
    Psychology
      Discipline
      Patience
      Emotional Control
    Exit Strategy
      Take Profit
      Trail Stop
      Review
    """,
    "recommended": "flowchart"
}

# Save to ark-intelligent
print("🔄 Saving demo transcript to ark-intelligent...")
saved_path = save_youtube_transcript(
    video_id="demo-trading-masterclass",
    title="Trading Masterclass - Three Pillars of Success",
    transcript_text=sample_transcript,
    summary=sample_summary,
    diagrams=sample_diagrams,
    language="id",
    duration_seconds=180,
    source_url="https://youtu.be/demo-trading-masterclass"
)

print(f"✅ Saved to: {saved_path}")
print(f"\n📁 Files created:")
for file in sorted(saved_path.glob("*")):
    print(f"   - {file.name}")

if (saved_path / "diagrams").exists():
    print(f"\n📊 Diagrams:")
    for diag in sorted((saved_path / "diagrams").glob("*")):
        print(f"   - {diag.name}")

print(f"\n🎯 Ready to commit and push to GitHub!")
