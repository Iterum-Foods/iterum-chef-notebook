"""
OCR Processing Service - Fallback Implementation
Handles text extraction when Tesseract is not available
"""

import os
import logging
from typing import Optional, List, Dict, Any
import tempfile

logger = logging.getLogger(__name__)

class OCRProcessorFallback:
    """Fallback OCR processor when Tesseract is not available"""
    
    def __init__(self):
        self.tesseract_available = self.check_tesseract_availability()
        
    def check_tesseract_availability(self) -> bool:
        """Check if Tesseract and dependencies are available"""
        try:
            import pytesseract
            import cv2
            from PIL import Image
            from pdf2image import convert_from_path
            
            # Try to run tesseract
            pytesseract.get_tesseract_version()
            return True
        except ImportError as e:
            logger.warning(f"OCR dependencies not available: {e}")
            return False
        except Exception as e:
            logger.warning(f"Tesseract not properly configured: {e}")
            return False
    
    def extract_text_from_file(self, file_path: str, file_type: str) -> Dict[str, Any]:
        """
        Extract text from various file types with fallback handling
        
        Args:
            file_path: Path to the uploaded file
            file_type: MIME type of the file
            
        Returns:
            Dictionary with extracted text and processing info
        """
        try:
            if not self.tesseract_available:
                return self.handle_no_tesseract(file_path, file_type)
                
            # If Tesseract is available, use full OCR
            if file_type.startswith('image/'):
                return self.process_image_with_ocr(file_path)
            elif file_type == 'application/pdf':
                return self.process_pdf_with_ocr(file_path)
            else:
                raise ValueError(f"Unsupported file type: {file_type}")
                
        except Exception as e:
            logger.error(f"OCR processing failed for {file_path}: {e}")
            return {
                'success': False,
                'text': '',
                'error': str(e),
                'processing_info': {'status': 'failed', 'method': 'fallback'}
            }
    
    def handle_no_tesseract(self, file_path: str, file_type: str) -> Dict[str, Any]:
        """Handle file processing when Tesseract is not available"""
        
        if file_type == 'application/pdf':
            # Try to extract text from PDF without OCR
            return self.extract_pdf_text_fallback(file_path)
        else:
            # For images, return helpful guidance
            return {
                'success': False,
                'text': '',
                'error': 'OCR not available - Tesseract not installed',
                'processing_info': {
                    'status': 'failed',
                    'method': 'fallback',
                    'message': 'Please install Tesseract OCR to process images',
                    'setup_guide': 'See OCR_SETUP_GUIDE.md for installation instructions'
                }
            }
    
    def extract_pdf_text_fallback(self, pdf_path: str) -> Dict[str, Any]:
        """Extract text from PDF using PyPDF2 as fallback"""
        try:
            import PyPDF2
            
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text_content = []
                
                for page_num, page in enumerate(pdf_reader.pages):
                    page_text = page.extract_text()
                    if page_text.strip():
                        text_content.append(f"--- Page {page_num + 1} ---")
                        text_content.append(page_text.strip())
                        text_content.append("")
                
                extracted_text = "\n".join(text_content)
                
                if extracted_text.strip():
                    return {
                        'success': True,
                        'text': extracted_text,
                        'processing_info': {
                            'method': 'pdf_text_extraction',
                            'pages_processed': len(pdf_reader.pages),
                            'confidence': 100,  # Text extraction is exact
                            'word_count': len(extracted_text.split()),
                            'status': 'completed',
                            'note': 'Text extracted directly from PDF (no OCR needed)'
                        }
                    }
                else:
                    return {
                        'success': False,
                        'text': '',
                        'error': 'No extractable text found in PDF - may be image-based',
                        'processing_info': {
                            'method': 'pdf_text_extraction',
                            'status': 'failed',
                            'note': 'PDF may contain only images - OCR required'
                        }
                    }
                    
        except ImportError:
            # PyPDF2 not available, try basic text extraction
            return {
                'success': False,
                'text': '',
                'error': 'PDF processing dependencies not available',
                'processing_info': {
                    'status': 'failed',
                    'method': 'fallback',
                    'required_packages': ['PyPDF2', 'pytesseract', 'pdf2image']
                }
            }
        except Exception as e:
            return {
                'success': False,
                'text': '',
                'error': f"PDF text extraction failed: {str(e)}",
                'processing_info': {'status': 'failed', 'method': 'pdf_text_extraction'}
            }
    
    def process_image_with_ocr(self, image_path: str) -> Dict[str, Any]:
        """Process image with full OCR (when available)"""
        try:
            import cv2
            import pytesseract
            from PIL import Image
            import numpy as np
            
            # Load and preprocess image
            image = cv2.imread(image_path)
            if image is None:
                raise ValueError("Could not load image file")
            
            # Basic preprocessing
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            pil_image = Image.fromarray(gray)
            
            # Extract text
            custom_config = r'--oem 3 --psm 6'
            extracted_text = pytesseract.image_to_string(pil_image, config=custom_config)
            
            return {
                'success': True,
                'text': extracted_text.strip(),
                'processing_info': {
                    'method': 'image_ocr',
                    'confidence': 85,  # Default confidence
                    'word_count': len(extracted_text.split()),
                    'status': 'completed'
                }
            }
            
        except Exception as e:
            return {
                'success': False,
                'text': '',
                'error': f"Image OCR failed: {str(e)}",
                'processing_info': {'status': 'failed', 'method': 'image_ocr'}
            }
    
    def process_pdf_with_ocr(self, pdf_path: str) -> Dict[str, Any]:
        """Process PDF with full OCR (when available)"""
        try:
            from pdf2image import convert_from_path
            import pytesseract
            from PIL import Image
            
            # Convert PDF to images
            with tempfile.TemporaryDirectory() as temp_dir:
                pages = convert_from_path(pdf_path, dpi=200, output_folder=temp_dir)
                
                all_text = []
                for i, page in enumerate(pages):
                    # Extract text from page
                    custom_config = r'--oem 3 --psm 6'
                    page_text = pytesseract.image_to_string(page, config=custom_config)
                    
                    if page_text.strip():
                        all_text.append(f"--- Page {i+1} ---")
                        all_text.append(page_text.strip())
                        all_text.append("")
                
                extracted_text = "\n".join(all_text)
                
                return {
                    'success': True,
                    'text': extracted_text,
                    'processing_info': {
                        'method': 'pdf_ocr',
                        'pages_processed': len(pages),
                        'confidence': 80,  # Default confidence
                        'word_count': len(extracted_text.split()),
                        'status': 'completed'
                    }
                }
                
        except Exception as e:
            # Fallback to text extraction
            return self.extract_pdf_text_fallback(pdf_path)
    
    def validate_extracted_text(self, text: str) -> Dict[str, Any]:
        """Validate extracted text for recipe content"""
        if not text or len(text.strip()) < 10:
            return {
                'is_valid': False,
                'reason': 'Text too short or empty',
                'confidence': 0
            }
        
        # Check for recipe-like keywords
        recipe_keywords = [
            'ingredient', 'cup', 'tablespoon', 'teaspoon', 'ounce', 'pound', 'gram',
            'recipe', 'cook', 'bake', 'heat', 'mix', 'add', 'combine', 'serve',
            'minutes', 'hours', 'temperature', 'degrees', 'salt', 'pepper',
            'menu', 'dish', 'course', 'appetizer', 'main', 'dessert'
        ]
        
        text_lower = text.lower()
        keyword_matches = sum(1 for keyword in recipe_keywords if keyword in text_lower)
        
        # Calculate confidence
        keyword_confidence = min(keyword_matches / len(recipe_keywords) * 100, 100)
        length_confidence = min(len(text) / 500 * 100, 100)
        overall_confidence = (keyword_confidence + length_confidence) / 2
        
        return {
            'is_valid': overall_confidence > 15,  # Lower threshold for menus
            'confidence': round(overall_confidence, 2),
            'keyword_matches': keyword_matches,
            'text_length': len(text),
            'reason': 'Sufficient content detected' if overall_confidence > 15 else 'Low content confidence'
        }