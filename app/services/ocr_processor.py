"""
OCR Processing Service for Recipe Images and PDFs
Handles text extraction from uploaded files using pytesseract
"""

import os
import cv2
import pytesseract
import numpy as np
from PIL import Image
from pdf2image import convert_from_path
import tempfile
from typing import Optional, List, Dict, Any
import logging

logger = logging.getLogger(__name__)

class OCRProcessor:
    """Handles OCR processing for recipe images and PDFs"""
    
    def __init__(self):
        # Configure pytesseract path (may need adjustment based on OS)
        self.setup_tesseract()
        
    def setup_tesseract(self):
        """Setup tesseract executable path"""
        # On Windows, might need to set the path
        # pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
        pass
    
    def extract_text_from_file(self, file_path: str, file_type: str) -> Dict[str, Any]:
        """
        Extract text from various file types
        
        Args:
            file_path: Path to the uploaded file
            file_type: MIME type of the file
            
        Returns:
            Dictionary with extracted text and processing info
        """
        try:
            if file_type.startswith('image/'):
                return self.process_image(file_path)
            elif file_type == 'application/pdf':
                return self.process_pdf(file_path)
            else:
                raise ValueError(f"Unsupported file type: {file_type}")
                
        except Exception as e:
            logger.error(f"OCR processing failed for {file_path}: {e}")
            return {
                'success': False,
                'text': '',
                'error': str(e),
                'processing_info': {'status': 'failed'}
            }
    
    def process_image(self, image_path: str) -> Dict[str, Any]:
        """
        Process a single image file using OCR
        
        Args:
            image_path: Path to the image file
            
        Returns:
            Dictionary with extracted text and processing info
        """
        try:
            # Load and preprocess image
            image = cv2.imread(image_path)
            if image is None:
                raise ValueError("Could not load image file")
            
            # Preprocess image for better OCR results
            processed_image = self.preprocess_image(image)
            
            # Convert back to PIL Image for pytesseract
            pil_image = Image.fromarray(processed_image)
            
            # Extract text using pytesseract
            custom_config = r'--oem 3 --psm 6 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789.,()-/: \n\t'
            extracted_text = pytesseract.image_to_string(pil_image, config=custom_config)
            
            # Get additional OCR data for confidence scoring
            ocr_data = pytesseract.image_to_data(pil_image, output_type=pytesseract.Output.DICT)
            confidence_scores = [int(conf) for conf in ocr_data['conf'] if int(conf) > 0]
            avg_confidence = sum(confidence_scores) / len(confidence_scores) if confidence_scores else 0
            
            return {
                'success': True,
                'text': extracted_text.strip(),
                'processing_info': {
                    'method': 'image_ocr',
                    'confidence': round(avg_confidence, 2),
                    'word_count': len(extracted_text.split()),
                    'status': 'completed'
                }
            }
            
        except Exception as e:
            logger.error(f"Image OCR processing failed: {e}")
            return {
                'success': False,
                'text': '',
                'error': str(e),
                'processing_info': {'status': 'failed', 'method': 'image_ocr'}
            }
    
    def process_pdf(self, pdf_path: str) -> Dict[str, Any]:
        """
        Process a PDF file by converting to images and running OCR
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            Dictionary with extracted text and processing info
        """
        try:
            # Convert PDF to images
            with tempfile.TemporaryDirectory() as temp_dir:
                # Convert PDF pages to images
                pages = convert_from_path(pdf_path, dpi=300, output_folder=temp_dir)
                
                all_text = []
                total_confidence = 0
                total_words = 0
                
                for i, page in enumerate(pages):
                    # Convert PIL image to numpy array
                    page_array = np.array(page)
                    
                    # Preprocess page image
                    processed_page = self.preprocess_image(page_array)
                    pil_page = Image.fromarray(processed_page)
                    
                    # Extract text from this page
                    custom_config = r'--oem 3 --psm 6 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789.,()-/: \n\t'
                    page_text = pytesseract.image_to_string(pil_page, config=custom_config)
                    
                    if page_text.strip():
                        all_text.append(f"--- Page {i+1} ---")
                        all_text.append(page_text.strip())
                        all_text.append("")  # Empty line between pages
                    
                    # Get confidence data
                    ocr_data = pytesseract.image_to_data(pil_page, output_type=pytesseract.Output.DICT)
                    confidence_scores = [int(conf) for conf in ocr_data['conf'] if int(conf) > 0]
                    if confidence_scores:
                        total_confidence += sum(confidence_scores)
                        total_words += len(confidence_scores)
                
                extracted_text = "\n".join(all_text)
                avg_confidence = total_confidence / total_words if total_words > 0 else 0
                
                return {
                    'success': True,
                    'text': extracted_text,
                    'processing_info': {
                        'method': 'pdf_ocr',
                        'pages_processed': len(pages),
                        'confidence': round(avg_confidence, 2),
                        'word_count': len(extracted_text.split()),
                        'status': 'completed'
                    }
                }
                
        except Exception as e:
            logger.error(f"PDF OCR processing failed: {e}")
            return {
                'success': False,
                'text': '',
                'error': str(e),
                'processing_info': {'status': 'failed', 'method': 'pdf_ocr'}
            }
    
    def preprocess_image(self, image: np.ndarray) -> np.ndarray:
        """
        Preprocess image for better OCR results
        
        Args:
            image: Input image as numpy array
            
        Returns:
            Preprocessed image as numpy array
        """
        # Convert to grayscale
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image
        
        # Apply Gaussian blur to reduce noise
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        
        # Apply adaptive thresholding for better text contrast
        thresh = cv2.adaptiveThreshold(
            blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
        )
        
        # Apply morphological operations to clean up the image
        kernel = np.ones((1, 1), np.uint8)
        cleaned = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
        cleaned = cv2.morphologyEx(cleaned, cv2.MORPH_OPEN, kernel)
        
        return cleaned
    
    def validate_extracted_text(self, text: str) -> Dict[str, Any]:
        """
        Validate extracted text for recipe content
        
        Args:
            text: Extracted text to validate
            
        Returns:
            Validation results
        """
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
            'minutes', 'hours', 'temperature', 'degrees', 'salt', 'pepper'
        ]
        
        text_lower = text.lower()
        keyword_matches = sum(1 for keyword in recipe_keywords if keyword in text_lower)
        
        # Calculate confidence based on keyword matches and text length
        keyword_confidence = min(keyword_matches / len(recipe_keywords) * 100, 100)
        length_confidence = min(len(text) / 500 * 100, 100)  # 500 chars = 100% confidence
        overall_confidence = (keyword_confidence + length_confidence) / 2
        
        return {
            'is_valid': overall_confidence > 20,  # At least 20% confidence
            'confidence': round(overall_confidence, 2),
            'keyword_matches': keyword_matches,
            'text_length': len(text),
            'reason': 'Sufficient recipe content detected' if overall_confidence > 20 else 'Low recipe content confidence'
        }