# ============================================
# Dockerfile for STM32F103 Firmware Build Only
# ============================================

# Base image — lightweight Ubuntu
FROM ubuntu:22.04

# -----------------------------
# Install build dependencies
# -----------------------------

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \       
    gcc-arm-none-eabi \ 
    libnewlib-arm-none-eabi \                       
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# -----------------------------
# Set working directory inside container
# -----------------------------
WORKDIR /workspace/firmware

# -----------------------------
# Notes:
# - Firmware source code and Makefile will be mounted at runtime
#   with: 
#       docker run --rm -v ${PWD}:/workspace -w /workspace/firmware stm32devboardcompiler make all
# - Container is purely for reproducible compilation
# - To clean build artifacts, run:
#       docker run --rm -v ${PWD}:/workspace -w /workspace/firmware stm32devboardcompiler make clean all
# -----------------------------
