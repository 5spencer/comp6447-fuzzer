FROM --platform=linux/amd64 ubuntu:22.04

# Install dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Copy your fuzzer
COPY fuzzer.py /fuzzer.py
RUN chmod +x /fuzzer.py

# Set the entrypoint
ENTRYPOINT ["python3", "/fuzzer.py"]