#!/usr/bin/env python3
"""
Test PDF processing through API with detailed error logging
"""
import sys
sys.path.insert(0, '/workspace/main/ark-transcriber')

from pdf_processor import PDFProcessor
import logging

logging.basicConfig(level=logging.DEBUG)

pdf_path = "/usr/local/lib/node_modules/openclaw/.openclaw/media/inbound/goldbach_trifecta_plans_2026_01---a5b2bf8f-c3a4-491e-b00f-a1fd1ad8fcaf.pdf"

processor = PDFProcessor()

print("Step 1: Analyze PDF")
analysis = processor.analyze_pdf(pdf_path)
print(f"Analysis result: {analysis}")

print("\nStep 2: Extract text")
try:
    text_content, page_details = processor.extract_text_from_pdf(pdf_path)
    print(f"Text extracted: {len(text_content)} chars")
    print(f"First 200 chars: {text_content[:200]}")
except Exception as e:
    print(f"❌ Text extraction failed: {str(e)}")
    import traceback
    traceback.print_exc()

print("\nStep 3: Process PDF")
try:
    result = processor.process_pdf(pdf_path, use_ocr=False)
    print(f"✅ Processed successfully!")
    print(f"   Filename: {result['filename']}")
    print(f"   Total pages: {result['total_pages']}")
    print(f"   Text pages: {result['text_pages']}")
    print(f"   Full text length: {len(result['full_text'])} chars")
except Exception as e:
    print(f"❌ Processing failed: {str(e)}")
    import traceback
    traceback.print_exc()
