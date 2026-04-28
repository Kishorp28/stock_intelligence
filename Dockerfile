# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set the working directory directly in the container
WORKDIR /app

# Install system dependencies required for data-science and MySQL packages
RUN apt-get update && apt-get install -y \
    build-essential \
    pkg-config \
    default-libmysqlclient-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file into the container
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project directory into the container
COPY . .

# Explicitly expose port 8000
EXPOSE 8000

# Command to run on application startup
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
