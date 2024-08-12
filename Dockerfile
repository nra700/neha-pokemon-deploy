# Use an official Python runtime as a parent image
FROM python:latest

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Set the working directory
WORKDIR /app

# Copy the application code
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Command to run the Celery worker
CMD ["celery", "-A", "app1.celery", "worker", "--loglevel=info"]
