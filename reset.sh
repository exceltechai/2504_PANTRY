#!/bin/bash

# Project Reset Script
# This script cleans up temporary files and resets the project to a clean state

set -e  # Exit on any error

echo "🧹 Resetting [PROJECT_NAME]..."

# Confirm with user
read -p "⚠️  This will clean up temporary files. Continue? (y/N): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "❌ Reset cancelled."
    exit 1
fi

# [REPLACE: Add your project-specific cleanup commands]

# Common cleanup tasks:
echo "🗑️  Removing temporary files..."

# Remove Python cache files
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find . -type f -name "*.pyc" -delete 2>/dev/null || true
find . -type f -name "*.pyo" -delete 2>/dev/null || true

# Remove Node.js files (if applicable)
# rm -rf node_modules/ 2>/dev/null || true
# rm -f package-lock.json 2>/dev/null || true

# Remove build artifacts
# rm -rf build/ dist/ 2>/dev/null || true

# Remove log files
# rm -f *.log 2>/dev/null || true

# Remove test artifacts
# rm -rf .pytest_cache/ 2>/dev/null || true
# rm -rf coverage/ htmlcov/ 2>/dev/null || true
# rm -f .coverage 2>/dev/null || true

# Remove IDE files (optional - be careful with this)
# rm -rf .vscode/ .idea/ 2>/dev/null || true

# Reset git to clean state (optional - uncomment if needed)
# echo "🔄 Resetting git state..."
# git reset --hard HEAD
# git clean -fd

# Recreate necessary directories
echo "📁 Recreating directories..."
mkdir -p src tests images legacy

echo "✅ Project reset complete!"
echo "💡 Run ./start.sh to restart the project."