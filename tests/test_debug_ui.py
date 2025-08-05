"""
Debug test to understand the UI structure
"""

import pytest
from playwright.sync_api import Page, expect

def test_debug_inventory_structure(page: Page):
    """Debug test to see the actual inventory structure"""
    page.goto("http://localhost:8000")
    
    # Wait a bit for any dynamic content
    page.wait_for_timeout(5000)
    
    # Take a screenshot for debugging
    page.screenshot(path="debug_inventory.png")
    
    # Print the content of the inventory summary
    inventory_summary = page.locator("#inventory-summary")
    print("Inventory summary HTML:")
    print(inventory_summary.inner_html())
    
    # Check what classes/elements are actually present
    all_elements = page.locator("#inventory-summary *")
    count = all_elements.count()
    print(f"\nFound {count} elements in inventory summary:")
    
    for i in range(min(count, 10)):  # Limit to first 10 elements
        element = all_elements.nth(i)
        tag_name = element.evaluate("el => el.tagName")
        class_name = element.get_attribute("class") or ""
        text = element.inner_text()[:50] + "..." if len(element.inner_text()) > 50 else element.inner_text()
        print(f"  {i}: <{tag_name} class='{class_name}'>{text}")

def test_debug_network_requests(page: Page):
    """Debug test to check API calls"""
    
    # Monitor network requests
    requests = []
    
    def log_request(request):
        requests.append({
            'url': request.url,
            'method': request.method,
            'headers': dict(request.headers)
        })
    
    page.on("request", log_request)
    
    page.goto("http://localhost:8000")
    page.wait_for_timeout(5000)
    
    print("\nNetwork requests made:")
    for req in requests:
        if 'localhost:5001' in req['url']:
            print(f"  {req['method']} {req['url']}")
    
    # Check if API is responding
    response = page.request.get("http://localhost:5001/api/sample-data")
    print(f"\nAPI /api/sample-data response: {response.status}")
    if response.status == 200:
        data = response.json()
        print(f"Response keys: {data.keys()}")
        if 'summary' in data:
            print(f"Summary: {data['summary']}")