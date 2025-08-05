# Playwright Code Examples and Patterns

Practical examples and common patterns for web automation and testing with Playwright.

## Basic Test Structure

### JavaScript/TypeScript
```typescript
import { test, expect } from '@playwright/test';

test('complete user flow', async ({ page }) => {
  // Navigate to page
  await page.goto('https://example.com');
  
  // Interact with elements
  await page.getByRole('button', { name: 'Get Started' }).click();
  
  // Fill forms
  await page.getByLabel('Email').fill('user@example.com');
  await page.getByLabel('Password').fill('securepassword');
  
  // Submit and verify
  await page.getByRole('button', { name: 'Sign In' }).click();
  await expect(page.getByText('Welcome')).toBeVisible();
});
```

### Python
```python
import re
from playwright.sync_api import Page, expect

def test_user_flow(page: Page):
    page.goto("https://example.com")
    
    page.get_by_role("button", name="Get Started").click()
    
    page.get_by_label("Email").fill("user@example.com")
    page.get_by_label("Password").fill("securepassword")
    
    page.get_by_role("button", name="Sign In").click()
    expect(page.get_by_text("Welcome")).to_be_visible()
```

## Form Interactions

### Comprehensive Form Handling
```typescript
test('form interactions', async ({ page }) => {
  await page.goto('https://forms-example.com');
  
  // Text inputs
  await page.getByLabel('First Name').fill('John');
  await page.getByPlaceholder('Enter your email').fill('john@example.com');
  
  // Checkboxes and radio buttons
  await page.getByRole('checkbox', { name: 'Subscribe to newsletter' }).check();
  await page.getByRole('radio', { name: 'Male' }).check();
  
  // Select dropdowns
  await page.getByLabel('Country').selectOption('United States');
  await page.selectOption('select#country', { label: 'United States' });
  
  // File uploads
  await page.getByLabel('Upload file').setInputFiles('path/to/file.pdf');
  
  // Multiple file uploads
  await page.getByLabel('Upload multiple').setInputFiles([
    'file1.pdf',
    'file2.jpg'
  ]);
  
  // Date inputs
  await page.getByLabel('Birth Date').fill('2023-12-25');
  
  // Submit form
  await page.getByRole('button', { name: 'Submit' }).click();
  
  // Verify submission
  await expect(page.getByText('Form submitted successfully')).toBeVisible();
});
```

## Navigation Patterns

### Multi-page Navigation
```typescript
test('navigation flow', async ({ page }) => {
  await page.goto('https://example.com');
  
  // Click links and navigate
  await page.getByRole('link', { name: 'Products' }).click();
  await expect(page).toHaveURL(/.*products/);
  
  // Use browser navigation
  await page.goBack();
  await expect(page).toHaveURL('https://example.com');
  
  await page.goForward();
  await expect(page).toHaveURL(/.*products/);
  
  // Wait for navigation to complete
  await Promise.all([
    page.waitForNavigation(),
    page.getByRole('link', { name: 'Contact' }).click()
  ]);
  
  // Wait for specific URL
  await page.waitForURL('**/contact');
});
```

### Single Page Application (SPA) Navigation
```typescript
test('SPA navigation', async ({ page }) => {
  await page.goto('https://spa-example.com');
  
  // Wait for SPA to load
  await page.waitForLoadState('networkidle');
  
  // Navigate within SPA
  await page.getByRole('link', { name: 'Dashboard' }).click();
  
  // Wait for URL change without page reload
  await page.waitForURL('**/dashboard');
  
  // Wait for content to load
  await page.waitForSelector('[data-testid="dashboard-content"]');
});
```

## Element Interaction Patterns

### Advanced Locator Strategies
```typescript
test('locator strategies', async ({ page }) => {
  await page.goto('https://complex-app.com');
  
  // Chaining locators
  const productCard = page.locator('.product-card').filter({ hasText: 'iPhone' });
  await productCard.getByRole('button', { name: 'Add to Cart' }).click();
  
  // Nth element selection
  await page.locator('.item').nth(2).click();
  await page.locator('.item').first().hover();
  await page.locator('.item').last().scrollIntoViewIfNeeded();
  
  // Complex filtering
  const activeButtons = page.getByRole('button').filter({ has: page.locator('.active') });
  await activeButtons.first().click();
  
  // Parent/child relationships
  const table = page.getByRole('table');
  const row = table.getByRole('row').filter({ hasText: 'John Doe' });
  await row.getByRole('button', { name: 'Edit' }).click();
});
```

### Drag and Drop
```typescript
test('drag and drop', async ({ page }) => {
  await page.goto('https://drag-drop-example.com');
  
  // Simple drag and drop
  await page.dragAndDrop('#source', '#target');
  
  // Drag and drop with custom steps
  const source = page.locator('#source');
  const target = page.locator('#target');
  
  await source.hover();
  await page.mouse.down();
  await target.hover();
  await page.mouse.up();
  
  // Verify drop result
  await expect(target).toContainText('Dropped item');
});
```

