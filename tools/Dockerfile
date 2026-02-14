FROM texlive/texlive:latest

# Install Python and build tools
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    build-essential \
    git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip3 install --no-cache-dir --upgrade pip --break-system-packages && \
    pip3 install --no-cache-dir -r requirements.txt --break-system-packages

# Use existing non-root user from base image
USER texlive

# Maintain compatibility with our scripts
ENTRYPOINT ["python3"]