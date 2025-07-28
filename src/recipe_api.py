"""
/Users/mighk/Documents/2504_PANTRY/src/recipe_api.py
Spoonacular API integration for recipe search and data retrieval
Provides Whole30-compliant recipe searches with detailed ingredient analysis
RELEVANT FILES: app.py, .env, requirements.txt, ingredient_matcher.py
"""

import os
import requests
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import time
from dotenv import load_dotenv

# Load environment variables - specify the path explicitly and override existing
import os.path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
env_path = os.path.join(project_root, '.env')
load_dotenv(env_path, override=True)

logger = logging.getLogger(__name__)

class SpoonacularAPI:
    """
    Spoonacular API client for recipe search and ingredient analysis
    Handles rate limiting, error handling, and data formatting
    """
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.spoonacular.com"
        self.session = requests.Session()
        self.last_request_time = 0
        self.min_request_interval = 0.1  # 100ms between requests to respect rate limits
        
        # Set up session headers
        self.session.headers.update({
            'Content-Type': 'application/json',
            'User-Agent': 'Pantry-Commissary-Recipe-System/1.0'
        })
    
    def _rate_limit_delay(self):
        """
        Enforce rate limiting between API requests
        Spoonacular allows 150 requests per day on free tier
        """
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        
        if time_since_last < self.min_request_interval:
            sleep_time = self.min_request_interval - time_since_last
            logger.debug(f"Rate limiting: sleeping for {sleep_time:.2f} seconds")
            time.sleep(sleep_time)
        
        self.last_request_time = time.time()
    
    def _make_request(self, endpoint: str, params: Dict[str, Any]) -> Optional[Dict]:
        """
        Make authenticated request to Spoonacular API with error handling
        """
        self._rate_limit_delay()
        
        # Add API key to parameters
        params['apiKey'] = self.api_key
        
        url = f"{self.base_url}{endpoint}"
        
        try:
            logger.info(f"Making request to: {endpoint}")
            logger.debug(f"Request parameters: {params}")
            
            response = self.session.get(url, params=params, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            logger.info(f"Successfully received {len(data.get('results', []))} results")
            
            return data
            
        except requests.exceptions.HTTPError as e:
            if response.status_code == 402:
                logger.error("Spoonacular API quota exceeded")
                raise Exception("API quota exceeded. Please upgrade your Spoonacular plan.")
            elif response.status_code == 401:
                logger.error("Invalid Spoonacular API key")
                raise Exception("Invalid API key. Please check your Spoonacular configuration.")
            else:
                logger.error(f"HTTP error {response.status_code}: {e}")
                raise Exception(f"API request failed: {e}")
                
        except requests.exceptions.Timeout:
            logger.error("API request timed out")
            raise Exception("API request timed out. Please try again.")
            
        except requests.exceptions.ConnectionError:
            logger.error("Failed to connect to Spoonacular API")
            raise Exception("Unable to connect to recipe service. Please check your internet connection.")
            
        except Exception as e:
            logger.error(f"Unexpected API error: {str(e)}")
            raise Exception(f"Recipe search failed: {str(e)}")
    
    def search_recipes(self, 
                      query: str = "",
                      dish_type: str = "",
                      cuisine: str = "",
                      diet: str = "whole30",
                      intolerances: str = "",
                      include_ingredients: List[str] = None,
                      number: int = 10,
                      offset: int = 0) -> Dict[str, Any]:
        """
        Search for recipes using Spoonacular's complex search endpoint
        
        Args:
            query: General search query
            dish_type: Type of dish (breakfast, lunch, dinner, etc.)
            cuisine: Cuisine type (mediterranean, asian, etc.)
            diet: Diet restriction (whole30, paleo, etc.)
            intolerances: Food intolerances to exclude
            include_ingredients: List of ingredients that must be included
            number: Number of recipes to return (max 100)
            offset: Number of recipes to skip (for pagination)
        
        Returns:
            Dict containing recipe search results
        """
        endpoint = "/recipes/complexSearch"
        
        params = {
            'number': min(number, 100),  # API limit
            'offset': offset,
            'addRecipeInformation': True,
            'addRecipeNutrition': False,  # Skip nutrition to save API calls
            'fillIngredients': True,
            'sort': 'popularity',  # Sort by popularity for better results
        }
        
        # Add search parameters if provided
        if query:
            params['query'] = query
        if dish_type:
            params['type'] = dish_type
        if cuisine:
            params['cuisine'] = cuisine
        if diet:
            params['diet'] = diet
        if intolerances:
            params['intolerances'] = intolerances
        if include_ingredients:
            params['includeIngredients'] = ','.join(include_ingredients)
        
        try:
            data = self._make_request(endpoint, params)
            
            if not data or 'results' not in data:
                logger.warning("No results returned from API")
                return {
                    'recipes': [],
                    'total_results': 0,
                    'query_info': params
                }
            
            # Process and format the results
            processed_recipes = []
            for recipe in data['results']:
                processed_recipe = self._process_recipe_data(recipe)
                if processed_recipe:
                    # Apply cuisine filtering if specified (Spoonacular sometimes returns incorrect cuisines)
                    if cuisine and not self._matches_cuisine_filter(processed_recipe, cuisine):
                        logger.warning(f"Filtering out '{processed_recipe.get('title')}' - doesn't match {cuisine} cuisine")
                        continue
                    processed_recipes.append(processed_recipe)
            
            return {
                'recipes': processed_recipes,
                'total_results': data.get('totalResults', len(processed_recipes)),
                'number': data.get('number', len(processed_recipes)),
                'offset': data.get('offset', offset),
                'query_info': params,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Recipe search failed: {str(e)}")
            raise
    
    def get_recipe_details(self, recipe_id: int) -> Dict[str, Any]:
        """
        Get detailed information about a specific recipe
        """
        endpoint = f"/recipes/{recipe_id}/information"
        
        params = {
            'includeNutrition': False
        }
        
        try:
            data = self._make_request(endpoint, params)
            return self._process_recipe_data(data) if data else None
            
        except Exception as e:
            logger.error(f"Failed to get recipe details for ID {recipe_id}: {str(e)}")
            raise
    
    def _matches_cuisine_filter(self, recipe: Dict[str, Any], requested_cuisine: str) -> bool:
        """
        Check if a recipe actually matches the requested cuisine.
        This is needed because Spoonacular sometimes returns recipes from wrong cuisines,
        especially when combining cuisine filters with diet restrictions.
        """
        title = recipe.get('title', '').lower()
        requested_cuisine = requested_cuisine.lower()
        
        # Define cuisine exclusion patterns
        cuisine_exclusions = {
            'asian': [
                'jamaican', 'caribbean', 'jerk', 'trinidadian', 'cuban', 'mexican',
                'peruvian', 'brazilian', 'argentinian', 'ethiopian', 'moroccan'
            ],
            'mediterranean': [
                'jamaican', 'caribbean', 'asian', 'chinese', 'japanese', 'korean',
                'thai', 'vietnamese', 'mexican', 'indian', 'trinidadian'
            ],
            'mexican': [
                'asian', 'chinese', 'italian', 'jamaican', 'indian', 'thai',
                'japanese', 'korean', 'vietnamese', 'mediterranean'
            ]
        }
        
        # Get exclusion patterns for requested cuisine
        exclusions = cuisine_exclusions.get(requested_cuisine, [])
        
        # Check if title contains any excluded cuisine indicators
        for exclusion in exclusions:
            if exclusion in title:
                return False
        
        # Additional specific checks for Asian cuisine
        if requested_cuisine == 'asian':
            # Allow explicitly Asian recipes
            asian_indicators = ['asian', 'chinese', 'japanese', 'korean', 'thai', 'vietnamese', 
                              'teriyaki', 'stir fry', 'stir-fry', 'sesame', 'ginger', 'soy sauce']
            if any(indicator in title for indicator in asian_indicators):
                return True
            
            # Allow Indian/curry recipes only if they don't contain Caribbean/Jamaican indicators
            indian_indicators = ['curry', 'korma', 'tikka', 'masala', 'tandoori']
            if any(indicator in title for indicator in indian_indicators):
                # But exclude if it's clearly Caribbean/Jamaican
                caribbean_indicators = ['jamaican', 'caribbean', 'trinidadian', 'jerk']
                if any(indicator in title for indicator in caribbean_indicators):
                    return False
                return True
        
        # If no specific exclusions found, allow the recipe
        return True
    
    def _process_recipe_data(self, recipe_data: Dict) -> Dict[str, Any]:
        """
        Process and standardize recipe data from Spoonacular API
        """
        try:
            # Extract basic recipe information
            processed = {
                'id': recipe_data.get('id'),
                'title': recipe_data.get('title', 'Unknown Recipe'),
                'image': recipe_data.get('image', ''),
                'summary': self._clean_html(recipe_data.get('summary', '')),
                'ready_in_minutes': recipe_data.get('readyInMinutes', 0),
                'servings': recipe_data.get('servings', 1),
                'source_url': recipe_data.get('sourceUrl', ''),
                'spoonacular_url': recipe_data.get('spoonacularSourceUrl', ''),
                'vegetarian': recipe_data.get('vegetarian', False),
                'vegan': recipe_data.get('vegan', False),
                'gluten_free': recipe_data.get('glutenFree', False),
                'dairy_free': recipe_data.get('dairyFree', False),
                'whole30': recipe_data.get('whole30', False),
                'health_score': recipe_data.get('healthScore', 0),
                'price_per_serving': recipe_data.get('pricePerServing', 0),
            }
            
            # Extract and process ingredients
            ingredients = []
            if 'extendedIngredients' in recipe_data:
                for ingredient in recipe_data['extendedIngredients']:
                    ingredients.append({
                        'id': ingredient.get('id'),
                        'name': ingredient.get('name', ''),
                        'original': ingredient.get('original', ''),
                        'amount': ingredient.get('amount', 0),
                        'unit': ingredient.get('unit', ''),
                        'aisle': ingredient.get('aisle', ''),
                        'consistency': ingredient.get('consistency', ''),
                        'original_name': ingredient.get('originalName', '')
                    })
            
            processed['ingredients'] = ingredients
            processed['ingredients_count'] = len(ingredients)
            
            # Extract cooking instructions if available
            instructions = []
            if 'analyzedInstructions' in recipe_data:
                for instruction_group in recipe_data['analyzedInstructions']:
                    if 'steps' in instruction_group:
                        for step in instruction_group['steps']:
                            instructions.append({
                                'number': step.get('number', 0),
                                'step': step.get('step', '')
                            })
            
            processed['instructions'] = instructions
            
            # Add placeholder fields for ingredient matching (will be filled later)
            processed['ingredient_analysis'] = {
                'pantry_ingredients': [],
                'commissary_ingredients': [],
                'store_ingredients': [],
                'pantry_count': 0,
                'commissary_count': 0,
                'store_count': 0,
                'match_percentage': 0,
                'cost_score': 0
            }
            
            return processed
            
        except Exception as e:
            logger.error(f"Failed to process recipe data: {str(e)}")
            return None
    
    def _clean_html(self, text: str) -> str:
        """
        Remove HTML tags from text (simple implementation)
        """
        if not text:
            return ""
        
        # Simple HTML tag removal - for production, consider using BeautifulSoup
        import re
        clean = re.compile('<.*?>')
        return re.sub(clean, '', text).strip()
    
    def test_connection(self) -> Dict[str, Any]:
        """
        Test API connection and quota status
        """
        try:
            # Use a simple recipe search to test the connection
            result = self.search_recipes(query="chicken", number=1)
            
            return {
                'status': 'success',
                'message': 'API connection successful',
                'recipes_found': len(result.get('recipes', [])),
                'api_key_valid': True,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'message': str(e),
                'api_key_valid': False,
                'timestamp': datetime.now().isoformat()
            }


def get_spoonacular_client() -> SpoonacularAPI:
    """
    Create and return a configured Spoonacular API client
    """
    api_key = os.getenv('SPOONACULAR_API_KEY')
    
    if not api_key or api_key == 'your_spoonacular_api_key_here' or api_key.strip() == '':
        raise ValueError(f"Spoonacular API key not configured. Current value: '{api_key}'. Please set SPOONACULAR_API_KEY in .env file")
    
    return SpoonacularAPI(api_key.strip())