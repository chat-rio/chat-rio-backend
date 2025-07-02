# Base image with Python
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app source code
COPY . .

# Expose port (change if using a different one)
EXPOSE 8894

# Start the FastAPI server
CMD ["uvicorn", "run:app", "--host", "0.0.0.0", "--port", "8894", "--reload"]
