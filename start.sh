#!/bin/bash

# Pantry & Commissary Recipe System Startup Script
# This script starts both the backend and frontend servers

set -e  # Exit on any error

echo "🚀 Starting Pantry & Commissary Recipe System..."

# Check if .env file exists
if [ ! -f .env ]; then
    echo "⚠️  No .env file found. Creating from .env.example..."
    if [ -f .env.example ]; then
        cp .env.example .env
        echo "✅ Created .env file. Please edit it with your Spoonacular API key."
        echo "💡 Get your API key from: https://spoonacular.com/food-api"
        exit 1
    else
        echo "❌ No .env.example file found. Please run ./setup.sh first."
        exit 1
    fi
fi

# Load environment variables
if [ -f .env ]; then
    export $(cat .env | grep -v '^#' | xargs)
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found. Please run ./setup.sh first."
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

# Check if Flask app exists
if [ ! -f "src/app.py" ]; then
    echo "❌ Flask app not found. Please ensure src/app.py exists."
    exit 1
fi

# Check if API key is configured
if [ "$SPOONACULAR_API_KEY" = "your_spoonacular_api_key_here" ]; then
    echo "⚠️  Please configure your Spoonacular API key in .env file"
    echo "💡 Get your API key from: https://spoonacular.com/food-api"
    exit 1
fi

# Create upload folder if it doesn't exist
mkdir -p temp_uploads

# Function to cleanup background processes
cleanup() {
    echo "🧹 Cleaning up..."
    kill $(jobs -p) 2>/dev/null || true
    exit 0
}

# Set up signal handlers
trap cleanup SIGINT SIGTERM

echo "🔧 Starting backend server..."
python src/app.py &
BACKEND_PID=$!

# Wait a moment for backend to start
sleep 2

echo "🌐 Starting frontend server..."
python -m http.server ${FRONTEND_PORT:-8000} --directory frontend &
FRONTEND_PID=$!

echo ""
echo "✅ Pantry & Commissary Recipe System is ready!"
echo ""
echo "🔗 Backend API: http://localhost:${FLASK_PORT:-5001}"
echo "🌐 Frontend:    http://localhost:${FRONTEND_PORT:-8000}"
echo ""
echo "📊 To test the API:"
echo "curl http://localhost:${FLASK_PORT:-5001}/health"
echo ""
echo "Press Ctrl+C to stop both servers"

# Wait for background processes
wait