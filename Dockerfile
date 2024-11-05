# Start with the base image from Docker Hub
FROM runpod/pytorch:2.4.0-py3.11-cuda12.4.1-devel-ubuntu22.04

# Install additional Python packages
RUN pip install --no-cache-dir gdown xu2net segmentation-refinement && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# pull in google drive images
COPY ./pre_start.sh /pre_start.sh
