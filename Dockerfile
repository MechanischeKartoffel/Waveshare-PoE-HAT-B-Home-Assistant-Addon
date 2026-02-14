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

# Install system dependencies and I2C/GPIO tools
RUN apk add --no-cache \
    python3 \
    py3-virtualenv \
    python3-dev \
    build-base \
    openjpeg \
    tiff \
    openblas-dev \
    linux-headers \
    libffi-dev \
    bash \
    git \
    libjpeg-turbo \
    libwebp \
    libsharpyuv \
    i2c-tools \
    RPi.GPIO \
    smbus \
    udev

# Create virtual environment for Python packages
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install required Python packages inside the virtual environment
RUN pip install --no-cache-dir \
    pillow \
    numpy \
    RPi.GPIO \
    smbus

# Copy addon files into container
COPY . .

# Set permissions for GPIO and I2C access
RUN chmod -R 777 /dev/i2c-* /sys/class/gpio

# Default command (start Bash, can be overridden by addon)
CMD ["bash"]
