FROM python:3.9-slim

WORKDIR /app

# Copy model first since it rarely changes
COPY u2net.onnx /home/.u2net/u2net.onnx

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY templates /app/templates
COPY app.py .

# Create uploads directory
RUN mkdir -p uploads

# Set environment variables
ENV PORT=8080
EXPOSE 8080

# Use array form of CMD for better signal handling
CMD ["python", "app.py"]