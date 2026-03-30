# ===== ROOT DOCKERFILE (Backend) =====
# Use the official Python image from the Docker Hub
FROM python:3.10-slim

# Install system dependencies required for psycopg2 and Google Cloud libraries
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /usr/src/app

# Copy requirements file first for better caching
COPY requirements.txt ./

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Create a non-root user for security
RUN useradd --create-home --shell /bin/bash app && \
    chown -R app:app /usr/src/app
USER app

# Expose the port FastAPI will run on
EXPOSE 8000

# Add health check endpoint
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Command to run the application with proper configuration for Cloud Run
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]






# # Use the official Python image from the Docker Hub
# FROM python:3.10-slim

# # Install system dependencies required for psycopg2
# RUN apt-get update && apt-get install -y \
#     libpq-dev \
#     gcc \
#     && rm -rf /var/lib/apt/lists/*

# # Set the working directory
# WORKDIR /usr/src/app

# # Copy requirements file first for better caching
# COPY requirements.txt ./

# # Install Python dependencies
# RUN pip install --no-cache-dir -r requirements.txt

# # Copy the application code
# COPY . .

# # Expose the port FastAPI will run on
# EXPOSE 8000

# # Command to run the application
# CMD [ "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000" ]