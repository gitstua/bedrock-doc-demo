#!/bin/bash
set -e

# Change to the root directory
cd "$(dirname "$0")/.."

echo "Building all Docker images using docker-compose..."
docker-compose build

echo "Build complete."
