"""
PDF Processor for Ark Transcriber
Handles text extraction, OCR, and content analysis for PDFs
"""

import os
import logging
import tempfile
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
import pdfplumber
import pytesseract
from pdf2image import convert_from_path
from PIL import Image
import io

logger = logging.getLogger(__name__)


class PDFProcessor:
    """Process PDFs - extract text, handle images, OCR"""
    
    def __init__(self, workspace_dir: str = "/tmp/pdf-workspace"):
        self.workspace_dir = Path(workspace_dir)
        self.workspace_dir.mkdir(parents=True, exist_ok=True)
        
        # Check if tesseract is installed
        try:
            pytesseract.get_tesseract_version()
            self.ocr_available = True
            logger.info("Tesseract OCR is available")
        except pytesseract.TesseractNotFoundError:
            self.ocr_available = False
            logger.warning("Tesseract OCR not found. Image-based PDFs will not be processed.")
    
    def analyze_pdf(self, pdf_path: str) -> Dict[str, Any]:
        """Analyze PDF to determine types of pages (text vs image)"""
        
        result = {
            "total_pages": 0,
            "text_pages": 0,
            "image_pages": 0,
            "hybrid": False,
            "page_types": []
        }
        
        try:
            with pdfplumber.open(pdf_path) as pdf:
                result["total_pages"] = len(pdf.pages)
                
                for i, page in enumerate(pdf.pages):
                    text = page.extract_text() or ""
                    images = page.images
                    
                    if text.strip() and images:
                        result["page_types"].append("hybrid")
                        result["hybrid"] = True
                        result["text_pages"] += 1
                        result["image_pages"] += 1
                    elif text.strip():
                        result["page_types"].append("text")
                        result["text_pages"] += 1
                    else:
                        result["page_types"].append("image")
                        result["image_pages"] += 1
        
        except Exception as e:
            logger.error(f"PDF analysis failed: {str(e)}")
            raise
    
    def extract_text_from_pdf(self, pdf_path: str) -> Tuple[str, List[Dict[str, Any]]]:
        """Extract text from PDF pages"""
        
        full_text = ""
        page_details = []
        
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for i, page in enumerate(pdf.pages):
                    text = page.extract_text() or ""
                    
                    # Extract tables if any
                    tables = page.extract_tables()
                    
                    page_info = {
                        "page_number": i + 1,
                        "text": text,
                        "tables": tables,
                        "has_tables": len(tables) > 0 if tables else False
                    }
                    
                    page_details.append(page_info)
                    full_text += f"\n\n--- Page {i+1} ---\n{text}"
        
        except Exception as e:
            logger.error(f"Text extraction failed: {str(e)}")
            raise
        
        return full_text, page_details
    
    def extract_images_from_pdf(self, pdf_path: str) -> List[Dict[str, Any]]:
        """Convert PDF pages to images for OCR"""
        
        if not self.ocr_available:
            logger.warning("OCR not available, skipping image extraction")
            return []
        
        images_info = []
        
        try:
            # Convert PDF to images
            images = convert_from_path(pdf_path, dpi=300)
            
            for i, image in enumerate(images):
                # Save temporary image
                temp_path = self.workspace_dir / f"page_{i+1}.png"
                image.save(str(temp_path), "PNG")
                
                # Perform OCR
                text = pytesseract.image_to_string(image)
                
                images_info.append({
                    "page_number": i + 1,
                    "image_path": str(temp_path),
                    "ocr_text": text,
                    "confidence": 0.0  # Could be improved with --psm options
                })
        
        except Exception as e:
            logger.error(f"Image extraction/OCR failed: {str(e)}")
        
        return images_info
    
    def process_pdf(self, pdf_path: str, use_ocr: bool = True) -> Dict[str, Any]:
        """
        Complete PDF processing:
        1. Analyze page types
        2. Extract text from text-based pages
        3. OCR image-based pages if enabled
        4. Combine all content
        """
        
        logger.info(f"Processing PDF: {pdf_path}")
        
        # Step 1: Analyze
        analysis = self.analyze_pdf(pdf_path)
        logger.info(f"PDF analysis: {analysis['text_pages']} text pages, "
                   f"{analysis['image_pages']} image pages")
        
        # Step 2: Extract text
        text_content, page_details = self.extract_text_from_pdf(pdf_path)
        
        # Step 3: OCR if needed
        ocr_content = ""
        if use_ocr and analysis["image_pages"] > 0:
            logger.info(f"Performing OCR on {analysis['image_pages']} pages...")
            images_info = self.extract_images_from_pdf(pdf_path)
            
            for img_info in images_info:
                if img_info["ocr_text"].strip():
                    ocr_content += f"\n\n--- OCR Page {img_info['page_number']} ---\n{img_info['ocr_text']}"
        
        # Step 4: Combine
        full_content = text_content
        if ocr_content:
            full_content += f"\n\n=== OCR CONTENT ===\n{ocr_content}"
        
        return {
            "filename": os.path.basename(pdf_path),
            "total_pages": analysis["total_pages"],
            "text_pages": analysis["text_pages"],
            "image_pages": analysis["image_pages"],
            "hybrid": analysis["hybrid"],
            "page_types": analysis["page_types"],
            "full_text": full_content,
            "page_details": page_details,
            "ocr_used": use_ocr and analysis["image_pages"] > 0,
            "ocr_pages": len([p for p in analysis["page_types"] if p == "image"]) if use_ocr else 0
        }
    
    def cleanup_temp_files(self):
        """Remove temporary files"""
        import shutil
        if self.workspace_dir.exists():
            shutil.rmtree(self.workspace_dir)
            self.workspace_dir.mkdir(parents=True, exist_ok=True)
