FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libssl-dev \
    python3-dev \
    libjpeg62-turbo-dev \
    zlib1g-dev \
    libfreetype6-dev \
    # Additional dependencies for SVG handling
    pkg-config \
    libcairo2-dev \
    libpango1.0-dev \
    libgdk-pixbuf2.0-dev \
    libtiff5-dev \
    libxml2-dev \
    libxslt1-dev \
    # PDF handling dependencies
    poppler-utils \
    libpangocairo-1.0-0 \
    libgdk-pixbuf2.0-0 \
    shared-mime-info \
    # Tesseract OCR dependencies
    tesseract-ocr \
    tesseract-ocr-deu \
    && rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    FLASK_APP=run.py \
    FLASK_ENV=production

# Set the working directory
WORKDIR /app

# Create necessary directories
RUN mkdir -p /app/logs /app/temp_uploads

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY app app/
COPY static static/
COPY templates templates/
COPY run.py .

# Set correct permissions
RUN chmod -R 755 /app && \
    chmod -R 777 /app/logs && \
    chmod -R 777 /app/temp_uploads

# Expose port 5001
EXPOSE 5001

# Set the entry point to run your app
CMD ["python", "run.py"]