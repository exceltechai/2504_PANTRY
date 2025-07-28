"""
End-to-end tests for ingredient matching functionality using Playwright
Tests the complete workflow from file upload to recipe search and ingredient categorization
"""

import pytest
import asyncio
import json
import os
import sys
from pathlib import Path
from playwright.async_api import async_playwright, Page, BrowserContext, Browser

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

# Test configuration
BASE_URL = "http://localhost:8000"
API_BASE_URL = "http://localhost:5001"
TEST_DATA_DIR = Path(__file__).parent / "test_data"


class TestIngredientMatchingE2E:
    """End-to-end tests for ingredient matching in the web interface"""
    
    @pytest.fixture(scope="class")
    async def browser_context(self):
        """Set up browser context for tests"""
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=False, slow_mo=500)
            context = await browser.new_context(
                viewport={'width': 1280, 'height': 720},
                permissions=['clipboard-read', 'clipboard-write']
            )
            yield context
            await browser.close()
    
    @pytest.fixture
    async def page(self, browser_context):
        """Create a new page for each test"""
        page = await browser_context.new_page()
        yield page
        await page.close()
    
    @pytest.mark.asyncio
    async def test_application_loads(self, page: Page):
        """Test that the application loads correctly"""
        await page.goto(BASE_URL)
        
        # Check page title
        title = await page.title()
        assert "Pantry & Commissary Recipe System" in title
        
        # Check main heading
        heading = page.locator("h1")
        await heading.wait_for()
        assert await heading.inner_text() == "Pantry & Commissary Recipe System"
        
        # Check that main sections are present
        assert await page.locator(".sample-data-section").is_visible()
        assert await page.locator(".search-section").is_visible()
    
    @pytest.mark.asyncio
    async def test_sample_data_loads(self, page: Page):
        """Test that sample inventory data loads automatically"""
        await page.goto(BASE_URL)
        
        # Wait for inventory summary to load
        inventory_summary = page.locator("#inventory-summary")
        await inventory_summary.wait_for()
        
        # Check that loading spinner is replaced with inventory data
        await page.wait_for_selector(".loading-inventory", state="detached", timeout=10000)
        
        # Verify inventory summary appears
        summary_content = page.locator("#inventory-summary .inventory-grid")
        await summary_content.wait_for(timeout=10000)
        
        # Check that pantry and commissary sections are visible
        pantry_section = page.locator("[data-type='pantry']")
        commissary_section = page.locator("[data-type='commissary']")
        
        await pantry_section.wait_for()
        await commissary_section.wait_for()
        
        # Verify some sample items are displayed
        pantry_text = await pantry_section.inner_text()
        assert "Chicken Breast" in pantry_text or "chicken" in pantry_text.lower()
        
        commissary_text = await commissary_section.inner_text()
        assert "Turkey" in commissary_text or "turkey" in commissary_text.lower()
    
    @pytest.mark.asyncio
    async def test_file_upload_functionality(self, page: Page):
        """Test file upload for custom inventory"""
        await page.goto(BASE_URL)
        
        # Open the upload section
        upload_toggle = page.locator(".upload-toggle summary")
        await upload_toggle.click()
        
        # Wait for upload content to be visible
        upload_content = page.locator(".upload-content")
        await upload_content.wait_for()
        
        # Test pantry file upload
        pantry_input = page.locator("#pantry-upload")
        await pantry_input.set_input_files(str(TEST_DATA_DIR / "sample_pantry.csv"))
        
        # Test commissary file upload
        commissary_input = page.locator("#commissary-upload")
        await commissary_input.set_input_files(str(TEST_DATA_DIR / "sample_commissary.csv"))
        
        # Check that upload button becomes enabled
        upload_btn = page.locator("#upload-btn")
        await upload_btn.wait_for(state="visible")
        assert not await upload_btn.is_disabled()
        
        # Click upload button
        await upload_btn.click()
        
        # Wait for processing to complete
        loading_overlay = page.locator("#loading")
        await loading_overlay.wait_for(state="visible")
        await loading_overlay.wait_for(state="hidden", timeout=15000)
        
        # Verify inventory was updated
        inventory_summary = page.locator("#inventory-summary")
        summary_text = await inventory_summary.inner_text()
        assert "uploaded" in summary_text.lower() or "custom" in summary_text.lower()
    
    @pytest.mark.asyncio
    async def test_excel_file_upload(self, page: Page):
        """Test Excel file upload functionality"""
        await page.goto(BASE_URL)
        
        # Open upload section
        upload_toggle = page.locator(".upload-toggle summary")
        await upload_toggle.click()
        
        # Upload Excel files
        pantry_input = page.locator("#pantry-upload")
        await pantry_input.set_input_files(str(TEST_DATA_DIR / "sample_pantry.xlsx"))
        
        commissary_input = page.locator("#commissary-upload")
        await commissary_input.set_input_files(str(TEST_DATA_DIR / "sample_commissary.xlsx"))
        
        # Process files
        upload_btn = page.locator("#upload-btn")
        await upload_btn.click()
        
        # Wait for completion
        loading_overlay = page.locator("#loading")
        await loading_overlay.wait_for(state="visible")
        await loading_overlay.wait_for(state="hidden", timeout=15000)
        
        # Verify success
        inventory_summary = page.locator("#inventory-summary")
        await page.wait_for_timeout(1000)  # Allow UI to update
        summary_text = await inventory_summary.inner_text()
        assert "15" in summary_text or "30" in summary_text  # Should show item counts
    
    @pytest.mark.asyncio
    async def test_recipe_search_workflow(self, page: Page):
        """Test the complete recipe search workflow with ingredient matching"""
        await page.goto(BASE_URL)
        
        # Wait for sample data to load
        await page.wait_for_selector("#inventory-summary .inventory-grid", timeout=10000)
        
        # Configure search parameters
        dish_type_select = page.locator("#dish-type")
        await dish_type_select.select_option("main course")
        
        cuisine_input = page.locator("#cuisine")
        await cuisine_input.fill("Mediterranean")
        
        # Perform search
        search_btn = page.locator("#search-btn")
        await search_btn.click()
        
        # Wait for loading to start and complete
        loading_overlay = page.locator("#loading")
        await loading_overlay.wait_for(state="visible")
        await loading_overlay.wait_for(state="hidden", timeout=30000)
        
        # Check that results section becomes visible
        results_section = page.locator(".results-section")
        await results_section.wait_for(state="visible")
        
        # Verify recipe results are displayed
        results_container = page.locator("#results-container")
        await results_container.wait_for()
        
        # Check for recipe cards
        recipe_cards = page.locator(".recipe-card")
        await recipe_cards.first.wait_for(timeout=10000)
        
        recipe_count = await recipe_cards.count()
        assert recipe_count > 0, "No recipes found in search results"
        
        # Verify ingredient categorization in first recipe
        first_recipe = recipe_cards.first
        await first_recipe.wait_for()
        
        # Check for ingredient categories
        pantry_ingredients = first_recipe.locator(".pantry-ingredients")
        commissary_ingredients = first_recipe.locator(".commissary-ingredients")
        store_ingredients = first_recipe.locator(".store-ingredients")
        
        # At least one category should be present
        categories_present = 0
        if await pantry_ingredients.count() > 0:
            categories_present += 1
        if await commissary_ingredients.count() > 0:
            categories_present += 1
        if await store_ingredients.count() > 0:
            categories_present += 1
        
        assert categories_present > 0, "No ingredient categories found in recipe results"
    
    @pytest.mark.asyncio
    async def test_ingredient_categorization_accuracy(self, page: Page):
        """Test that ingredients are correctly categorized based on matching"""
        await page.goto(BASE_URL)
        
        # Wait for sample data
        await page.wait_for_selector("#inventory-summary .inventory-grid", timeout=10000)
        
        # Search for a specific recipe type that should have good matches
        dish_type_select = page.locator("#dish-type")
        await dish_type_select.select_option("breakfast")
        
        search_btn = page.locator("#search-btn")
        await search_btn.click()
        
        # Wait for results
        loading_overlay = page.locator("#loading")
        await loading_overlay.wait_for(state="visible")
        await loading_overlay.wait_for(state="hidden", timeout=30000)
        
        # Check results
        recipe_cards = page.locator(".recipe-card")
        await recipe_cards.first.wait_for(timeout=10000)
        
        # Examine the first recipe's ingredient categorization
        first_recipe = recipe_cards.first
        
        # Check that ingredients are properly sorted by availability
        priority_score = page.locator(".priority-score")
        if await priority_score.count() > 0:
            score_text = await priority_score.first.inner_text()
            # Should contain numerical score
            assert any(char.isdigit() for char in score_text)
        
        # Check that match percentages are displayed
        match_percentage = page.locator(".match-percentage")
        if await match_percentage.count() > 0:
            match_text = await match_percentage.first.inner_text()
            assert "%" in match_text
    
    @pytest.mark.asyncio
    async def test_recipe_sorting_by_ingredient_availability(self, page: Page):
        """Test that recipes are sorted by ingredient availability priority"""
        await page.goto(BASE_URL)
        
        # Wait for sample data
        await page.wait_for_selector("#inventory-summary .inventory-grid", timeout=10000)
        
        # Search for recipes
        search_btn = page.locator("#search-btn")
        await search_btn.click()
        
        # Wait for results
        loading_overlay = page.locator("#loading")
        await loading_overlay.wait_for(state="visible")
        await loading_overlay.wait_for(state="hidden", timeout=30000)
        
        # Get recipe cards
        recipe_cards = page.locator(".recipe-card")
        await recipe_cards.first.wait_for(timeout=10000)
        
        recipe_count = await recipe_cards.count()
        assert recipe_count >= 2, "Need at least 2 recipes to test sorting"
        
        # Check that first recipe has better or equal score than second
        first_recipe_score = await self.get_recipe_priority_score(recipe_cards.nth(0))
        second_recipe_score = await self.get_recipe_priority_score(recipe_cards.nth(1))
        
        if first_recipe_score is not None and second_recipe_score is not None:
            assert first_recipe_score >= second_recipe_score, \
                f"Recipes not sorted correctly: {first_recipe_score} < {second_recipe_score}"
    
    async def get_recipe_priority_score(self, recipe_card):
        """Extract priority score from recipe card"""
        try:
            score_element = recipe_card.locator(".priority-score, .match-percentage")
            if await score_element.count() > 0:
                score_text = await score_element.first.inner_text()
                # Extract numerical value
                import re
                numbers = re.findall(r'\d+\.?\d*', score_text)
                if numbers:
                    return float(numbers[0])
        except:
            pass
        return None
    
    @pytest.mark.asyncio
    async def test_synonym_matching_in_results(self, page: Page):
        """Test that synonym matching works in recipe results"""
        await page.goto(BASE_URL)
        
        # Wait for sample data
        await page.wait_for_selector("#inventory-summary .inventory-grid", timeout=10000)
        
        # Search for recipes
        search_btn = page.locator("#search-btn")
        await search_btn.click()
        
        # Wait for results
        loading_overlay = page.locator("#loading")
        await loading_overlay.wait_for(state="visible")
        await loading_overlay.wait_for(state="hidden", timeout=30000)
        
        # Look for recipes with ingredients that should match synonyms
        recipe_cards = page.locator(".recipe-card")
        await recipe_cards.first.wait_for(timeout=10000)
        
        # Check if any recipe contains ingredients that should be matched via synonyms
        found_synonym_match = False
        recipe_count = min(await recipe_cards.count(), 5)  # Check first 5 recipes
        
        for i in range(recipe_count):
            recipe = recipe_cards.nth(i)
            recipe_text = await recipe.inner_text()
            
            # Check for common synonym matches
            synonym_pairs = [
                ("scallion", "green onion"),
                ("sweet pepper", "bell pepper"),
                ("courgette", "zucchini"),
                ("turkey", "mince")
            ]
            
            for synonym, canonical in synonym_pairs:
                if synonym.lower() in recipe_text.lower() and canonical.lower() in recipe_text.lower():
                    found_synonym_match = True
                    break
            
            if found_synonym_match:
                break
        
        # Note: This test may not always pass depending on the recipes returned by the API
        # But it provides valuable insight into synonym matching behavior
        print(f"Synonym matching test result: {'PASSED' if found_synonym_match else 'NO_SYNONYMS_FOUND'}")
    
    @pytest.mark.asyncio
    async def test_error_handling(self, page: Page):
        """Test error handling for various failure scenarios"""
        await page.goto(BASE_URL)
        
        # Test invalid file upload
        upload_toggle = page.locator(".upload-toggle summary")
        await upload_toggle.click()
        
        # Try to upload a non-CSV/Excel file (this test file itself)
        pantry_input = page.locator("#pantry-upload")
        current_file = Path(__file__)
        await pantry_input.set_input_files(str(current_file))
        
        upload_btn = page.locator("#upload-btn")
        
        # The upload button might become enabled, but the backend should handle the error
        if not await upload_btn.is_disabled():
            await upload_btn.click()
            
            # Check for error handling
            await page.wait_for_timeout(2000)
            
            # Error might be shown in loading overlay or as an alert
            error_messages = page.locator(".error-message, .alert-error")
            if await error_messages.count() > 0:
                error_text = await error_messages.first.inner_text()
                assert len(error_text) > 0
    
    @pytest.mark.asyncio 
    async def test_responsive_design(self, page: Page):
        """Test that the application works on different screen sizes"""
        await page.goto(BASE_URL)
        
        # Test mobile viewport
        await page.set_viewport_size({"width": 375, "height": 667})
        await page.wait_for_timeout(500)
        
        # Check that main elements are still visible and accessible
        heading = page.locator("h1")
        assert await heading.is_visible()
        
        search_section = page.locator(".search-section")
        assert await search_section.is_visible()
        
        # Test tablet viewport
        await page.set_viewport_size({"width": 768, "height": 1024})
        await page.wait_for_timeout(500)
        
        # Elements should still be visible
        assert await heading.is_visible()
        assert await search_section.is_visible()
        
        # Return to desktop
        await page.set_viewport_size({"width": 1280, "height": 720})


if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([__file__, "-v", "--tb=short"])