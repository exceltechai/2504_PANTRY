"""
Pantry & Commissary Recipe Recommendation System
Main Flask application entry point
"""

import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import logging
from datetime import datetime

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
            'upload': '/api/upload',
            'recipes': '/api/recipes'
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
            'POST /api/upload': 'Upload pantry and commissary files',
            'GET /api/recipes': 'Search for recipes',
            'GET /api/recipes/{id}': 'Get recipe details'
        }
    })

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
    """Search for recipes based on available ingredients"""
    try:
        # Get query parameters
        dish_type = request.args.get('type', 'main course')
        cuisine = request.args.get('cuisine', '')
        max_results = int(request.args.get('limit', 10))
        
        # Placeholder response - will be implemented in Phase 2
        return jsonify({
            'recipes': [
                {
                    'id': 1,
                    'title': 'Sample Whole30 Chicken Bowl',
                    'description': 'A healthy chicken bowl with vegetables',
                    'ingredients_available': 8,
                    'ingredients_total': 10,
                    'match_percentage': 80,
                    'sources': {
                        'pantry': 5,
                        'commissary': 3,
                        'store': 2
                    },
                    'url': 'https://example.com/recipe/1'
                }
            ],
            'total_results': 1,
            'query': {
                'type': dish_type,
                'cuisine': cuisine,
                'limit': max_results
            },
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error searching recipes: {str(e)}")
        return jsonify({
            'error': 'Search failed',
            'message': str(e)
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