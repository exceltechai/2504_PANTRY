# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Pantry & Commissary Recipe Recommendation System**

This is a web-based application that helps users find Whole30-compliant recipes by intelligently prioritizing ingredients from their available inventories. The project enables users to upload pantry (free) and commissary (reduced-cost) ingredient lists, then recommends recipes that maximize usage of these available ingredients before suggesting full-price supermarket purchases. The system is designed to reduce food costs and food waste while maintaining dietary compliance.

## Key Commands

### Running the Project

```bash
# Start the Flask backend
python src/app.py

# Serve frontend (development)
python -m http.server 8000

# Run the complete application
./start.sh

# Run tests
python -m pytest tests/

# Setup project
./setup.sh
```

### Development Commands

```bash
# Install Python dependencies
pip install -r requirements.txt

# Start development backend server
export FLASK_ENV=development && python src/app.py

# Start development frontend server
python -m http.server 8000

# Lint Python code
flake8 src/ tests/

# Format Python code
black src/ tests/
```

## Architecture & Structure

### Directory Structure
- `src/` - Main source code directory (Flask backend)
- `tests/` - Test files and test utilities
- `specs/` - Project specifications and requirements documents
- `ai_docs/` - AI-related documentation and Claude Code tutorials
- `images/` - Project images, diagrams, and visual assets
- `legacy/` - Previous iterations and deprecated code
- `frontend/` - Frontend HTML/CSS/JavaScript files (if separated)

### Configuration Files
- `.env` - Environment variables (Spoonacular API key, etc.) - not committed to git
- `requirements.txt` - Python dependencies
- `setup.sh` - Project setup script
- `start.sh` - Application start script

### Key Implementation Details
- **Backend**: Flask-based API server with Spoonacular integration
- **Frontend**: Responsive HTML/CSS/JavaScript interface with file upload capabilities  
- **Data Processing**: Pandas for Excel/CSV parsing, rapidfuzz/Fuse.js for fuzzy ingredient matching
- **Recipe Prioritization**: Custom algorithm prioritizing Pantry > Commissary > Supermarket ingredients
- **File Handling**: Session-based temporary storage for uploaded inventory files
- **API Integration**: Spoonacular API for Whole30-compliant recipe search and filtering

## Development Guidelines

### Code Style
- Follow PEP 8 for Python code styling
- Use descriptive variable and function names (e.g., `fuzzy_match_ingredient`, `calculate_recipe_score`)
- Add docstrings for all functions, especially ingredient matching and recipe scoring logic
- Maintain consistent indentation (4 spaces for Python, 2 spaces for JavaScript)
- Use type hints in Python functions where applicable

### Testing
- Write tests for ingredient matching algorithms (critical for accuracy)
- Test file upload and parsing functionality with sample Excel/CSV files
- Ensure all tests pass before committing
- Test with different data formats and edge cases (empty ingredients, special characters)

### Git Workflow
- Use descriptive commit messages following format: "feat/fix/docs: description"
- Test recipe matching functionality thoroughly before pushing
- Never commit API keys or sensitive environment variables

## Environment Setup

### Prerequisites
- Python 3.8+ (for Flask backend and data processing)
- Web browser with JavaScript enabled
- Spoonacular API account and API key
- Optional: Node.js (if using package managers for frontend dependencies)

### Installation
1. Clone the repository
2. Run `./setup.sh` or manually install dependencies with `pip install -r requirements.txt`
3. Set up environment variables (see below)
4. Run `./start.sh` to start both backend and frontend servers

### Environment Variables
Create `.env` file in project root and configure:
```
SPOONACULAR_API_KEY=your_spoonacular_api_key_here
FLASK_ENV=development
FLASK_PORT=5000
FRONTEND_PORT=8000
FUZZY_MATCH_THRESHOLD=80
DEBUG=True
```

## References & Documentation

### External Resources
- Watch the `/images/incoming` folder for uploaded sketches and notes relevant to the project
- [Spoonacular API Documentation](https://spoonacular.com/food-api) - Recipe search and nutrition data
- [Flask Documentation](https://flask.palletsprojects.com/) - Web framework
- [Pandas Documentation](https://pandas.pydata.org/docs/) - Excel/CSV data processing
- [RapidFuzz Documentation](https://maxbachmann.github.io/RapidFuzz/) - Fuzzy string matching
- [Fuse.js Documentation](https://fusejs.io/) - Client-side fuzzy search (if using frontend approach)

### Internal Documentation
- See `ai_docs/` for AI-related documentation and Claude Code tutorials
- See `specs/` for detailed project specifications (multiple approaches documented)
- See `legacy/` for previous implementation attempts and lessons learned
- See individual file headers for module-specific documentation

## Project-Specific Implementation Notes

### Core Algorithm Priorities
1. **Ingredient Matching**: Use fuzzy matching with 80% threshold (configurable)
2. **Recipe Scoring**: Prioritize recipes with highest percentage of Pantry ingredients, then Commissary
3. **Whole30 Compliance**: All recipe searches must include Whole30 dietary filter
4. **User Experience**: Minimize file upload friction - provide default sample data

### Data Format Expectations
- **Pantry/Commissary Files**: Excel (.xlsx) or CSV with columns: Item, Category, Vendor, U/M
- **Recipe Results**: JSON format with ingredient source tagging (Pantry/Commissary/Store)
- **Fuzzy Matching**: Handle variations like "scallion" vs "green onion", ingredient plurals

### Performance Considerations
- Cache recipe search results to minimize API calls
- Implement client-side file parsing when possible to reduce server load
- Graceful degradation: lower fuzzy match threshold if no results found at 90%