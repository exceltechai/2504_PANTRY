"""
Debug test for recipe search functionality
"""

import pytest
from playwright.sync_api import Page, expect

def test_debug_recipe_search(page: Page):
    """Debug recipe search to see what's happening"""
    
    # Monitor console messages
    console_messages = []
    
    def log_console(msg):
        console_messages.append(f"{msg.type}: {msg.text}")
    
    page.on("console", log_console)
    
    # Monitor network responses
    api_responses = []
    
    def log_response(response):
        if "localhost:5001" in response.url:
            api_responses.append({
                'url': response.url,
                'status': response.status,
                'headers': dict(response.headers)
            })
    
    page.on("response", log_response)
    
    page.goto("http://localhost:8000")
    
    # Wait for sample data to load
    page.wait_for_selector("#inventory-summary .inventory-cards", timeout=10000)
    print("Sample data loaded successfully")
    
    # Configure search parameters
    dish_type_select = page.locator("#dish-type")
    dish_type_select.select_option("main course")
    
    cuisine_input = page.locator("#cuisine")
    cuisine_input.fill("Mediterranean")
    
    print("Search parameters set")
    
    # Perform search
    search_btn = page.locator("#search-btn")
    search_btn.click()
    
    print("Search button clicked")
    
    # Wait a bit to see what happens
    page.wait_for_timeout(5000)
    
    # Check for loading overlay
    loading_overlay = page.locator("#loading")
    print(f"Loading overlay visible: {loading_overlay.is_visible()}")
    
    # Wait longer for results
    page.wait_for_timeout(10000)
    
    # Check results section
    results_section = page.locator(".results-section")
    print(f"Results section visible: {results_section.is_visible()}")
    print(f"Results section style: {results_section.get_attribute('style')}")
    
    # Check results container
    results_container = page.locator("#results-container")
    print(f"Results container visible: {results_container.is_visible()}")
    print(f"Results container HTML: {results_container.inner_html()}")
    
    print("\n=== Console Messages ===")
    for msg in console_messages:
        print(msg)
    
    print("\n=== API Responses ===")
    for response in api_responses:
        print(f"{response['status']} {response['url']}")
    
    # Take a screenshot for debugging
    page.screenshot(path="debug_recipe_search.png")
    print("Screenshot saved as debug_recipe_search.png")