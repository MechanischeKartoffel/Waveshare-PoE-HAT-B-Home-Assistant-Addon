# Use the Home Assistant aarch64 base image
ARG BUILD_FROM=ghcr.io/home-assistant/aarch64-base:latest
FROM $BUILD_FROM

# Set working directory
WORKDIR /app

# Install system dependencies and Python + pip
RUN apk add --no-cache \
    python3 \
    py3-pip \
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
    libsharpyuv

# Upgrade pip
RUN pip3 install --upgrade pip

# Install required Python packages
RUN pip3 install --no-cache-dir \
    pillow \
    numpy \
    RPi.GPIO \
    smbus

# Copy addon files (if any)
COPY . .

# Set default command (optional, depending on your addon)
CMD [ "bash" ]
