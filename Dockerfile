FROM python:3.11-slim

# Improve runtime behavior and install deps without cache
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# Install Python dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt \
    && pip install --no-cache-dir "psycopg[binary]>=3.1,<3.2"

# Copy application code
COPY . .

# Default runtime configuration
ENV IMAGE_DIR=/app/image_data
EXPOSE 8000

# Start FastAPI with Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

