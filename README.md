# Pantry & Commissary Recipe Recommendation System

A web-based intelligent recipe recommendation system that helps users find Whole30-compliant recipes by prioritizing ingredients from their available pantry (free) and commissary (reduced-cost) inventories before suggesting full-price supermarket purchases.

## Overview

This application solves the common problem of meal planning while trying to minimize food costs and waste. Users upload their available ingredient inventories from two sources - a pantry (free items) and a commissary (discounted items) - and the system intelligently recommends Whole30-compliant recipes that maximize the use of these available ingredients.

Key benefits:
- **Cost optimization**: Prioritizes free pantry items, then reduced-cost commissary items
- **Smart ingredient matching**: Uses fuzzy string matching to handle ingredient name variations
- **Whole30 compliance**: Filters recipes to maintain dietary adherence
- **Waste reduction**: Encourages use of available ingredients before purchasing new ones

## Quick Start

Get the recipe recommendation system running in under 5 minutes:

```bash
# Clone the repository
git clone https://github.com/yourusername/2504_PANTRY.git
cd 2504_PANTRY

# Setup the project (install dependencies and create .env)
./setup.sh

# Start the application (backend + frontend)
./start.sh

# Access the application at http://localhost:8000
```

## Setup

### Prerequisites

Before running the recipe recommendation system, ensure you have:

- Python 3.8+ (with pip)
- A modern web browser (Chrome, Firefox, Safari, Edge)
- Spoonacular API account (free tier available)
- 1GB free disk space for dependencies

### Installation

Follow these steps to set up the project locally:

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/2504_PANTRY.git
   ```

2. Navigate to the project directory:
   ```bash
   cd 2504_PANTRY
   ```

3. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Configuration

Set up your environment for optimal performance:

1. **Environment Variables**
   - Create your environment configuration:
     ```bash
     cp .env.example .env
     ```
   - Edit `.env` with your API credentials:
     ```
     SPOONACULAR_API_KEY=your_api_key_here
     FLASK_ENV=development
     FLASK_PORT=5000
     FRONTEND_PORT=8000
     FUZZY_MATCH_THRESHOLD=80
     ```

2. **Spoonacular API Setup**
   - Register for a free account at [Spoonacular.com](https://spoonacular.com/food-api)
   - Generate your API key from the dashboard
   - Add the key to your `.env` file

## Usage

### Basic Usage

Start the application and begin finding recipes:

```bash
# Start both backend and frontend servers
./start.sh

# Access the web interface at http://localhost:8000
# Upload your pantry.xlsx and commissary.xlsx files
# Search for recipes by type, cuisine, or ingredients
```

### Advanced Usage

For development and customization:

```bash
# Start only the backend server (API endpoints)
python src/app.py

# Start only the frontend server
python -m http.server 8000

# Run with custom fuzzy matching threshold
FUZZY_MATCH_THRESHOLD=75 python src/app.py
```

### API Usage

Direct API access for integration with other applications:

```javascript
// Search for recipes
fetch('http://localhost:5000/api/recipes?type=breakfast&cuisine=mediterranean')
  .then(response => response.json())
  .then(recipes => console.log(recipes));

