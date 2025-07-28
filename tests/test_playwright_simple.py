"""
Simple Playwright test to verify setup
"""

import pytest
from playwright.sync_api import Page, expect

def test_application_loads_sync(page: Page):
    """Test that the application loads correctly (sync version)"""
    page.goto("http://localhost:8000")
    
    # Check page title
    expect(page).to_have_title("Pantry & Commissary Recipe System")
    
    # Check main heading
    heading = page.locator("h1")
    expect(heading).to_contain_text("Pantry & Commissary Recipe System")
    
    # Check that main sections are present
    expect(page.locator(".sample-data-section")).to_be_visible()
    expect(page.locator(".search-section")).to_be_visible()

def test_sample_data_loads_sync(page: Page):
    """Test that sample inventory data loads automatically (sync version)"""
    page.goto("http://localhost:8000")
    
    # Wait for inventory summary to load
    inventory_summary = page.locator("#inventory-summary")
    expect(inventory_summary).to_be_visible()
    
    # Check that loading spinner is replaced with inventory data
    page.wait_for_selector(".loading-inventory", state="detached", timeout=10000)
    
    # Verify inventory summary appears
    summary_content = page.locator("#inventory-summary .inventory-cards")
    expect(summary_content).to_be_visible(timeout=10000)