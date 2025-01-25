# app/utils.py
import base64
from io import BytesIO
from flask import current_app
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM
from werkzeug.utils import secure_filename
import os
import tempfile
import logging
from typing import Union, Dict, Any, Optional, Tuple
from pdf2image import convert_from_path
from PIL import Image
import hashlib
import json

logger = logging.getLogger(__name__)

class ImageCache:
    """Manages caching of processed images."""
    
    def __init__(self):
        self._cache_dir = os.path.join(current_app.config['UPLOAD_FOLDER'], 'cache')
        os.makedirs(self._cache_dir, exist_ok=True)
    
    def _get_cache_key(self, file_path: str, original_filename: str) -> str:
        """Generate a unique cache key based on file content and name."""
        with open(file_path, 'rb') as f:
            file_hash = hashlib.md5(f.read()).hexdigest()
        return f"{file_hash}_{os.path.splitext(original_filename)[0]}"
    
    def get(self, cache_key: str) -> Optional[str]:
        """Retrieve cached base64 image data."""
        cache_file = os.path.join(self._cache_dir, f"{cache_key}.json")
        if os.path.exists(cache_file):
            try:
                with open(cache_file, 'r') as f:
                    return json.load(f)['base64_data']
            except Exception as e:
                logger.error(f"Error reading cache file: {str(e)}")
                return None
        return None
    
    def set(self, cache_key: str, base64_data: str) -> None:
        """Store base64 image data in cache."""
        cache_file = os.path.join(self._cache_dir, f"{cache_key}.json")
        try:
            with open(cache_file, 'w') as f:
                json.dump({'base64_data': base64_data}, f)
        except Exception as e:
            logger.error(f"Error writing cache file: {str(e)}")

def allowed_file(filename: str) -> bool:
    """Check if a filename has an allowed extension."""
    return (
        '.' in filename and 
        filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']
    )

def process_image(file_path: str, original_filename: str) -> str:
    """
    Process an uploaded file, converting to base64 encoded PNG with caching.
    
    Args:
        file_path: Path to the uploaded file
        original_filename: Original name of the file
        
    Returns:
        str: Base64 encoded image data
    """
    try:
        cache = ImageCache()
        cache_key = cache._get_cache_key(file_path, original_filename)
        
        # Try to get from cache first
        cached_data = cache.get(cache_key)
        if cached_data:
            logger.info(f"Cache hit for {original_filename}")
            return cached_data
            
        # Process based on file type if not in cache
        extension = original_filename.rsplit('.', 1)[1].lower()
        
        if extension == 'svg':
            base64_data = _process_svg(file_path)
        elif extension == 'pdf':
            base64_data = _process_pdf(file_path)
        else:  # Regular image files (png, jpg, jpeg)
            base64_data = _process_regular_image(file_path)
        
        # Cache the processed image
        cache.set(cache_key, base64_data)
        logger.info(f"Cached processed image for {original_filename}")
        
        return base64_data
        
    except Exception as e:
        logger.error(f"Error processing file {original_filename}: {str(e)}")
        raise ValueError(f"Failed to process file: {str(e)}")

def _process_svg(file_path: str) -> str:
    """Convert SVG to base64 encoded PNG."""
    drawing = svg2rlg(file_path)
    if not drawing:
        raise ValueError("Failed to convert SVG file")
        
    img_data = BytesIO()
    renderPM.drawToFile(drawing, img_data, fmt="PNG")
    return base64.b64encode(img_data.getvalue()).decode('utf-8')

def _process_pdf(file_path: str) -> str:
    """Convert PDF pages into a single combined image."""
    try:
        images = convert_from_path(
            file_path,
            dpi=300,
            size=(2000, None),
            use_cropbox=True,
            strict=False
        )
        
        if not images:
            raise ValueError("Failed to convert PDF file")
            
        # Calculate dimensions for combined image
        total_height = sum(img.size[1] for img in images)
        max_width = max(img.size[0] for img in images)
        
        # Create new image to hold all pages
        combined_image = Image.new('RGB', (max_width, total_height), 'white')
        
        # Paste each page into the combined image
        y_offset = 0
        for img in images:
            if img.mode != 'RGB':
                img = img.convert('RGB')
            combined_image.paste(img, (0, y_offset))
            y_offset += img.size[1]
        
        # Convert to PNG and encode as base64
        img_buffer = BytesIO()
        combined_image.save(
            img_buffer, 
            format='PNG', 
            optimize=True, 
            quality=95
        )
        img_buffer.seek(0)
        
        return base64.b64encode(img_buffer.getvalue()).decode('utf-8')
        
    except Exception as e:
        logger.error(f"Error converting PDF: {str(e)}")
        raise ValueError(f"Failed to convert PDF: {str(e)}")

def _process_regular_image(file_path: str) -> str:
    """Process regular image files (PNG, JPEG)."""
    with open(file_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

def save_uploaded_file(file) -> Tuple[str, str]:
    """Safely save an uploaded file."""
    if not allowed_file(file.filename):
        raise ValueError("Invalid file type")
        
    filename = secure_filename(file.filename)
    file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)
    
    return file_path, file.filename

def format_workarounds_tree(tree: dict) -> str:
    """
    Format workarounds tree into text format.
    
    Args:
        tree: Dictionary representing workarounds tree
        
    Returns:
        str: Formatted text representation
    """
    def traverse(node, depth):
        """Recursively traverse workaround tree."""
        lines = []
        if node['id'] != 0:
            indent = '    ' * depth
            lines.append(f"{indent}- {node['text']}")
        for child in node.get('children', []):
            lines.extend(traverse(child, depth + 1))
        return lines

    lines = []
    for child in tree.get('children', []):
        lines.extend(traverse(child, 0))
        
    return '\n'.join(lines)