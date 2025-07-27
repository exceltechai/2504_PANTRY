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
    """Load sample pantry and commissary data from CSV files"""
    try:
        # Get the project root directory (parent of src)
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        pantry_path = os.path.join(project_root, 'specs', 'Pantry.csv')
        commissary_path = os.path.join(project_root, 'specs', 'Commissary.csv')
        
        pantry_data = []
        commissary_data = []
        
        # Load pantry data
        if os.path.exists(pantry_path):
            df_pantry = pd.read_csv(pantry_path)
            # Clean the data - remove empty rows and filter valid items
            df_pantry = df_pantry.dropna(subset=['Item'])
            df_pantry = df_pantry[df_pantry['Item'].str.strip() != '']
            pantry_data = df_pantry.to_dict('records')
            logger.info(f"Loaded {len(pantry_data)} pantry items")
        
        # Load commissary data  
        if os.path.exists(commissary_path):
            df_commissary = pd.read_csv(commissary_path)
            # Clean the data - remove empty rows and filter valid items
            df_commissary = df_commissary.dropna(subset=['Item'])
            df_commissary = df_commissary[df_commissary['Item'].str.strip() != '']
            commissary_data = df_commissary.to_dict('records')
            logger.info(f"Loaded {len(commissary_data)} commissary items")
            
        return {
            'pantry': pantry_data,
            'commissary': commissary_data,
            'status': 'success',
            'timestamp': datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error loading sample data: {str(e)}")
        return {
            'pantry': [],
            'commissary': [],
            'status': 'error',
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }

@app.route('/')
def home():
    """Root endpoint with basic project information"""
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
            'GET /api/sample-data': 'Get sample pantry and commissary data',
            'POST /api/upload': 'Upload pantry and commissary files',
            'GET /api/recipes': 'Search for Whole30 recipes',
            'GET /api/recipes/{id}': 'Get detailed recipe information',
            'GET /api/test-connection': 'Test Spoonacular API connection'
        }
    })

@app.route('/api/sample-data')
def get_sample_data():
    """Get sample pantry and commissary data from CSV files"""
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
        cuisine = request.args.get('cuisine', '')
        max_results = int(request.args.get('limit', 10))
        offset = int(request.args.get('offset', 0))
        
        logger.info(f"Searching recipes: type={dish_type}, cuisine={cuisine}, limit={max_results}")
        
        # Search recipes using Spoonacular API with Whole30 filter
        search_result = spoonacular_client.search_recipes(
            query=query,
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
    port = int(os.getenv('FLASK_PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    
    logger.info(f"Starting Pantry & Commissary Recipe System on port {port}")
    logger.info(f"Debug mode: {debug}")
    
    app.run(
        host='0.0.0.0',
        port=port,
        debug=debug
    )