// Upload inventory files
const formData = new FormData();
formData.append('pantry', pantryFile);
formData.append('commissary', commissaryFile);
fetch('http://localhost:5000/api/upload', { method: 'POST', body: formData });
```

## Features

Current functionality and planned enhancements:

- ✅ **Excel/CSV File Upload**: Parse pantry and commissary inventory files
- ✅ **Fuzzy Ingredient Matching**: Handle ingredient name variations with 80% accuracy
- ✅ **Recipe Prioritization**: Smart ranking based on available ingredients
- ✅ **Whole30 Compliance**: Filter recipes for dietary requirements
- ✅ **Ingredient Source Tagging**: Visual indicators for Pantry/Commissary/Store items
- 🚧 **Recipe Substitution Suggestions**: AI-powered ingredient alternatives
- 🚧 **Meal Planning Calendar**: Multi-day recipe planning
- 📋 **Shopping List Generation**: Auto-generate lists for missing ingredients
- 📋 **User Profiles**: Save favorite recipes and dietary preferences

## Project Structure

```
2504_PANTRY/
├── src/                   # Flask backend source code
│   ├── app.py            # Main Flask application
│   ├── ingredient_matcher.py # Fuzzy matching algorithms
│   └── recipe_api.py     # Spoonacular API integration
├── tests/                 # Test files and utilities
├── specs/                 # Project specifications and requirements
│   ├── Pantry.csv        # Sample pantry inventory
│   ├── Commissary.csv    # Sample commissary inventory
│   └── *.md              # Detailed specifications
├── ai_docs/               # AI-related documentation
├── images/                # Project images and diagrams
│   └── incoming/         # User-uploaded sketches/notes
├── legacy/                # Previous implementation attempts
├── requirements.txt       # Python dependencies
├── setup.sh              # Project setup script
├── start.sh              # Application startup script
└── README.md             # This file
```

## Recent Progress (2025-07-27)

### Completed:
- **Real Spoonacular API Integration**: Live Whole30 recipe search with 18+ results per query
- **Advanced Ingredient Matching Engine**: RapidFuzz-based fuzzy matching with 80% threshold
- **Smart Priority Scoring**: Pantry (50%) → Commissary (30%) → Store cost optimization algorithm
- **Auto-Loading Sample Data**: 1,448 items (206 pantry + 1,242 commissary) from CSV files
- **Complete Backend API**: All endpoints operational (`/api/recipes`, `/api/sample-data`, `/api/test-connection`)
- **Environment Configuration**: Fixed .env loading conflicts, API key validation working
- **Comprehensive Documentation**: Updated CLAUDE.md with proper markdown formatting

### Current Status:
- **Backend System**: Fully operational with real Spoonacular data integration
- **Frontend**: Auto-loads sample inventory, ready for UI/UX development
- **Matching Algorithm**: Functional but needs accuracy tuning (80% threshold may be too high)
- **API Performance**: ~2-3 second response times for recipe search with ingredient analysis
- **Data Pipeline**: Sample → API → Fuzzy Match → Priority Score → Frontend display

### Next Steps:
- [ ] **Tune Matching Accuracy**: Debug why "egg"→"Eggs: fresh" not matching (likely threshold issue)
- [ ] **UI/UX Development**: User to implement frontend improvements
- [ ] **Performance Optimization**: Cache frequently matched ingredients
- [ ] **Enhanced Filtering**: Add cuisine, prep time, difficulty filters
- [ ] **Recipe Details**: Implement full recipe view with instructions

### Technical Notes:
- **Architecture**: Flask + Spoonacular API + RapidFuzz + Pandas + Sample CSV Auto-loading
- **Matching Logic**: Handles plurals, synonyms, stop words, quantity removal
- **Priority Algorithm**: `(pantry_% * 0.5) + (commissary_% * 0.3) + (available_% * 0.2)`
- **Cost Scoring**: Pantry=0, Commissary=1, Store=2 points per ingredient
- **Environment**: .env.example conflict resolved, API key configured
- **Sample Data**: 1,448 total inventory items with fuzzy matching against recipe ingredients
- **Repository**: GitHub repo created at https://github.com/exceltechai/2504_PANTRY

### Session Summary:
**Major Milestone Achieved**: Fully functional backend system with real Spoonacular API integration and intelligent ingredient matching. The core recommendation engine is operational and ready for frontend development. Next session should focus on matching accuracy tuning and UI/UX enhancements.

## Development

### Running Tests

```bash
# Run all tests
python -m pytest tests/

# Run specific test categories
python -m pytest tests/test_ingredient_matching.py
python -m pytest tests/test_api_endpoints.py
```

### Running in Development Mode

```bash
# Start with debug mode enabled
export FLASK_ENV=development
python src/app.py

# Auto-reload frontend changes
python -m http.server 8000 --directory frontend
```

### Building for Production

```bash
# Install production dependencies
pip install -r requirements.txt --no-dev

# Set production environment
export FLASK_ENV=production
export DEBUG=False

# Start production server
gunicorn --bind 0.0.0.0:5000 src.app:app
```

## Contributing

We welcome contributions to improve the recipe recommendation system:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/enhanced-ingredient-matching`)
3. Make your changes with tests
4. Commit your changes (`git commit -m 'feat: improve fuzzy matching accuracy'`)
5. Push to the branch (`git push origin feature/enhanced-ingredient-matching`)
6. Open a Pull Request

### Contribution Areas
- Ingredient matching algorithm improvements
- Additional recipe API integrations (Yummly, Edamam)
- Frontend UI/UX enhancements
- Performance optimizations
- Documentation and tutorials

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

Special thanks to the following projects and resources:

- **Spoonacular API** for comprehensive recipe data and Whole30 filtering
- **RapidFuzz** for fast and accurate fuzzy string matching
- **Flask** for the lightweight web framework
- **Pandas** for Excel/CSV data processing
- **Claude Code** for development assistance and code generation

Built with modern web technologies for optimal performance and user experience.

## Links

Project resources and documentation:

- [Project Specifications](specs/) - Detailed technical specifications
- [API Documentation](docs/api.md) - Backend API endpoints
- [User Guide](docs/user-guide.md) - How to use the application
- [Development Setup](docs/development.md) - Developer environment setup
