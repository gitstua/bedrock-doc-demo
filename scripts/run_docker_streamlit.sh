#!/bin/bash
set -e

# Change to the root directory
cd "$(dirname "$0")/.."

APP_DIR="./app"
IMAGE_NAME="streamlit-app"
CONTAINER_NAME="streamlit-app-container"

echo "Building Docker image: $IMAGE_NAME..."
docker build -t "$IMAGE_NAME" "$APP_DIR"

echo "Stopping existing container (if any)..."
docker stop "$CONTAINER_NAME" 2>/dev/null || true
docker rm "$CONTAINER_NAME" 2>/dev/null || true

# Prepare environment variable arguments
ENV_FILE="./.env"
ENV_ARGS=()

if [ -f "$ENV_FILE" ]; then
    echo "Loading environment variables from $ENV_FILE..."
    ENV_ARGS=("--env-file" "$ENV_FILE")
else
    echo "No .env file found at $ENV_FILE. Skipping environment variables injection."
fi

echo "Running container: $CONTAINER_NAME..."
docker run -d \
    --name "$CONTAINER_NAME" \
    -p 8501:8501 \
    "${ENV_ARGS[@]}" \
    "$@" \
    "$IMAGE_NAME"

echo "Container started. Access the app at http://localhost:8501"
