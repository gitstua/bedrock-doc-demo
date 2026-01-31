#!/bin/bash

# Navigate to the project root directory (assuming script is in scripts/)
cd "$(dirname "$0")/.."

# Check if .env exists in root
if [ -f .env ]; then
    echo "Loading environment variables from .env..."
    # Export variables from .env file, ignoring comments
    export $(grep -v '^#' .env | xargs)
else
    echo "Warning: .env file not found in root. Ensure you have created it from .env.example"
fi

echo "Starting Docker containers..."
# Use -f to specify the compose file location
docker-compose -f vueapp/docker-compose.yml up --build "$@"
