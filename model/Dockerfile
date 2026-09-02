# Model Training Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy model requirements
COPY model/requirements.txt requirements.txt

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy code
COPY train.csv .
COPY test.csv .
COPY model/ model/

# Run training
CMD ["python", "model/train.py"]
