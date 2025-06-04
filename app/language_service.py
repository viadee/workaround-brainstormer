# app/language_service.py
from typing import Optional, Set
from dataclasses import dataclass, field
from langdetect import detect, DetectorFactory
import pytesseract
import logging
import base64
import io
from PIL import Image
import numpy as np
from functools import lru_cache

# Set seed for consistent language detection
DetectorFactory.seed = 0

# Initialize logger
logger = logging.getLogger(__name__)

# Cache for decoded base64 images
@lru_cache(maxsize=32)
def _decode_base64(base64_string: str) -> bytes:
    """
    Decode base64 string to bytes with caching.
    
    Args:
        base64_string: Base64 encoded string
        
    Returns:
        bytes: Decoded bytes
        
    Raises:
        ValueError: If decoding fails
    """
    try:
        # Clean up base64 string if it has data URI prefix
        if ',' in base64_string:
            base64_string = base64_string.split(',')[1]
        return base64.b64decode(base64_string)
    except Exception as e:
        logger.error(f"Failed to decode base64 string: {str(e)}")
        raise ValueError("Invalid base64 data") from e

@dataclass
class LanguageService:
    """Service for detecting languages in text and images."""
    
    supported_languages: Set[str] = field(default_factory=lambda: {'en', 'de'})

    def detect_language(
        self,
        text: Optional[str] = None,
        base64_image: Optional[str] = None,
        default_language: str = 'en'
    ) -> str:
        """
        Detect the language from text and/or image.
        
        Args:
            text: Text to analyze
            base64_image: Base64 encoded image to analyze
            default_language: Fallback language if detection fails
            
        Returns:
            str: Detected language code from supported languages
            
        Note:
            Prioritizes text over image for language detection.
            Falls back to default_language if detection fails.
        """
        try:
            # First try text-based detection if available
            if text and text.strip():
                detected = detect(text)
                if detected in self.supported_languages:
                    logger.info(f"Language detected from text: {detected}")
                    return detected

            # Then try image-based detection if available
            if base64_image:
                detected = self._detect_language_from_image(base64_image)
                if detected in self.supported_languages:
                    logger.info(f"Language detected from image: {detected}")
                    return detected

            # Default to specified language if no supported language detected
            logger.info(f"No supported language detected, using default: {default_language}")
            return default_language

        except Exception as e:
            logger.warning(f"Language detection failed: {str(e)}")
            return default_language

    def _decode_base64_image(self, base64_image: str) -> Image.Image:
        """
        Decode base64 image to PIL Image.
        
        Args:
            base64_image: Base64 encoded image
            
        Returns:
            Image.Image: PIL Image object
            
        Raises:
            ValueError: If image decoding fails
        """
        try:
            # Use cached base64 decoding
            image_data = _decode_base64(base64_image)
            
            # Convert to PIL Image
            return Image.open(io.BytesIO(image_data))
            
        except Exception as e:
            logger.error(f"Failed to decode base64 image: {str(e)}")
            raise ValueError("Invalid base64 image data") from e

    def _detect_language_from_image(self, base64_image: str) -> Optional[str]:
        """
        Detect language from image using Tesseract OCR.
        
        Args:
            base64_image: Base64 encoded image
            
        Returns:
            Optional[str]: Detected language code or None if detection fails
        """
        try:
            # Convert base64 to PIL Image
            image = self._decode_base64_image(base64_image)
            
            # Convert to grayscale for better OCR
            if image.mode != 'L':
                image = image.convert('L')
            
            # Perform OCR with error handling
            # Use --oem 1 for LSTM OCR Engine and --psm 3 for automatic page segmentation
            text = pytesseract.image_to_string(
                image,
                config='--oem 1 --psm 11'
            )
            
            # Detect language from extracted text
            if text.strip():
                detected = detect(text)
                if detected in self.supported_languages:
                    return detected
                    
        except Exception as e:
            logger.error(f"Image language detection failed: {str(e)}")
            
        return None