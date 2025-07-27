"""
/Users/mighk/Documents/2504_PANTRY/src/ingredient_matcher.py
Fuzzy string matching engine for comparing recipe ingredients with pantry/commissary items
Handles ingredient variations, plurals, and synonyms with configurable matching thresholds
RELEVANT FILES: app.py, recipe_api.py, .env, requirements.txt
"""

import os
import re
import logging
from typing import Dict, List, Tuple, Optional, Set
from rapidfuzz import fuzz, process
from dotenv import load_dotenv

# Load environment variables
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
env_path = os.path.join(project_root, '.env')
load_dotenv(env_path, override=True)

logger = logging.getLogger(__name__)

class IngredientMatcher:
    """
    Advanced ingredient matching engine using fuzzy string matching
    Handles variations, plurals, synonyms, and cooking-specific transformations
    """
    
    def __init__(self, fuzzy_threshold: int = None):
        self.fuzzy_threshold = fuzzy_threshold or int(os.getenv('FUZZY_MATCH_THRESHOLD', 80))
        
        # Common ingredient synonyms and variations
        self.synonyms = {
            'scallion': ['green onion', 'spring onion'],
            'green onion': ['scallion', 'spring onion'],
            'spring onion': ['scallion', 'green onion'],
            'cilantro': ['coriander', 'chinese parsley'],
            'coriander': ['cilantro', 'chinese parsley'],
            'bell pepper': ['sweet pepper', 'capsicum'],
            'sweet pepper': ['bell pepper', 'capsicum'],
            'zucchini': ['courgette'],
            'courgette': ['zucchini'],
            'eggplant': ['aubergine'],
            'aubergine': ['eggplant'],
            'romaine': ['romaine lettuce', 'cos lettuce'],
            'romaine lettuce': ['romaine', 'cos lettuce'],
            'ground beef': ['beef mince', 'minced beef'],
            'beef mince': ['ground beef', 'minced beef'],
            'ground turkey': ['turkey mince', 'minced turkey'],
            'turkey mince': ['ground turkey', 'minced turkey'],
            'chicken breast': ['chicken breasts', 'chicken breast meat'],
            'olive oil': ['extra virgin olive oil', 'evoo'],
            'coconut oil': ['virgin coconut oil', 'unrefined coconut oil'],
            'sea salt': ['salt', 'kosher salt'],
            'kosher salt': ['salt', 'sea salt'],
            'black pepper': ['pepper', 'ground black pepper'],
            'ground black pepper': ['black pepper', 'pepper']
        }
        
        # Words to remove from ingredient names for better matching
        self.stop_words = {
            'fresh', 'frozen', 'dried', 'organic', 'raw', 'cooked', 'chopped', 
            'diced', 'sliced', 'minced', 'grated', 'shredded', 'crushed',
            'whole', 'ground', 'powdered', 'extra', 'virgin', 'pure',
            'unsalted', 'salted', 'unsweetened', 'sweetened', 'low', 'fat',
            'reduced', 'sodium', 'free', 'range', 'grade', 'large', 'medium',
            'small', 'baby', 'young', 'mature', 'ripe', 'unripe', 'canned',
            'jarred', 'bottled', 'packaged', 'refrigerated'
        }
        
        # Unit patterns to remove (with quantities)
        self.unit_patterns = [
            r'\b\d+\.?\d*\s*(cup|cups|tablespoon|tablespoons|tbsp|teaspoon|teaspoons|tsp)\b',
            r'\b\d+\.?\d*\s*(pound|pounds|lb|lbs|ounce|ounces|oz)\b',
            r'\b\d+\.?\d*\s*(gram|grams|g|kilogram|kilograms|kg)\b',
            r'\b\d+\.?\d*\s*(liter|liters|l|milliliter|milliliters|ml)\b',
            r'\b\d+\.?\d*\s*(inch|inches|in)\b',
            r'\b\d+\.?\d*\s*(piece|pieces|pcs|slice|slices|clove|cloves)\b',
            r'\b\d+\.?\d*\s*(can|cans|jar|jars|bottle|bottles|package|packages|pkg)\b',
            r'\(\d+\.?\d*\s*[^)]*\)',  # Remove parenthetical quantities
            r'\b\d+\.?\d*\s*-\s*\d+\.?\d*\b',  # Remove ranges like "2-3"
            r'\b\d+/\d+\b',  # Remove fractions like "1/2"
            r'\b\d+\.?\d*\b',  # Remove standalone numbers
        ]
        
        logger.info(f"Ingredient matcher initialized with {self.fuzzy_threshold}% threshold")
    
    def normalize_ingredient_name(self, ingredient: str) -> str:
        """
        Normalize ingredient name by removing quantities, units, and descriptors
        """
        if not ingredient:
            return ""
        
        # Convert to lowercase and strip
        normalized = ingredient.lower().strip()
        
        # Remove unit patterns and quantities
        for pattern in self.unit_patterns:
            normalized = re.sub(pattern, '', normalized, flags=re.IGNORECASE)
        
        # Remove stop words
        words = normalized.split()
        filtered_words = [word for word in words if word not in self.stop_words]
        normalized = ' '.join(filtered_words)
        
        # Remove extra whitespace and punctuation
        normalized = re.sub(r'[,\(\)\[\]\.]+', '', normalized)
        normalized = re.sub(r'\s+', ' ', normalized).strip()
        
        # Handle common plural forms
        if normalized.endswith('ies'):
            normalized = normalized[:-3] + 'y'
        elif normalized.endswith('es') and not normalized.endswith('oes'):
            normalized = normalized[:-2]
        elif normalized.endswith('s') and len(normalized) > 3:
            normalized = normalized[:-1]
        
        return normalized
    
    def get_ingredient_variations(self, ingredient: str) -> List[str]:
        """
        Generate variations of an ingredient name including synonyms
        """
        normalized = self.normalize_ingredient_name(ingredient)
        variations = [normalized, ingredient.lower().strip()]
        
        # Add synonyms
        if normalized in self.synonyms:
            variations.extend(self.synonyms[normalized])
        
        # Add partial matches for compound ingredients
        words = normalized.split()
        if len(words) > 1:
            variations.extend(words)  # Add individual words
            
        # Remove duplicates while preserving order
        seen = set()
        unique_variations = []
        for var in variations:
            if var and var not in seen:
                seen.add(var)
                unique_variations.append(var)
        
        return unique_variations
    
    def find_best_match(self, recipe_ingredient: str, available_ingredients: List[Dict]) -> Optional[Dict]:
        """
        Find the best matching available ingredient for a recipe ingredient
        
        Args:
            recipe_ingredient: Ingredient name from recipe
            available_ingredients: List of available ingredients with 'Item' and 'source' fields
        
        Returns:
            Best matching ingredient dict with match score, or None if no good match
        """
        if not recipe_ingredient or not available_ingredients:
            return None
        
        # Get variations of the recipe ingredient
        recipe_variations = self.get_ingredient_variations(recipe_ingredient)
        
        best_match = None
        best_score = 0
        
        # Create a list of available ingredient names for batch processing
        available_names = []
        for item in available_ingredients:
            if not isinstance(item, dict):
                logger.warning(f"Skipping non-dict item: {item}")
                continue
                
            item_name = item.get('Item', '').strip()
            if item_name:
                normalized_name = self.normalize_ingredient_name(item_name)
                if normalized_name:  # Only add if normalization succeeded
                    available_names.append((normalized_name, item))
        
        # Try each recipe variation against all available ingredients
        for recipe_var in recipe_variations:
            if not recipe_var:
                continue
                
            # Use rapidfuzz for efficient batch matching
            matches = process.extract(
                recipe_var, 
                [name for name, _ in available_names],
                scorer=fuzz.ratio,
                limit=5
            )
            
            for match_result in matches:
                if len(match_result) != 2:
                    logger.warning(f"Unexpected match result format: {match_result}")
                    continue
                    
                match_name, score = match_result
                if score > best_score and score >= self.fuzzy_threshold:
                    # Find the original item for this match
                    for name_item_tuple in available_names:
                        if len(name_item_tuple) != 2:
                            logger.warning(f"Unexpected available_names format: {name_item_tuple}")
                            continue
                            
                        name, item = name_item_tuple
                        if name == match_name:
                            best_match = item.copy()
                            best_match['match_score'] = score
                            best_match['recipe_ingredient'] = recipe_ingredient
                            best_match['matched_name'] = match_name
                            best_score = score
                            break
        
        if best_match:
            logger.debug(f"Matched '{recipe_ingredient}' -> '{best_match['Item']}' (score: {best_score})")
        
        return best_match
    
    def match_recipe_ingredients(self, recipe: Dict, pantry_items: List[Dict], commissary_items: List[Dict]) -> Dict:
        """
        Match all ingredients in a recipe against available pantry and commissary items
        
        Args:
            recipe: Recipe dict with 'ingredients' list
            pantry_items: List of pantry ingredient dicts
            commissary_items: List of commissary ingredient dicts
        
        Returns:
            Updated recipe with ingredient analysis and priority scoring
        """
        if not recipe or 'ingredients' not in recipe:
            return recipe
        
        # Add source information to ingredients
        pantry_with_source = [dict(item, source='pantry') for item in pantry_items]
        commissary_with_source = [dict(item, source='commissary') for item in commissary_items]
        all_available = pantry_with_source + commissary_with_source
        
        # Match each recipe ingredient
        matched_ingredients = {
            'pantry': [],
            'commissary': [],
            'store': []
        }
        
        for recipe_ing in recipe.get('ingredients', []):
            ingredient_name = recipe_ing.get('name', '') or recipe_ing.get('original', '')
            
            if not ingredient_name:
                continue
            
            # Try to find a match
            match = self.find_best_match(ingredient_name, all_available)
            
            if match:
                source = match['source']
                match_info = {
                    'recipe_ingredient': ingredient_name,
                    'matched_item': match['Item'],
                    'match_score': match['match_score'],
                    'category': match.get('Category', ''),
                    'vendor': match.get('Vendor', ''),
                    'original_recipe_data': recipe_ing
                }
                matched_ingredients[source].append(match_info)
            else:
                # No match found - goes to store
                store_info = {
                    'recipe_ingredient': ingredient_name,
                    'matched_item': None,
                    'match_score': 0,
                    'category': 'Store Purchase',
                    'vendor': 'Supermarket',
                    'original_recipe_data': recipe_ing
                }
                matched_ingredients['store'].append(store_info)
        
        # Calculate scores and update recipe
        total_ingredients = len(recipe.get('ingredients', []))
        pantry_count = len(matched_ingredients['pantry'])
        commissary_count = len(matched_ingredients['commissary'])
        store_count = len(matched_ingredients['store'])
        
        # Priority scoring: Pantry (50%) + Commissary (30%) + availability (20%)
        pantry_percentage = (pantry_count / total_ingredients) if total_ingredients > 0 else 0
        commissary_percentage = (commissary_count / total_ingredients) if total_ingredients > 0 else 0
        available_percentage = ((pantry_count + commissary_count) / total_ingredients) if total_ingredients > 0 else 0
        
        # Weighted score prioritizing pantry items
        priority_score = (pantry_percentage * 0.5) + (commissary_percentage * 0.3) + (available_percentage * 0.2)
        
        # Cost score (lower is better) - pantry=0, commissary=1, store=2
        cost_score = (pantry_count * 0 + commissary_count * 1 + store_count * 2) / total_ingredients if total_ingredients > 0 else 2
        
        # Update recipe with analysis
        recipe['ingredient_analysis'] = {
            'pantry_ingredients': [item['recipe_ingredient'] for item in matched_ingredients['pantry']],
            'commissary_ingredients': [item['recipe_ingredient'] for item in matched_ingredients['commissary']],
            'store_ingredients': [item['recipe_ingredient'] for item in matched_ingredients['store']],
            'pantry_count': pantry_count,
            'commissary_count': commissary_count,
            'store_count': store_count,
            'total_ingredients': total_ingredients,
            'match_percentage': round(available_percentage * 100, 1),
            'pantry_percentage': round(pantry_percentage * 100, 1),
            'commissary_percentage': round(commissary_percentage * 100, 1),
            'priority_score': round(priority_score, 3),
            'cost_score': round(cost_score, 2),
            'detailed_matches': matched_ingredients
        }
        
        logger.info(f"Recipe '{recipe.get('title', 'Unknown')}': "
                   f"{pantry_count}P/{commissary_count}C/{store_count}S "
                   f"(score: {priority_score:.3f})")
        
        return recipe
    
    def sort_recipes_by_priority(self, recipes: List[Dict]) -> List[Dict]:
        """
        Sort recipes by priority score (higher is better)
        """
        def get_priority_score(recipe):
            analysis = recipe.get('ingredient_analysis', {})
            return analysis.get('priority_score', 0)
        
        return sorted(recipes, key=get_priority_score, reverse=True)


def create_ingredient_matcher() -> IngredientMatcher:
    """
    Factory function to create a configured ingredient matcher
    """
    threshold = int(os.getenv('FUZZY_MATCH_THRESHOLD', 80))
    return IngredientMatcher(fuzzy_threshold=threshold)