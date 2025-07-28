"""
Test suite for ingredient matching accuracy and functionality
"""

import pytest
import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from ingredient_matcher import IngredientMatcher


class TestIngredientMatcher:
    """Test cases for the IngredientMatcher class"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.matcher = IngredientMatcher(fuzzy_threshold=90)
        
        # Sample pantry and commissary data
        self.pantry_items = [
            {'Item': 'Chicken Breast', 'Category': 'Protein', 'Vendor': 'Pantry'},
            {'Item': 'Green Onions', 'Category': 'Vegetables', 'Vendor': 'Pantry'},
            {'Item': 'Bell Peppers', 'Category': 'Vegetables', 'Vendor': 'Pantry'},
            {'Item': 'Olive Oil', 'Category': 'Oils', 'Vendor': 'Pantry'},
            {'Item': 'Sea Salt', 'Category': 'Seasonings', 'Vendor': 'Pantry'},
            {'Item': 'Black Pepper', 'Category': 'Seasonings', 'Vendor': 'Pantry'},
        ]
        
        self.commissary_items = [
            {'Item': 'Turkey Mince', 'Category': 'Protein', 'Vendor': 'Commissary'},
            {'Item': 'Zucchini', 'Category': 'Vegetables', 'Vendor': 'Commissary'},
            {'Item': 'Carrots', 'Category': 'Vegetables', 'Vendor': 'Commissary'},
            {'Item': 'Garlic', 'Category': 'Seasonings', 'Vendor': 'Commissary'},
        ]
        
        self.all_items = self.pantry_items + self.commissary_items
    
    def test_exact_matches(self):
        """Test exact ingredient name matches"""
        test_cases = [
            ('chicken breast', 'Chicken Breast'),
            ('olive oil', 'Olive Oil'),
            ('bell peppers', 'Bell Peppers'),
            ('garlic', 'Garlic')
        ]
        
        for recipe_ingredient, expected_match in test_cases:
            match = self.matcher.find_best_match(recipe_ingredient, self.all_items)
            assert match is not None, f"No match found for '{recipe_ingredient}'"
            assert match['Item'] == expected_match, f"Expected '{expected_match}', got '{match['Item']}'"
            assert match['match_score'] >= 95, f"Score too low: {match['match_score']}"
    
    def test_synonym_matches(self):
        """Test ingredient synonym matching"""
        test_cases = [
            ('scallions', 'Green Onions'),
            ('spring onions', 'Green Onions'),
            ('sweet pepper', 'Bell Peppers'),
            ('courgette', 'Zucchini'),
            ('ground turkey', 'Turkey Mince'),
            ('kosher salt', 'Sea Salt')
        ]
        
        for recipe_ingredient, expected_match in test_cases:
            match = self.matcher.find_best_match(recipe_ingredient, self.all_items)
            assert match is not None, f"No match found for '{recipe_ingredient}'"
            assert match['Item'] == expected_match, f"Expected '{expected_match}', got '{match['Item']}'"
    
    def test_quantity_removal(self):
        """Test matching with quantities and descriptors"""
        test_cases = [
            ('2 lbs chicken breast', 'Chicken Breast'),
            ('1 cup diced carrots', 'Carrots'),
            ('3 cloves fresh garlic', 'Garlic'),
            ('2 tbsp extra virgin olive oil', 'Olive Oil'),
            ('1/2 tsp ground black pepper', 'Black Pepper')
        ]
        
        for recipe_ingredient, expected_match in test_cases:
            match = self.matcher.find_best_match(recipe_ingredient, self.all_items)
            assert match is not None, f"No match found for '{recipe_ingredient}'"
            assert match['Item'] == expected_match, f"Expected '{expected_match}', got '{match['Item']}'"
    
    def test_no_matches(self):
        """Test ingredients that should not match anything"""
        test_cases = [
            'quinoa',
            'almond flour', 
            'coconut milk',
            'avocado oil'
        ]
        
        for recipe_ingredient in test_cases:
            match = self.matcher.find_best_match(recipe_ingredient, self.all_items)
            assert match is None, f"Unexpected match found for '{recipe_ingredient}': {match['Item'] if match else None}"
    
    def test_normalization(self):
        """Test ingredient name normalization"""
        test_cases = [
            ('2 lbs fresh chicken breast', 'chicken breast'),
            ('1 cup diced yellow onions', 'yellow onion'),
            ('3 tbsp extra virgin olive oil', 'olive oil'),
            ('2 medium bell peppers, chopped', 'bell pepper')
        ]
        
        for original, expected in test_cases:
            normalized = self.matcher.normalize_ingredient_name(original)
            assert expected in normalized or normalized in expected, f"Expected '{expected}' in '{normalized}'"
    
    def test_recipe_matching(self):
        """Test full recipe ingredient analysis"""
        sample_recipe = {
            'title': 'Test Recipe',
            'ingredients': [
                {'name': 'chicken breast'},
                {'name': '2 cups bell peppers'},
                {'name': 'quinoa'},
                {'name': 'garlic'}
            ]
        }
        
        analyzed_recipe = self.matcher.match_recipe_ingredients(
            sample_recipe, self.pantry_items, self.commissary_items
        )
        
        analysis = analyzed_recipe['ingredient_analysis']
        
        # Check that we have the expected categorization
        assert 'chicken breast' in analysis['pantry_ingredients']
        assert '2 cups bell peppers' in analysis['pantry_ingredients']
        assert 'garlic' in analysis['commissary_ingredients']
        assert 'quinoa' in analysis['store_ingredients']
        
        # Check counts
        assert analysis['pantry_count'] == 2
        assert analysis['commissary_count'] == 1
        assert analysis['store_count'] == 1
        assert analysis['total_ingredients'] == 4
        
        # Check percentages
        assert analysis['pantry_percentage'] == 50.0
        assert analysis['commissary_percentage'] == 25.0
        assert analysis['match_percentage'] == 75.0
    
    def test_threshold_enforcement(self):
        """Test that threshold is properly enforced"""
        low_threshold_matcher = IngredientMatcher(fuzzy_threshold=50)
        high_threshold_matcher = IngredientMatcher(fuzzy_threshold=99)
        
        # This should match with low threshold but not with high threshold
        test_ingredient = 'chicken thighs'  # Similar to 'Chicken Breast'
        
        low_match = low_threshold_matcher.find_best_match(test_ingredient, self.all_items)
        high_match = high_threshold_matcher.find_best_match(test_ingredient, self.all_items)
        
        # Low threshold should find a match, high threshold should not
        assert low_match is not None, "Low threshold should find a match"
        assert high_match is None, "High threshold should not find a match"
    
    def test_priority_scoring(self):
        """Test that priority scoring works correctly"""
        recipes = [
            {
                'title': 'Pantry Heavy Recipe',
                'ingredients': [
                    {'name': 'chicken breast'},
                    {'name': 'bell peppers'},
                    {'name': 'olive oil'}
                ]
            },
            {
                'title': 'Store Heavy Recipe', 
                'ingredients': [
                    {'name': 'quinoa'},
                    {'name': 'almond flour'},
                    {'name': 'coconut milk'}
                ]
            }
        ]
        
        # Analyze both recipes
        analyzed_recipes = []
        for recipe in recipes:
            analyzed = self.matcher.match_recipe_ingredients(
                recipe, self.pantry_items, self.commissary_items
            )
            analyzed_recipes.append(analyzed)
        
        # Sort by priority
        sorted_recipes = self.matcher.sort_recipes_by_priority(analyzed_recipes)
        
        # Pantry heavy recipe should be first
        assert sorted_recipes[0]['title'] == 'Pantry Heavy Recipe'
        assert sorted_recipes[1]['title'] == 'Store Heavy Recipe'
        
        # Check priority scores
        pantry_score = sorted_recipes[0]['ingredient_analysis']['priority_score']
        store_score = sorted_recipes[1]['ingredient_analysis']['priority_score']
        assert pantry_score > store_score, f"Pantry score {pantry_score} should be > store score {store_score}"


if __name__ == '__main__':
    pytest.main([__file__, '-v'])