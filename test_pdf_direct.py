#!/usr/bin/env python3
"""
Direct PDF test without API
"""
import sys
sys.path.insert(0, '/workspace/main/ark-transcriber')

from pdf_processor import PDFProcessor
import pdfplumber

pdf_path = "/usr/local/lib/node_modules/openclaw/.openclaw/media/inbound/goldbach_trifecta_plans_2026_01---a5b2bf8f-c3a4-491e-b00f-a1fd1ad8fcaf.pdf"

print(f"Testing PDF: {pdf_path}")

try:
    # Try to open with pdfplumber directly
    with pdfplumber.open(pdf_path) as pdf:
        print(f"✅ PDF opened successfully")
        print(f"   Total pages: {len(pdf.pages)}")
        
        for i, page in enumerate(pdf.pages[:2]):  # First 2 pages
            text = page.extract_text()
            print(f"\n--- Page {i+1} ---")
            print(text[:200] if text else "No text")
            
except Exception as e:
    print(f"❌ Error: {str(e)}")
    import traceback
    traceback.print_exc()
