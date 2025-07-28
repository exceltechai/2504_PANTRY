"""
Quick test to verify recipe search is working in browser
"""

import pytest
from playwright.sync_api import Page, expect

def test_quick_recipe_search_debug(page: Page):
    """Quick test to debug recipe search issue"""
    
    # Monitor console messages and network requests
    console_messages = []
    network_requests = []
    
    def log_console(msg):
        console_messages.append(f"{msg.type}: {msg.text}")
    
    def log_request(request):
        if "localhost:5001" in request.url:
            network_requests.append(request.url)
    
    page.on("console", log_console)
    page.on("request", log_request)
    
    # Go to the site
    page.goto("http://localhost:8000")
    
    # Wait for sample data to load
    expect(page.locator("#inventory-summary .inventory-cards")).to_be_visible(timeout=10000)
    print("✓ Sample data loaded")
    
    # Perform a simple search
    search_btn = page.locator("#search-btn")
    search_btn.click()
    print("✓ Search button clicked")
    
    # Wait a bit to see what happens
    page.wait_for_timeout(8000)
    
    # Check for error messages
    error_notifications = page.locator(".notification.error, .alert-danger, .error-message")
    if error_notifications.count() > 0:
        error_text = error_notifications.first.inner_text()
        print(f"❌ Error found: {error_text}")
    else:
        print("✓ No error messages found")
    
    # Check if results section is visible
    results_section = page.locator(".results-section")
    if results_section.is_visible():
        print("✓ Results section is visible")
        
        # Check for recipe cards
        recipe_cards = page.locator(".recipe-card")
        recipe_count = recipe_cards.count()
        print(f"✓ Found {recipe_count} recipe cards")
        
        if recipe_count > 0:
            first_recipe_text = recipe_cards.first.inner_text()
            print(f"✓ First recipe preview: {first_recipe_text[:100]}...")
    else:
        print("❌ Results section is not visible")
    
    # Print console messages for debugging
    print("\n=== Console Messages ===")
    for msg in console_messages[-10:]:  # Last 10 messages
        print(msg)
    
    # Print network requests
    print("\n=== API Requests ===")
    for req in network_requests:
        print(req)
    
    # Take a screenshot
    page.screenshot(path="quick_test_debug.png")
    print("\n✓ Screenshot saved as quick_test_debug.png")