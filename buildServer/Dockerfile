FROM python:3.11-slim

# Set environment variables to prevent writing bytecode and reduce cache
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Set working directory
WORKDIR /app

# Install dependencies required for building Python packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libpq-dev 


COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt daphne

# Copy the rest of the application
COPY . .

# Expose port
EXPOSE 8000

# Run Daphne ASGI server
CMD ["daphne", "-b", "0.0.0.0", "-p", "8000", "buildServer.asgi:application"]
