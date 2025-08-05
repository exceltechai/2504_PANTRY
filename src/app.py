"""
Pantry & Commissary Recipe Recommendation System
Main Flask application entry point
"""

import os
import pandas as pd
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import logging
from datetime import datetime
from recipe_api import get_spoonacular_client
from ingredient_matcher import create_ingredient_matcher

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for frontend communication

# Configure logging
logging.basicConfig(
    level=getattr(logging, os.getenv('LOG_LEVEL', 'INFO')),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configuration
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')
app.config['UPLOAD_FOLDER'] = os.getenv('UPLOAD_FOLDER', 'temp_uploads')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize Spoonacular API client
try:
    spoonacular_client = get_spoonacular_client()
    logger.info("Spoonacular API client initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize Spoonacular API client: {str(e)}")
    spoonacular_client = None

# Initialize ingredient matcher
try:
    ingredient_matcher = create_ingredient_matcher()
    logger.info("Ingredient matcher initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize ingredient matcher: {str(e)}")
    ingredient_matcher = None

# Sample data functions
def load_sample_data():
    """Load actual pantry and commissary data from CSV files"""
    try:
        import pandas as pd
        
        # Load actual pantry data
        pantry_file = os.path.join(os.path.dirname(__file__), '..', 'specs', 'Pantry.csv')
        pantry_df = pd.read_csv(pantry_file, encoding='utf-8-sig')  # Handle BOM
        pantry_data = pantry_df.to_dict('records')
        
        # Load actual commissary data  
        commissary_file = os.path.join(os.path.dirname(__file__), '..', 'specs', 'Commissary.csv')
        commissary_df = pd.read_csv(commissary_file, encoding='utf-8-sig')  # Handle BOM
        commissary_data = commissary_df.to_dict('records')
        
        # Clean up any empty columns that might have been added by pandas
        pantry_data = [{k: v for k, v in item.items() if pd.notna(v) and k.strip()} for item in pantry_data]
        commissary_data = [{k: v for k, v in item.items() if pd.notna(v) and k.strip()} for item in commissary_data]
        
        logger.info(f"Loaded {len(pantry_data)} pantry items and {len(commissary_data)} commissary items from CSV files")
            
        return {
            'pantry': pantry_data,
            'commissary': commissary_data,
            'status': 'success',
            'summary': {
                'pantry_count': len(pantry_data),
                'commissary_count': len(commissary_data),
                'total_items': len(pantry_data) + len(commissary_data)
            },
            'timestamp': datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error loading CSV data: {str(e)}")
        return {
            'pantry': [],
            'commissary': [],
            'status': 'error',
            'error': str(e),
            'summary': {
                'pantry_count': 0,
                'commissary_count': 0,
                'total_items': 0
            },
            'timestamp': datetime.now().isoformat()
        }

@app.route('/')
def home():
    """Serve the frontend application"""
    try:
        frontend_path = os.path.join(os.path.dirname(__file__), '..', 'frontend', 'index.html')
        with open(frontend_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return content, 200, {'Content-Type': 'text/html'}
    except FileNotFoundError:
        # Fallback to API info if frontend not found
        return jsonify({
            'project': 'Pantry & Commissary Recipe Recommendation System',
            'version': '1.0.0',
            'status': 'running',
            'timestamp': datetime.now().isoformat(),
            'endpoints': {
                'health': '/health',
                'api_info': '/api/info',
                'sample_data': '/api/sample-data',
                'upload': '/api/upload',
                'recipes': '/api/recipes',
                'recipe_details': '/api/recipes/{id}',
                'test_api': '/api/test-connection'
            }
        })

# Serve static files
@app.route('/js/<path:filename>')
def serve_js(filename):
    """Serve JavaScript files"""
    try:
        js_path = os.path.join(os.path.dirname(__file__), '..', 'frontend', 'js', filename)
        with open(js_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return content, 200, {'Content-Type': 'application/javascript'}
    except FileNotFoundError:
        return "File not found", 404

@app.route('/css/<path:filename>')
def serve_css(filename):
    """Serve CSS files"""
    try:
        css_path = os.path.join(os.path.dirname(__file__), '..', 'frontend', 'css', filename)
        with open(css_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return content, 200, {'Content-Type': 'text/css'}
    except FileNotFoundError:
        return "File not found", 404

@app.route('/health')
def health_check():
    """Health check endpoint for monitoring"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0'
    })

@app.route('/api/info')
def api_info():
    """API information endpoint"""
    return jsonify({
        'name': 'Pantry & Commissary Recipe API',
        'version': '1.0.0',
        'description': 'Recipe recommendation system that prioritizes pantry and commissary ingredients',
        'features': [
            'File upload (Excel/CSV)',
            'Fuzzy ingredient matching',
            'Whole30 recipe filtering',
            'Smart ingredient prioritization'
        ],
        'endpoints': {
            'GET /api/sample-data': 'Get actual pantry and commissary availability data',
            'POST /api/upload': 'Upload pantry and commissary files',
            'GET /api/recipes': 'Search for Whole30 recipes',
            'GET /api/recipes/{id}': 'Get detailed recipe information',
            'GET /api/test-connection': 'Test Spoonacular API connection'
        }
    })

@app.route('/api/sample-data')
def get_sample_data():
    """Get actual pantry and commissary data from CSV files"""
    try:
        sample_data = load_sample_data()
        
        # Add summary statistics
        sample_data['summary'] = {
            'pantry_count': len(sample_data['pantry']),
            'commissary_count': len(sample_data['commissary']),
            'total_items': len(sample_data['pantry']) + len(sample_data['commissary'])
        }
        
        return jsonify(sample_data)
        
    except Exception as e:
        logger.error(f"Error getting sample data: {str(e)}")
        return jsonify({
            'error': 'Failed to load sample data',
            'message': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

@app.route('/api/upload', methods=['POST'])
def upload_files():
    """Upload and process pantry/commissary files"""
    try:
        # Check if files were uploaded
        if 'pantry' not in request.files and 'commissary' not in request.files:
            return jsonify({
                'error': 'No files uploaded',
                'message': 'Please upload at least one file (pantry or commissary)'
            }), 400
        
        result = {
            'message': 'Files uploaded successfully',
            'files_processed': [],
            'timestamp': datetime.now().isoformat()
        }
        
        # Process pantry file if uploaded
        if 'pantry' in request.files:
            pantry_file = request.files['pantry']
            if pantry_file.filename:
                result['files_processed'].append({
                    'type': 'pantry',
                    'filename': pantry_file.filename,
                    'status': 'received'
                })
        
        # Process commissary file if uploaded
        if 'commissary' in request.files:
            commissary_file = request.files['commissary']
            if commissary_file.filename:
                result['files_processed'].append({
                    'type': 'commissary',
                    'filename': commissary_file.filename,
                    'status': 'received'
                })
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Error uploading files: {str(e)}")
        return jsonify({
            'error': 'Upload failed',
            'message': str(e)
        }), 500

@app.route('/api/recipes', methods=['GET'])
def search_recipes():
    """Search for Whole30-compliant recipes using Spoonacular API"""
    try:
        # Check if Spoonacular client is available
        if not spoonacular_client:
            return jsonify({
                'error': 'Recipe service unavailable',
                'message': 'Spoonacular API not configured properly'
            }), 503
        
        # Get query parameters
        query = request.args.get('query', '')
        dish_type = request.args.get('type', 'main course')
        cuisine_input = request.args.get('cuisine', '')
        max_results = int(request.args.get('limit', 10))
        offset = int(request.args.get('offset', 0))
        
        # Smart handling of cuisine input - detect if it's a cuisine or flavor profile
        known_cuisines = ['mediterranean', 'asian', 'mexican', 'italian', 'indian', 'thai', 'chinese', 'japanese', 'french', 'greek']
        flavor_profiles = ['spicy', 'mild', 'sweet', 'savory', 'hot', 'tangy', 'smoky', 'herbal']
        
        cuisine = ''
        search_query = query
        
        if cuisine_input:
            cuisine_lower = cuisine_input.lower()
            if any(known_cuisine in cuisine_lower for known_cuisine in known_cuisines):
                # It's a cuisine
                cuisine = cuisine_input
            elif any(flavor in cuisine_lower for flavor in flavor_profiles):
                # It's a flavor profile - use as query instead
                search_query = cuisine_input if not query else f"{query} {cuisine_input}"
            else:
                # Unknown - try both
                cuisine = cuisine_input
                search_query = cuisine_input if not query else f"{query} {cuisine_input}"
        
        logger.info(f"Searching recipes: type={dish_type}, cuisine={cuisine}, query={search_query}, limit={max_results}")
        
        # Search recipes using Spoonacular API with Whole30 filter
        search_result = spoonacular_client.search_recipes(
            query=search_query,
            dish_type=dish_type,
            cuisine=cuisine,
            diet='whole30',  # Force Whole30 compliance
            number=max_results,
            offset=offset
        )
        
        # Load current inventory for ingredient matching
        sample_data = load_sample_data()
        if sample_data['status'] == 'success' and ingredient_matcher:
            pantry_items = sample_data['pantry']
            commissary_items = sample_data['commissary']
            
            # Analyze each recipe for ingredient matches and priority scoring
            analyzed_recipes = []
            for recipe in search_result['recipes']:
                analyzed_recipe = ingredient_matcher.match_recipe_ingredients(
                    recipe, pantry_items, commissary_items
                )
                analyzed_recipes.append(analyzed_recipe)
            
            # Sort recipes by priority score (pantry > commissary > store)
            analyzed_recipes = ingredient_matcher.sort_recipes_by_priority(analyzed_recipes)
            search_result['recipes'] = analyzed_recipes
            
            logger.info(f"Analyzed {len(analyzed_recipes)} recipes with ingredient matching")
        
        # Format response for frontend
        response = {
            'recipes': search_result['recipes'],
            'total_results': search_result.get('total_results', 0),
            'number': search_result.get('number', len(search_result['recipes'])),
            'offset': search_result.get('offset', offset),
            'query': {
                'query': query,
                'type': dish_type,
                'cuisine': cuisine,
                'limit': max_results,
                'diet': 'whole30'
            },
            'timestamp': search_result.get('timestamp', datetime.now().isoformat())
        }
        
        logger.info(f"Found {len(search_result['recipes'])} Whole30 recipes")
        
        return jsonify(response)
        
    except Exception as e:
        logger.error(f"Error searching recipes: {str(e)}")
        return jsonify({
            'error': 'Search failed',
            'message': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

@app.route('/api/recipes/<int:recipe_id>')
def get_recipe_details(recipe_id):
    """Get detailed information about a specific recipe"""
    try:
        # Check if Spoonacular client is available
        if not spoonacular_client:
            return jsonify({
                'error': 'Recipe service unavailable',
                'message': 'Spoonacular API not configured properly'
            }), 503
        
        logger.info(f"Getting details for recipe ID: {recipe_id}")
        
        # Get recipe details from Spoonacular API
        recipe_details = spoonacular_client.get_recipe_details(recipe_id)
        
        if not recipe_details:
            return jsonify({
                'error': 'Recipe not found',
                'message': f'Recipe with ID {recipe_id} not found'
            }), 404
        
        return jsonify({
            'recipe': recipe_details,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error getting recipe details for ID {recipe_id}: {str(e)}")
        return jsonify({
            'error': 'Failed to get recipe details',
            'message': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

@app.route('/api/test-connection')
def test_api_connection():
    """Test connection to Spoonacular API"""
    try:
        if not spoonacular_client:
            return jsonify({
                'status': 'error',
                'message': 'Spoonacular API client not initialized',
                'api_configured': False,
                'timestamp': datetime.now().isoformat()
            }), 503
        
        # Test API connection
        test_result = spoonacular_client.test_connection()
        
        if test_result['status'] == 'success':
            return jsonify(test_result)
        else:
            return jsonify(test_result), 503
            
    except Exception as e:
        logger.error(f"Error testing API connection: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': str(e),
            'api_configured': False,
            'timestamp': datetime.now().isoformat()
        }), 500

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        'error': 'Not found',
        'message': 'The requested endpoint was not found'
    }), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({
        'error': 'Internal server error',
        'message': 'Something went wrong on our end'
    }), 500

if __name__ == '__main__':
    # Use PORT environment variable for deployment platforms like Render
    port = int(os.getenv('PORT', os.getenv('FLASK_PORT', 5000)))
    debug = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    
    logger.info(f"Starting Pantry & Commissary Recipe System on port {port}")
    logger.info(f"Debug mode: {debug}")
    
    app.run(
        host='0.0.0.0',
        port=port,
        debug=debug
    )