ARG BUILD_FROM
FROM $BUILD_FROM

# Set a safe working directory inside the container
WORKDIR /app

# Install system dependencies needed for image processing and numpy
RUN apk add --no-cache \
    openjpeg \
    tiff \
    openblas-dev \
    build-base \
    python3-dev \
    linux-headers \
    libffi-dev

# Upgrade pip using python3 -m pip
RUN python3 -m ensurepip
RUN python3 -m pip install --upgrade pip

# Install Python dependencies
RUN python3 -m pip install --no-cache-dir \
    pillow \
    numpy \
    RPi.GPIO \
    smbus

# Copy add-on files into the container
COPY . /app

# Make sure main script is executable
RUN chmod +x ./bin/main.py

# Run the add-on
CMD ["python3", "./bin/main.py"]
