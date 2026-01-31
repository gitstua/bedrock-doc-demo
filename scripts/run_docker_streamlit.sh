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

# Prepare environment variables arguments
ENV_ARGS=()

# Check if secrets.toml exists and parse it
SECRETS_FILE="$APP_DIR/.streamlit/secrets.toml"
if [ -f "$SECRETS_FILE" ]; then
    echo "Loading secrets from $SECRETS_FILE..."
    while IFS='=' read -r key value; do
        # Skip comments and empty lines
        [[ "$key" =~ ^#.*$ ]] && continue
        [[ -z "$key" ]] && continue

        # Trim whitespace
        key=$(echo "$key" | xargs)
        value=$(echo "$value" | xargs)

        # Remove quotes from value if present
        value="${value%\"}"
        value="${value#\"}"

        if [ -n "$key" ]; then
            ENV_ARGS+=("-e" "$key=$value")
        fi
    done < "$SECRETS_FILE"
else
    echo "No secrets.toml found at $SECRETS_FILE. Skipping environment variables injection."
fi

echo "Running container: $CONTAINER_NAME..."
docker run -d \
    --name "$CONTAINER_NAME" \
    -p 8501:8501 \
    "${ENV_ARGS[@]}" \
    "$@" \
    "$IMAGE_NAME"

echo "Container started. Access the app at http://localhost:8501"
