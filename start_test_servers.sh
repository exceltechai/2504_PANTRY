#!/bin/bash

# Start test servers for Playwright testing
# This script starts both the Flask backend and the frontend server

echo "Starting Pantry & Commissary Recipe System servers for testing..."

# Function to cleanup processes on exit
cleanup() {
    echo "Shutting down servers..."
    if [ ! -z "$BACKEND_PID" ]; then
        kill $BACKEND_PID 2>/dev/null
    fi
    if [ ! -z "$FRONTEND_PID" ]; then
        kill $FRONTEND_PID 2>/dev/null
    fi
    exit
}

# Set trap to cleanup on script exit
trap cleanup EXIT

# Start Flask backend
echo "Starting Flask backend on port 5001..."
cd "$(dirname "$0")"
export FLASK_ENV=development
export FLASK_PORT=5001
python src/app.py &
BACKEND_PID=$!

# Wait for backend to start
sleep 3

# Check if backend is running
if ! curl -s http://localhost:5001/health > /dev/null; then
    echo "Error: Backend failed to start"
    exit 1
fi

echo "Backend started successfully (PID: $BACKEND_PID)"

# Start frontend server
echo "Starting frontend server on port 8000..."
cd frontend
python -m http.server 8000 &
FRONTEND_PID=$!

# Wait for frontend to start
sleep 2

# Check if frontend is running
if ! curl -s http://localhost:8000 > /dev/null; then
    echo "Error: Frontend failed to start"
    exit 1
fi

echo "Frontend started successfully (PID: $FRONTEND_PID)"
echo ""
echo "Servers are ready for testing:"
echo "  - Backend API: http://localhost:5001"
echo "  - Frontend:    http://localhost:8000"
echo ""
echo "Press Ctrl+C to stop all servers"

# Keep script running
wait