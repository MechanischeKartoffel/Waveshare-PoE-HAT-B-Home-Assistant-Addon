# Use the Home Assistant aarch64 base image
ARG BUILD_FROM=ghcr.io/home-assistant/aarch64-base:latest
FROM $BUILD_FROM

# Set metadata labels for Home Assistant addon
LABEL io.hass.type="addon" \
      io.hass.arch="aarch64" \
      io.hass.name="Waveshare PoE HAT (B)" \
      io.hass.description="PoE HAT Support for Raspberry Pi" \
      io.hass.version="1.0.0"

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apk add --no-cache \
    python3 \
    python3-dev \
    py3-pip \
    build-base \
    linux-headers \
    libffi-dev \
    bash \
    i2c-tools \
    freetype-dev \
    libjpeg-turbo-dev \
    zlib-dev \
    musl-dev

# Create virtual environment for Python packages
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install required Python packages inside the virtual environment
RUN pip install --no-cache-dir \
    pillow \
    smbus2

# Copy addon files into container
COPY . .

# Run the addon
CMD ["python3", "/app/bin/main.py"]