## Waiting Strategies

### Advanced Waiting Patterns
```typescript
test('waiting strategies', async ({ page }) => {
  await page.goto('https://dynamic-content.com');
  
  // Wait for network idle
  await page.waitForLoadState('networkidle');
  
  // Wait for specific element states
  await page.waitForSelector('.loading', { state: 'detached' });
  await page.waitForSelector('.content', { state: 'visible' });
  
  // Wait for custom conditions
  await page.waitForFunction(() => {
    return document.querySelectorAll('.item').length >= 10;
  });
  
  // Wait with timeout
  await page.waitForSelector('.slow-element', { timeout: 10000 });
  
  // Wait for multiple conditions
  await Promise.all([
    page.waitForResponse('**/api/data'),
    page.waitForSelector('.data-loaded'),
    page.getByRole('button', { name: 'Load Data' }).click()
  ]);
});
```

## API Testing Integration

### REST API Testing
```typescript
test('API integration', async ({ request, page }) => {
  // API calls
  const response = await request.get('https://api.example.com/users');
  expect(response.status()).toBe(200);
  
  const users = await response.json();
  expect(users).toHaveLength(10);
  
  // Create data via API, test in UI
  const newUser = await request.post('https://api.example.com/users', {
    data: {
      name: 'Test User',
      email: 'test@example.com'
    }
  });
  
  const userData = await newUser.json();
  
  // Verify in UI
  await page.goto('https://app.example.com/users');
  await expect(page.getByText(userData.name)).toBeVisible();
});
```

### Authentication Flows
```typescript
test('authentication flow', async ({ page, context }) => {
  // Login
  await page.goto('https://app.example.com/login');
  await page.getByLabel('Username').fill('testuser');
  await page.getByLabel('Password').fill('password123');
  await page.getByRole('button', { name: 'Login' }).click();
  
  // Save authentication state
  await context.storageState({ path: 'auth.json' });
  
  // Verify authenticated access
  await page.goto('https://app.example.com/dashboard');
  await expect(page.getByText('Welcome, testuser')).toBeVisible();
});

// Use saved authentication
test.use({ storageState: 'auth.json' });
test('protected page access', async ({ page }) => {
  await page.goto('https://app.example.com/dashboard');
  await expect(page.getByText('Dashboard')).toBeVisible();
});
```

## Network and Response Handling

### Network Interception
```typescript
test('network interception', async ({ page }) => {
  // Mock API responses
  await page.route('**/api/users', route => {
    route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify([
        { id: 1, name: 'Mock User 1' },
        { id: 2, name: 'Mock User 2' }
      ])
    });
  });
  
  // Modify requests
  await page.route('**/api/**', route => {
    const headers = route.request().headers();
    headers['authorization'] = 'Bearer mock-token';
    route.continue({ headers });
  });
  
  // Block requests
  await page.route('**/analytics/**', route => route.abort());
  
  await page.goto('https://app.example.com');
  await expect(page.getByText('Mock User 1')).toBeVisible();
});
```

### Response Validation
```typescript
test('response monitoring', async ({ page }) => {
  const responsePromise = page.waitForResponse('**/api/data');
  
  await page.goto('https://app.example.com');
  await page.getByRole('button', { name: 'Load Data' }).click();
  
  const response = await responsePromise;
  expect(response.status()).toBe(200);
  
  const data = await response.json();
  expect(data).toHaveProperty('items');
  expect(data.items).toHaveLength(5);
});
```

## Mobile and Responsive Testing

### Device Emulation
```typescript
import { devices } from '@playwright/test';

test('mobile testing', async ({ browser }) => {
  const context = await browser.newContext({
    ...devices['iPhone 12'],
    geolocation: { longitude: -122.4194, latitude: 37.7749 },
    permissions: ['geolocation']
  });
  
  const page = await context.newPage();
  await page.goto('https://mobile-app.example.com');
  
  // Mobile-specific interactions
  await page.locator('.menu-toggle').tap();
  await expect(page.locator('.mobile-menu')).toBeVisible();
  
  // Swipe gestures
  await page.touchscreen.tap(100, 200);
  
  // Orientation change
  await page.setViewportSize({ width: 812, height: 375 });
  
  await context.close();
});
```

## Error Handling and Debugging

### Comprehensive Error Handling
```typescript
test('error handling', async ({ page }) => {
  try {
    await page.goto('https://unreliable-site.com');
    
    // Handle slow elements
    const element = page.locator('.slow-element');
    await element.waitFor({ state: 'visible', timeout: 10000 });
    
  } catch (error) {
    if (error.name === 'TimeoutError') {
      console.log('Element took too long to appear');
      // Fallback action
      await page.reload();
    }
  }
  
  // Soft assertions (continue on failure)
  await expect.soft(page.locator('.optional')).toBeVisible();
  await expect.soft(page.locator('.another-optional')).toHaveText('Expected');
  
  // Continue with test even if soft assertions fail
  await page.getByRole('button', { name: 'Continue' }).click();
});
```

