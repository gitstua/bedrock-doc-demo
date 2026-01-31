#!/bin/bash

# Navigate to the directory where the script is located
cd "$(dirname "$0")"

# Check if backend/.env exists
if [ -f backend/.env ]; then
    echo "Loading environment variables from backend/.env..."
    # Export variables from .env file, ignoring comments
    export $(grep -v '^#' backend/.env | xargs)
else
    echo "Warning: backend/.env file not found. Ensure you have created it from backend/.env.example"
fi

echo "Starting Docker containers..."
docker-compose up --build
