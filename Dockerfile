# Start with the base image from Docker Hub
FROM runpod/pytorch:2.4.0-py3.11-cuda12.4.1-devel-ubuntu22.04

RUN apt-get update && \
    apt-get install -y --no-install-recommends unzip curl git && \
    curl https://rclone.org/install.sh | bash && \
    git clone https://github.com/xuebinqin/U-2-Net.git workspace/U-2-Net && \
    pip install --no-cache-dir gdown segmentation-refinement && \
    apt-get remove -y git curl && \
    apt-get autoremove -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# pull in google drive images
COPY ./pre_start.sh /pre_start.sh
CMD start.sh

