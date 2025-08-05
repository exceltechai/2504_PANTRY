"""
Test suite for the Pantry & Commissary Recipe System Flask app
"""

import pytest
import json
import os
import sys

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from app import app


@pytest.fixture
def client():
    """Create a test client for the Flask app"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_health_endpoint(client):
    """Test the health check endpoint"""
    response = client.get('/health')
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert data['status'] == 'healthy'
    assert 'timestamp' in data
    assert data['version'] == '1.0.0'


def test_home_endpoint(client):
    """Test the home endpoint"""
    response = client.get('/')
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert data['project'] == 'Pantry & Commissary Recipe Recommendation System'
    assert data['status'] == 'running'
    assert 'endpoints' in data
    assert 'timestamp' in data


def test_api_info_endpoint(client):
    """Test the API info endpoint"""
    response = client.get('/api/info')
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert data['name'] == 'Pantry & Commissary Recipe API'
    assert data['version'] == '1.0.0'
    assert 'features' in data
    assert 'endpoints' in data


def test_recipes_endpoint(client):
    """Test the recipes search endpoint"""
    response = client.get('/api/recipes?type=breakfast&limit=5')
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert 'recipes' in data
    assert 'total_results' in data
    assert 'query' in data
    assert 'timestamp' in data
    
    # Check query parameters
    assert data['query']['type'] == 'breakfast'
    assert data['query']['limit'] == 5


def test_upload_endpoint_no_files(client):
    """Test the upload endpoint with no files"""
    response = client.post('/api/upload')
    assert response.status_code == 400
    
    data = json.loads(response.data)
    assert 'error' in data
    assert data['error'] == 'No files uploaded'


def test_upload_endpoint_with_files(client):
    """Test the upload endpoint with files"""
    data = {
        'pantry': (open(__file__, 'rb'), 'test_pantry.csv'),
        'commissary': (open(__file__, 'rb'), 'test_commissary.csv')
    }
    
    response = client.post('/api/upload', data=data, content_type='multipart/form-data')
    assert response.status_code == 200
    
    result = json.loads(response.data)
    assert 'message' in result
    assert result['message'] == 'Files uploaded successfully'
    assert 'files_processed' in result
    assert len(result['files_processed']) == 2


def test_404_error(client):
    """Test 404 error handling"""
    response = client.get('/nonexistent-endpoint')
    assert response.status_code == 404
    
    data = json.loads(response.data)
    assert data['error'] == 'Not found'
    assert 'message' in data


if __name__ == '__main__':
    pytest.main([__file__])