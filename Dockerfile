ARG BUILD_FROM
FROM $BUILD_FROM

# Set working directory
WORKDIR /app

# Install system dependencies needed for Pillow, numpy, etc.
RUN apk add --no-cache \
    openjpeg \
    tiff \
    openblas-dev \
    build-base \
    python3-dev \
    linux-headers \
    libffi-dev

# Install Python dependencies directly (no pip upgrade)
RUN python3 -m pip install --no-cache-dir \
    pillow \
    numpy \
    RPi.GPIO \
    smbus

# Copy add-on files
COPY . /app

# Make main script executable
RUN chmod +x ./bin/main.py

# Run the add-on
CMD ["python3", "./bin/main.py"]
