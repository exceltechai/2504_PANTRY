#!/bin/bash

# Pantry & Commissary Recipe System Setup Script
# This script sets up the development environment for the first time

set -e  # Exit on any error

echo "⚙️  Setting up Pantry & Commissary Recipe System development environment..."

# Check prerequisites
echo "🔍 Checking prerequisites..."

# Check for Python 3
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed."
    echo "Please install Python 3.8+ from https://python.org"
    exit 1
fi

# Check Python version
python_version=$(python3 --version | cut -d' ' -f2)
echo "✅ Python version: $python_version"

# Check for pip
if ! command -v pip3 &> /dev/null && ! command -v pip &> /dev/null; then
    echo "❌ pip is required but not installed."
    echo "Please install pip with: python3 -m ensurepip --upgrade"
    exit 1
fi

echo "✅ Prerequisites check passed!"

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file..."
    if [ -f .env.example ]; then
        cp .env.example .env
        echo "✅ Created .env from .env.example"
        echo "⚠️  Please edit .env file with your Spoonacular API key before running the project."
    else
        echo "⚠️  No .env.example found. You'll need to create .env manually."
    fi
fi

# Create necessary directories
echo "📁 Creating project directories..."
mkdir -p src/api src/services src/utils frontend/css frontend/js frontend/assets tests/unit tests/integration temp_uploads

# Set up Python virtual environment
echo "🐍 Setting up Python virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✅ Created virtual environment"
fi

# Activate virtual environment and install dependencies
echo "📦 Installing Python dependencies..."
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
echo "✅ Dependencies installed"

# Create basic configuration files
echo "📄 Creating configuration files..."
if [ ! -f "src/__init__.py" ]; then
    touch src/__init__.py
fi

if [ ! -f "tests/__init__.py" ]; then
    touch tests/__init__.py
fi

# Make scripts executable
echo "🔧 Making scripts executable..."
chmod +x *.sh 2>/dev/null || true

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env file with your Spoonacular API key"
echo "2. Get your API key from: https://spoonacular.com/food-api"
echo "3. Run ./start.sh to start the project"
echo ""
echo "📚 Check README.md for detailed usage instructions."