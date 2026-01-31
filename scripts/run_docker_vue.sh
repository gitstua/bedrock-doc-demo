#!/bin/bash

# Navigate to the project root directory (assuming script is in scripts/)
cd "$(dirname "$0")/.."

# Check if vueapp/backend/.env exists
if [ -f vueapp/backend/.env ]; then
    echo "Loading environment variables from vueapp/backend/.env..."
    # Export variables from .env file, ignoring comments
    export $(grep -v '^#' vueapp/backend/.env | xargs)
else
    echo "Warning: vueapp/backend/.env file not found. Ensure you have created it from vueapp/backend/.env.example"
fi

echo "Starting Docker containers..."
# Use -f to specify the compose file location
docker-compose -f vueapp/docker-compose.yml up --build
