FROM --platform=linux/amd64 python:3.10-slim

# Set working directory
WORKDIR /app

# Copy dependencies
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# Entrypoint
CMD ["python", "process_pdfs.py"]
