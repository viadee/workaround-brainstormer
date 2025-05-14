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

# Create a non-root user and group
RUN groupadd -r appgroup && useradd --no-log-init -r -g appgroup appuser

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    FLASK_APP=run.py \
    FLASK_ENV=production

# Set the working directory
WORKDIR /app

# Create necessary directories and set ownership
RUN mkdir -p /app/logs /app/temp_uploads && \
    chown -R appuser:appgroup /app/logs && \
    chown -R appuser:appgroup /app/temp_uploads

# Copy requirements first for better caching
COPY --chown=appuser:appgroup requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install Gunicorn
RUN pip install --no-cache-dir gunicorn

# Copy the application code
COPY --chown=appuser:appgroup app app/
COPY --chown=appuser:appgroup static static/
COPY --chown=appuser:appgroup templates templates/
COPY --chown=appuser:appgroup run.py .

# Set correct permissions for the app directory
RUN chmod -R 755 /app
# Ensure appuser can write to logs and temp_uploads
RUN chmod -R u+w /app/logs /app/temp_uploads

# Switch to the non-root user
USER appuser

# Expose port 8080
EXPOSE 8080

# Use Gunicorn as the final command
CMD ["gunicorn", "run:app", "--workers=8", "--bind=0.0.0.0:8080"]