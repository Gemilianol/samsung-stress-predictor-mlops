FROM python:3.10-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY backend/app.py ./
COPY backend/src/ ./src
COPY backend/models/ ./models
COPY backend/logs/ ./logs

# Expose port and bind to all interfaces
EXPOSE 2000
CMD ["python", "app.py", "--host=0.0.0.0", "--port=2000"]
