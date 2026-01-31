#!/bin/bash
set -e

# Change to the root directory
cd "$(dirname "$0")/.."

echo "Starting all services..."

# Run Streamlit (already runs in -d mode)
./scripts/run_docker_streamlit.sh

# Run Vue (pass -d to run in background)
./scripts/run_docker_vue.sh -d

echo ""
echo "Services started:"
echo "- Streamlit App: http://localhost:8501"
echo "- Vue Frontend: http://localhost:80"
echo "- Vue Backend: http://localhost:8000/health"
echo ""
echo "Note: Vue Frontend is running on port 80 as per vueapp/docker-compose.yml"
