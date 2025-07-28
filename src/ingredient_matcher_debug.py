"""
Debugging and tuning tool for ingredient matching accuracy
Provides detailed analysis, accuracy metrics, and threshold optimization
"""

import os
import json
import pandas as pd
from typing import Dict, List, Tuple, Optional
from rapidfuzz import fuzz
import logging
from collections import defaultdict
import statistics

from ingredient_matcher import IngredientMatcher

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class IngredientMatcherDebugger:
    """
    Debugging and optimization tool for ingredient matching
    """
    
    def __init__(self, matcher: IngredientMatcher = None):
        self.matcher = matcher or IngredientMatcher()
        self.test_cases = []
        self.results = []
        
    def add_test_case(self, recipe_ingredient: str, expected_match: str, 
                     available_ingredients: List[Dict], should_match: bool = True):
        """Add a test case for validation"""
        self.test_cases.append({
            'recipe_ingredient': recipe_ingredient,
            'expected_match': expected_match,
            'available_ingredients': available_ingredients,
            'should_match': should_match
        })
    
    def load_sample_data(self) -> Tuple[List[Dict], List[Dict]]:
        """Load sample pantry and commissary data for testing"""
        pantry_sample = [
            {'Item': 'Chicken Breast', 'Category': 'Protein', 'Vendor': 'Pantry'},
            {'Item': 'Green Onions', 'Category': 'Vegetables', 'Vendor': 'Pantry'},
            {'Item': 'Bell Peppers', 'Category': 'Vegetables', 'Vendor': 'Pantry'},
            {'Item': 'Olive Oil', 'Category': 'Oils', 'Vendor': 'Pantry'},
            {'Item': 'Sea Salt', 'Category': 'Seasonings', 'Vendor': 'Pantry'},
            {'Item': 'Black Pepper', 'Category': 'Seasonings', 'Vendor': 'Pantry'},
            {'Item': 'Ground Beef', 'Category': 'Protein', 'Vendor': 'Pantry'},
            {'Item': 'Sweet Potatoes', 'Category': 'Vegetables', 'Vendor': 'Pantry'},
            {'Item': 'Avocados', 'Category': 'Vegetables', 'Vendor': 'Pantry'},
            {'Item': 'Coconut Oil', 'Category': 'Oils', 'Vendor': 'Pantry'}
        ]
        
        commissary_sample = [
            {'Item': 'Turkey Mince', 'Category': 'Protein', 'Vendor': 'Commissary'},
            {'Item': 'Zucchini', 'Category': 'Vegetables', 'Vendor': 'Commissary'},
            {'Item': 'Carrots', 'Category': 'Vegetables', 'Vendor': 'Commissary'},
            {'Item': 'Broccoli', 'Category': 'Vegetables', 'Vendor': 'Commissary'},
            {'Item': 'Spinach', 'Category': 'Vegetables', 'Vendor': 'Commissary'},
            {'Item': 'Cauliflower', 'Category': 'Vegetables', 'Vendor': 'Commissary'},
            {'Item': 'Garlic', 'Category': 'Seasonings', 'Vendor': 'Commissary'},
            {'Item': 'Onions', 'Category': 'Vegetables', 'Vendor': 'Commissary'},
            {'Item': 'Tomatoes', 'Category': 'Vegetables', 'Vendor': 'Commissary'},
            {'Item': 'Cucumbers', 'Category': 'Vegetables', 'Vendor': 'Commissary'}
        ]
        
        return pantry_sample, commissary_sample
    
    def create_test_cases(self):
        """Create comprehensive test cases for various matching scenarios"""
        pantry, commissary = self.load_sample_data()
        all_ingredients = pantry + commissary
        
        # Test cases for exact matches
        self.add_test_case('chicken breast', 'Chicken Breast', all_ingredients, True)
        self.add_test_case('olive oil', 'Olive Oil', all_ingredients, True)
        
        # Test cases for synonym matching
        self.add_test_case('scallions', 'Green Onions', all_ingredients, True)
        self.add_test_case('spring onions', 'Green Onions', all_ingredients, True)
        self.add_test_case('sweet pepper', 'Bell Peppers', all_ingredients, True)
        self.add_test_case('courgette', 'Zucchini', all_ingredients, True)
        
        # Test cases for plural/singular variations
        self.add_test_case('bell pepper', 'Bell Peppers', all_ingredients, True)
        self.add_test_case('sweet potato', 'Sweet Potatoes', all_ingredients, True)
        self.add_test_case('avocado', 'Avocados', all_ingredients, True)
        self.add_test_case('carrot', 'Carrots', all_ingredients, True)
        
        # Test cases with quantities and descriptors
        self.add_test_case('2 lbs ground beef', 'Ground Beef', all_ingredients, True)
        self.add_test_case('1 cup diced tomatoes', 'Tomatoes', all_ingredients, True)
        self.add_test_case('3 cloves fresh garlic', 'Garlic', all_ingredients, True)
        self.add_test_case('2 tbsp extra virgin olive oil', 'Olive Oil', all_ingredients, True)
        self.add_test_case('1 tsp kosher salt', 'Sea Salt', all_ingredients, True)
        self.add_test_case('1/2 tsp ground black pepper', 'Black Pepper', all_ingredients, True)
        
        # Test cases for partial matches
        self.add_test_case('chicken thighs', 'Chicken Breast', all_ingredients, False)  # Should not match
        self.add_test_case('ground turkey', 'Turkey Mince', all_ingredients, True)
        
        # Test cases for no matches (should go to store)
        self.add_test_case('quinoa', '', all_ingredients, False)
        self.add_test_case('almond flour', '', all_ingredients, False)
        self.add_test_case('coconut milk', '', all_ingredients, False)
        
    def test_normalization_accuracy(self):
        """Test the accuracy of ingredient name normalization"""
        test_normalizations = [
            ('2 lbs fresh chicken breast', 'chicken breast'),
            ('1 cup diced yellow onions', 'yellow onion'),
            ('3 tbsp extra virgin olive oil', 'olive oil'),
            ('1/2 tsp ground black pepper', 'black pepper'),
            ('2 medium bell peppers, chopped', 'bell pepper'),
            ('1 bunch green onions (scallions)', 'green onion'),
            ('4 oz baby spinach leaves', 'spinach leave')
        ]
        
        print("\n=== NORMALIZATION ACCURACY TEST ===")
        correct = 0
        total = len(test_normalizations)
        
        for original, expected in test_normalizations:
            actual = self.matcher.normalize_ingredient_name(original)
            is_correct = actual == expected
            if is_correct:
                correct += 1
            
            print(f"Original: '{original}'")
            print(f"Expected: '{expected}'")
            print(f"Actual:   '{actual}'")
            print(f"Correct:  {'✓' if is_correct else '✗'}")
            print("-" * 50)
        
        accuracy = (correct / total) * 100
        print(f"Normalization Accuracy: {accuracy:.1f}% ({correct}/{total})")
        return accuracy
    
    def run_accuracy_test(self, threshold: int = None) -> Dict:
        """Run accuracy test with current or specified threshold"""
        if threshold:
            original_threshold = self.matcher.fuzzy_threshold
            self.matcher.fuzzy_threshold = threshold
        
        if not self.test_cases:
            self.create_test_cases()
        
        results = {
            'threshold': self.matcher.fuzzy_threshold,
            'total_tests': len(self.test_cases),
            'correct_matches': 0,
            'false_positives': 0,
            'false_negatives': 0,
            'details': []
        }
        
        for test_case in self.test_cases:
            recipe_ingredient = test_case['recipe_ingredient']
            expected_match = test_case['expected_match']
            available_ingredients = test_case['available_ingredients']
            should_match = test_case['should_match']
            
            match = self.matcher.find_best_match(recipe_ingredient, available_ingredients)
            
            if should_match:
                if match and match['Item'] == expected_match:
                    results['correct_matches'] += 1
                    status = 'CORRECT'
                elif match:
                    results['false_positives'] += 1
                    status = 'FALSE_POSITIVE'
                else:
                    results['false_negatives'] += 1
                    status = 'FALSE_NEGATIVE'
            else:
                if not match:
                    results['correct_matches'] += 1
                    status = 'CORRECT_NO_MATCH'
                else:
                    results['false_positives'] += 1
                    status = 'FALSE_POSITIVE'
            
            details = {
                'recipe_ingredient': recipe_ingredient,
                'expected_match': expected_match if should_match else 'NO_MATCH',
                'actual_match': match['Item'] if match else 'NO_MATCH',
                'match_score': match['match_score'] if match else 0,
                'status': status,
                'should_match': should_match
            }
            results['details'].append(details)
        
        # Calculate metrics
        accuracy = (results['correct_matches'] / results['total_tests']) * 100
        precision = results['correct_matches'] / (results['correct_matches'] + results['false_positives']) if (results['correct_matches'] + results['false_positives']) > 0 else 0
        recall = results['correct_matches'] / (results['correct_matches'] + results['false_negatives']) if (results['correct_matches'] + results['false_negatives']) > 0 else 0
        f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
        
        results['accuracy'] = accuracy
        results['precision'] = precision
        results['recall'] = recall
        results['f1_score'] = f1_score
        
        # Restore original threshold
        if threshold:
            self.matcher.fuzzy_threshold = original_threshold
        
        return results
    
    def optimize_threshold(self, min_threshold: int = 60, max_threshold: int = 95, step: int = 5) -> Dict:
        """Find optimal threshold by testing different values"""
        print("\n=== THRESHOLD OPTIMIZATION ===")
        
        if not self.test_cases:
            self.create_test_cases()
        
        optimization_results = []
        
        for threshold in range(min_threshold, max_threshold + 1, step):
            results = self.run_accuracy_test(threshold)
            optimization_results.append(results)
            
            print(f"Threshold {threshold}%: Accuracy={results['accuracy']:.1f}%, "
                  f"F1={results['f1_score']:.3f}, "
                  f"Precision={results['precision']:.3f}, "
                  f"Recall={results['recall']:.3f}")
        
        # Find best threshold based on F1 score
        best_result = max(optimization_results, key=lambda x: x['f1_score'])
        
        print(f"\nOptimal threshold: {best_result['threshold']}%")
        print(f"Best F1 score: {best_result['f1_score']:.3f}")
        print(f"Accuracy: {best_result['accuracy']:.1f}%")
        
        return {
            'optimal_threshold': best_result['threshold'],
            'best_f1_score': best_result['f1_score'],
            'all_results': optimization_results
        }
    
    def analyze_match_scores(self) -> Dict:
        """Analyze distribution of match scores to understand threshold effectiveness"""
        if not self.test_cases:
            self.create_test_cases()
        
        correct_scores = []
        incorrect_scores = []
        
        for test_case in self.test_cases:
            recipe_ingredient = test_case['recipe_ingredient']
            expected_match = test_case['expected_match']
            available_ingredients = test_case['available_ingredients']
            should_match = test_case['should_match']
            
            match = self.matcher.find_best_match(recipe_ingredient, available_ingredients)
            
            if match:
                score = match['match_score']
                if should_match and match['Item'] == expected_match:
                    correct_scores.append(score)
                elif not should_match or match['Item'] != expected_match:
                    incorrect_scores.append(score)
        
        analysis = {
            'correct_match_scores': {
                'min': min(correct_scores) if correct_scores else 0,
                'max': max(correct_scores) if correct_scores else 0,
                'mean': statistics.mean(correct_scores) if correct_scores else 0,
                'median': statistics.median(correct_scores) if correct_scores else 0,
                'count': len(correct_scores)
            },
            'incorrect_match_scores': {
                'min': min(incorrect_scores) if incorrect_scores else 0,
                'max': max(incorrect_scores) if incorrect_scores else 0,
                'mean': statistics.mean(incorrect_scores) if incorrect_scores else 0,
                'median': statistics.median(incorrect_scores) if incorrect_scores else 0,
                'count': len(incorrect_scores)
            }
        }
        
        print("\n=== MATCH SCORE ANALYSIS ===")
        print(f"Correct matches: {analysis['correct_match_scores']['count']} samples")
        print(f"  Score range: {analysis['correct_match_scores']['min']:.1f} - {analysis['correct_match_scores']['max']:.1f}")
        print(f"  Mean: {analysis['correct_match_scores']['mean']:.1f}")
        print(f"  Median: {analysis['correct_match_scores']['median']:.1f}")
        
        print(f"\nIncorrect matches: {analysis['incorrect_match_scores']['count']} samples")
        print(f"  Score range: {analysis['incorrect_match_scores']['min']:.1f} - {analysis['incorrect_match_scores']['max']:.1f}")
        print(f"  Mean: {analysis['incorrect_match_scores']['mean']:.1f}")
        print(f"  Median: {analysis['incorrect_match_scores']['median']:.1f}")
        
        return analysis
    
    def test_different_algorithms(self) -> Dict:
        """Test different fuzzy matching algorithms"""
        if not self.test_cases:
            self.create_test_cases()
        
        algorithms = {
            'ratio': fuzz.ratio,
            'partial_ratio': fuzz.partial_ratio,
            'token_sort_ratio': fuzz.token_sort_ratio,
            'token_set_ratio': fuzz.token_set_ratio,
            'WRatio': fuzz.WRatio
        }
        
        results = {}
        
        print("\n=== ALGORITHM COMPARISON ===")
        
        for algo_name, algo_func in algorithms.items():
            # Temporarily modify the matcher's scorer
            original_find_best_match = self.matcher.find_best_match
            
            def modified_find_best_match(recipe_ingredient, available_ingredients):
                # Custom implementation using different algorithm
                if not recipe_ingredient or not available_ingredients:
                    return None
                
                recipe_variations = self.matcher.get_ingredient_variations(recipe_ingredient)
                best_match = None
                best_score = 0
                
                available_names = []
                for item in available_ingredients:
                    if isinstance(item, dict):
                        item_name = item.get('Item', '').strip()
                        if item_name:
                            normalized_name = self.matcher.normalize_ingredient_name(item_name)
                            if normalized_name:
                                available_names.append((normalized_name, item))
                
                for recipe_var in recipe_variations:
                    if not recipe_var:
                        continue
                    
                    for name, item in available_names:
                        score = algo_func(recipe_var, name)
                        if score > best_score and score >= self.matcher.fuzzy_threshold:
                            best_match = item.copy()
                            best_match['match_score'] = score
                            best_match['recipe_ingredient'] = recipe_ingredient
                            best_match['matched_name'] = name
                            best_score = score
                
                return best_match
            
            self.matcher.find_best_match = modified_find_best_match
            
            # Run test with this algorithm
            test_results = self.run_accuracy_test()
            results[algo_name] = test_results
            
            print(f"{algo_name:15} Accuracy: {test_results['accuracy']:.1f}% "
                  f"F1: {test_results['f1_score']:.3f}")
            
            # Restore original method
            self.matcher.find_best_match = original_find_best_match
        
        # Find best algorithm
        best_algo = max(results.keys(), key=lambda x: results[x]['f1_score'])
        print(f"\nBest algorithm: {best_algo} (F1: {results[best_algo]['f1_score']:.3f})")
        
        return results
    
    def generate_report(self, output_file: str = None) -> str:
        """Generate comprehensive accuracy and tuning report"""
        report = []
        report.append("INGREDIENT MATCHER ACCURACY REPORT")
        report.append("=" * 50)
        report.append(f"Current threshold: {self.matcher.fuzzy_threshold}%")
        report.append("")
        
        # Run normalization test
        norm_accuracy = self.test_normalization_accuracy()
        
        # Run accuracy test
        accuracy_results = self.run_accuracy_test()
        report.append(f"\nACCURACY METRICS (Threshold: {accuracy_results['threshold']}%)")
        report.append("-" * 30)
        report.append(f"Total test cases: {accuracy_results['total_tests']}")
        report.append(f"Accuracy: {accuracy_results['accuracy']:.1f}%")
        report.append(f"Precision: {accuracy_results['precision']:.3f}")
        report.append(f"Recall: {accuracy_results['recall']:.3f}")
        report.append(f"F1 Score: {accuracy_results['f1_score']:.3f}")
        report.append(f"Correct matches: {accuracy_results['correct_matches']}")
        report.append(f"False positives: {accuracy_results['false_positives']}")
        report.append(f"False negatives: {accuracy_results['false_negatives']}")
        
        # Detailed results
        report.append("\nDETAILED RESULTS")
        report.append("-" * 30)
        for detail in accuracy_results['details']:
            status_symbol = "✓" if detail['status'] in ['CORRECT', 'CORRECT_NO_MATCH'] else "✗"
            report.append(f"{status_symbol} {detail['recipe_ingredient']} -> {detail['actual_match']} "
                         f"(score: {detail['match_score']:.1f}, expected: {detail['expected_match']})")
        
        # Threshold optimization
        optimization = self.optimize_threshold()
        report.append(f"\nOPTIMAL THRESHOLD RECOMMENDATION")
        report.append("-" * 30)
        report.append(f"Recommended threshold: {optimization['optimal_threshold']}%")
        report.append(f"Expected F1 score: {optimization['best_f1_score']:.3f}")
        
        # Algorithm comparison
        algo_results = self.test_different_algorithms()
        report.append(f"\nALGORITHM COMPARISON")
        report.append("-" * 30)
        for algo, results in algo_results.items():
            report.append(f"{algo:15} F1: {results['f1_score']:.3f} "
                         f"Accuracy: {results['accuracy']:.1f}%")
        
        # Match score analysis
        score_analysis = self.analyze_match_scores()
        
        report_text = "\n".join(report)
        
        if output_file:
            with open(output_file, 'w') as f:
                f.write(report_text)
            print(f"\nReport saved to: {output_file}")
        
        return report_text


def main():
    """Main function to run ingredient matching debugging and tuning"""
    debugger = IngredientMatcherDebugger()
    
    print("INGREDIENT MATCHER DEBUGGING & TUNING TOOL")
    print("=" * 50)
    
    # Generate comprehensive report
    report = debugger.generate_report('ingredient_matcher_report.txt')
    print(report)


if __name__ == "__main__":
    main()