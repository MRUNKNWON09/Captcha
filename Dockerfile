FROM python:3.11-slim

# Install Tesseract OCR and required libraries
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    libtesseract-dev \
    libgl1 \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Run FastAPI with Uvicorn
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080"]
