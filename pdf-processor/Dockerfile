# # Use slim build image
# FROM python:3.10-slim-bookworm AS builder

# # Install compiler tools and dependencies
# RUN apt-get update && \
#     apt-get install -y --no-install-recommends \
#     build-essential \
#     g++ \
#     cmake \
#     git \
#     libgl1 \
#     libglib2.0-0 \
#     wget

# # Download language model
# RUN wget -O /lid.176.ftz https://dl.fbaipublicfiles.com/fasttext/supervised-models/lid.176.ftz

# # Create virtual environment
# RUN python -m venv /opt/venv
# ENV PATH="/opt/venv/bin:$PATH"

# # Install Python dependencies
# COPY requirements.txt .
# RUN pip install --no-cache-dir wheel && \
#     pip install --no-cache-dir -r requirements.txt
# # ...existing code continues...

# # Install fasttext from source
# RUN git clone https://github.com/facebookresearch/fastText.git && \
#     cd fastText && \
#     pip install --no-cache-dir .

# # Final runtime image
# FROM python:3.10-slim-bookworm

# # Install runtime dependencies
# RUN apt-get update && \
#     apt-get install -y --no-install-recommends \
#     libgl1 libglib2.0-0 && \
#     rm -rf /var/lib/apt/lists/*

# # Create non-root user
# RUN useradd -m appuser
# WORKDIR /app
# RUN chown appuser:appuser /app
# USER appuser

# # Copy from builder
# COPY --from=builder --chown=appuser /lid.176.ftz /app/
# COPY --from=builder --chown=appuser /opt/venv /opt/venv

# # Set environment
# ENV PATH="/opt/venv/bin:$PATH"

# # Copy application
# COPY --chown=appuser . .

# ENTRYPOINT ["python", "processor.py"]
# Use slim build image
FROM python:3.10-slim-bookworm AS builder

# Install compiler tools and dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    g++ \
    cmake \
    git \
    libgl1 \
    libglib2.0-0 \
    wget

# Download language model
RUN wget -O /lid.176.ftz https://dl.fbaipublicfiles.com/fasttext/supervised-models/lid.176.ftz

# Create virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir wheel && \
    pip install --no-cache-dir -r requirements.txt

# Install fasttext from source
RUN git clone https://github.com/facebookresearch/fastText.git && \
    cd fastText && \
    pip install --no-cache-dir .

# Final runtime image
FROM python:3.10-slim-bookworm

# Install runtime dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    libgl1 \
    libglib2.0-0 \
    tesseract-ocr \
    tesseract-ocr-eng \
    tesseract-ocr-jpn && \
    rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN useradd -m appuser
WORKDIR /app
RUN chown appuser:appuser /app
USER appuser

# Copy from builder
COPY --from=builder --chown=appuser /lid.176.ftz /app/
COPY --from=builder --chown=appuser /opt/venv /opt/venv

# Set environment
ENV PATH="/opt/venv/bin:$PATH"

# Copy application
COPY --chown=appuser . .

ENTRYPOINT ["python", "processor.py"]