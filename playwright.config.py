"""
Playwright configuration for end-to-end testing
"""

from playwright.sync_api import Playwright
import os

# Configuration
BASE_URL = "http://localhost:8000"
API_BASE_URL = "http://localhost:5001"

def configure_playwright():
    """Configure Playwright for testing"""
    return {
        'base_url': BASE_URL,
        'timeout': 30000,  # 30 seconds default timeout
        'use': {
            'screenshot': 'only-on-failure',
            'video': 'retain-on-failure',
            'trace': 'retain-on-failure',
            'viewport': {'width': 1280, 'height': 720},
            'ignore_https_errors': True,
        },
        'browsers': [
            {
                'name': 'chromium',
                'use': {
                    'channel': 'chrome',
                }
            }
        ],
        'projects': [
            {
                'name': 'Desktop Chrome',
                'use': {
                    'browser_name': 'chromium',
                    'viewport': {'width': 1280, 'height': 720},
                }
            },
            {
                'name': 'Mobile Chrome',
                'use': {
                    'browser_name': 'chromium',
                    'viewport': {'width': 375, 'height': 667},
                }
            }
        ]
    }