### Debug Information Collection
```typescript
test('debug helpers', async ({ page }) => {
  await page.goto('https://app.example.com');
  
  // Take screenshots
  await page.screenshot({ path: 'debug-screenshot.png' });
  
  // Get page content for debugging
  const title = await page.title();
  const url = page.url();
  console.log(`Page: ${title} at ${url}`);
  
  // Log network requests
  page.on('request', request => {
    console.log('Request:', request.method(), request.url());
  });
  
  // Log console messages
  page.on('console', msg => {
    console.log('Browser console:', msg.text());
  });
  
  // Get element information
  const element = page.locator('.debug-element');
  const text = await element.textContent();
  const isVisible = await element.isVisible();
  const boundingBox = await element.boundingBox();
  
  console.log(`Element text: ${text}, visible: ${isVisible}, bounds:`, boundingBox);
});
```

## Performance Testing

### Performance Monitoring
```typescript
test('performance monitoring', async ({ page }) => {
  // Start tracing
  await page.context().tracing.start({ screenshots: true, snapshots: true });
  
  const startTime = Date.now();
  await page.goto('https://performance-test.com');
  
  // Wait for page to be fully loaded
  await page.waitForLoadState('networkidle');
  const loadTime = Date.now() - startTime;
  
  // Get performance metrics
  const metrics = await page.evaluate(() => {
    const navigation = performance.getEntriesByType('navigation')[0];
    return {
      domContentLoaded: navigation.domContentLoadedEventEnd - navigation.domContentLoadedEventStart,
      loadComplete: navigation.loadEventEnd - navigation.loadEventStart,
      firstPaint: performance.getEntriesByName('first-paint')[0]?.startTime,
      firstContentfulPaint: performance.getEntriesByName('first-contentful-paint')[0]?.startTime
    };
  });
  
  console.log('Performance metrics:', metrics);
  expect(loadTime).toBeLessThan(3000); // Page should load in under 3 seconds
  
  // Stop tracing
  await page.context().tracing.stop({ path: 'trace.zip' });
});
```

## Data-Driven Testing

### Parametrized Tests
```typescript
const testData = [
  { name: 'John Doe', email: 'john@example.com', expected: 'Welcome John' },
  { name: 'Jane Smith', email: 'jane@example.com', expected: 'Welcome Jane' },
  { name: 'Bob Johnson', email: 'bob@example.com', expected: 'Welcome Bob' }
];

testData.forEach(({ name, email, expected }) => {
  test(`user registration for ${name}`, async ({ page }) => {
    await page.goto('https://app.example.com/register');
    
    await page.getByLabel('Name').fill(name);
    await page.getByLabel('Email').fill(email);
    await page.getByRole('button', { name: 'Register' }).click();
    
    await expect(page.getByText(expected)).toBeVisible();
  });
});
```

## Python-Specific Examples

### Pytest Integration
```python
import pytest
from playwright.sync_api import Page, expect

class TestUserManagement:
    def test_user_creation(self, page: Page):
        page.goto("https://app.example.com/users")
        
        page.get_by_role("button", name="Add User").click()
        page.get_by_label("Name").fill("Test User")
        page.get_by_label("Email").fill("test@example.com")
        page.get_by_role("button", name="Save").click()
        
        expect(page.get_by_text("User created successfully")).to_be_visible()
    
    @pytest.mark.parametrize("username,password,expected", [
        ("admin", "admin123", "Admin Dashboard"),
        ("user", "user123", "User Dashboard"),
        ("guest", "guest123", "Guest Dashboard")
    ])
    def test_login_roles(self, page: Page, username: str, password: str, expected: str):
        page.goto("https://app.example.com/login")
        
        page.get_by_label("Username").fill(username)
        page.get_by_label("Password").fill(password)
        page.get_by_role("button", name="Login").click()
        
        expect(page.get_by_text(expected)).to_be_visible()
```

### Async Python Example
```python
import asyncio
from playwright.async_api import async_playwright

async def run_automated_task():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        
        # Navigate and extract data
        await page.goto("https://data-source.com")
        
        # Wait for dynamic content
        await page.wait_for_selector(".data-table")
        
        # Extract data
        rows = await page.locator(".data-table tr").all()
        data = []
        
        for row in rows:
            cells = await row.locator("td").all_text_contents()
            data.append(cells)
        
        print(f"Extracted {len(data)} rows of data")
        
        await browser.close()
        return data

# Run the async function
data = asyncio.run(run_automated_task())
```