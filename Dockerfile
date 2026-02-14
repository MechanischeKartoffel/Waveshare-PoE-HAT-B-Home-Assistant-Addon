ARG BUILD_FROM
FROM $BUILD_FROM

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apk add --no-cache \
    openjpeg \
    tiff \
    openblas-dev

# Install Python dependencies
RUN pip install --no-cache-dir \
    pillow \
    numpy \
    RPi.GPIO \
    smbus

# Copy add-on files
COPY . .

# Run the add-on
CMD ["python3", "./bin/main.py"]
