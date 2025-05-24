# Use a lightweight Python base image
FROM python:3.11-slim

# Set environment variables to prevent writing bytecode and logs in Docker
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Set working directory
WORKDIR /app

# Install dependencies required for building Python packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libpq-dev 

# Copy and install dependencies first to leverage Docker caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt daphne

# Copy the rest of the application
COPY . .


# Expose port
EXPOSE 8001

# Run Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8001"]
