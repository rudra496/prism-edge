# PRISM-Edge: Production Container Image
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends     gcc     libc-dev     && rm -rf /var/lib/apt/lists/*

# Copy codebase
COPY . /app

# Install python dependencies
RUN pip install --no-cache-dir numpy reportlab

# Expose API port
EXPOSE 8080

# Healthcheck
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3     CMD python3 -c "import urllib.request; urllib.request.urlopen('http://localhost:8080/api/health')" || exit 1

# Launch Server
CMD ["python3", "api_server/server.py", "8080"]
