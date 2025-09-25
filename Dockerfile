# Use Python 3.12 slim image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install system dependencies for TensorFlow and OpenSpiel
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    gfortran \
    libopenblas-dev \
    liblapack-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY backend/requirements_docker.txt requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY backend/ .
COPY library/ ./library/
COPY neuralnet/ ./neuralnet/

# Install local packages
RUN pip install -e ./library
RUN pip install -e ./neuralnet

# Expose port 8080 (Cloud Run default)
EXPOSE 8080

# Set environment variables
ENV PORT=8080
ENV ENVIRONMENT=production

# Run the FastAPI application
CMD ["uvicorn", "server_full:app", "--host", "0.0.0.0", "--port", "8080"]
