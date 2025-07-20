# Playwright Quick Reference for AI Development

AI-optimized quick reference for common Playwright patterns and APIs.

## Installation & Setup

### Node.js/TypeScript
```bash
npm init playwright@latest
npx playwright test
```

### Python
```bash
pip install pytest-playwright
playwright install
```

## Core API Patterns

### Basic Test Structure
```javascript
import { test, expect } from '@playwright/test';

test('test name', async ({ page }) => {
  await page.goto('URL');
  await page.locator('selector').click();
  await expect(page.locator('result')).toBeVisible();
});
```

### Page Navigation
```javascript
await page.goto('https://example.com');
await page.reload();
await page.goBack();
await page.goForward();
```

## Element Selection Priority

**1. User-facing locators (RECOMMENDED):**
```javascript
page.getByRole('button', { name: 'Submit' })     // Accessibility-focused
page.getByText('Welcome')                        // Content-based  
page.getByLabel('Email')                         // Form labels
page.getByPlaceholder('Search...')               // Input placeholders
page.getByTestId('submit-btn')                   // Test IDs
```

**2. CSS/XPath (use sparingly):**
```javascript
page.locator('.submit-button')
page.locator('//button[@type="submit"]')
```

## Common Interactions

### Form Handling
```javascript
await page.getByLabel('Email').fill('user@example.com');
await page.getByLabel('Password').fill('password');
await page.getByRole('checkbox', { name: 'Remember me' }).check();
await page.getByLabel('Country').selectOption('United States');
await page.getByLabel('Upload').setInputFiles('file.pdf');
await page.getByRole('button', { name: 'Submit' }).click();
```

### Element Interactions
```javascript
await locator.click();                    // Click element
await locator.hover();                    // Hover over element
await locator.fill('text');              // Fill input field
await locator.type('text', { delay: 100 }); // Type with delay
await locator.press('Enter');            // Press key
await locator.dragTo(target);            // Drag and drop
```

## Waiting Strategies

### Auto-waiting (Built-in)
```javascript
await page.getByText('Loading...').waitFor({ state: 'detached' });
await page.getByText('Content').waitFor({ state: 'visible' });
```

### Custom Waiting
```javascript
await page.waitForLoadState('networkidle');
await page.waitForURL('**/dashboard');
await page.waitForFunction(() => window.dataLoaded);
await page.waitForResponse('**/api/data');
```

## Assertions (Auto-retrying)

### Element Assertions
```javascript
await expect(page.getByText('Success')).toBeVisible();
await expect(page.getByRole('button')).toBeEnabled();
await expect(page.getByLabel('Email')).toHaveValue('test@example.com');
await expect(page.getByText('Title')).toHaveText('Expected Title');
await expect(page.locator('.items')).toHaveCount(5);
```

### Page Assertions
```javascript
await expect(page).toHaveTitle('Page Title');
await expect(page).toHaveURL('https://example.com/dashboard');
```

## Browser & Context Management

### Browser Lifecycle
```javascript
const browser = await chromium.launch({ headless: false });
const context = await browser.newContext();
const page = await context.newPage();
// ... test actions
await browser.close();
```

### Mobile Emulation
```javascript
const context = await browser.newContext({
  ...devices['iPhone 12'],
  geolocation: { longitude: -122.4194, latitude: 37.7749 },
  permissions: ['geolocation']
});
```

## Network & API Integration

### API Testing
```javascript
test('API test', async ({ request }) => {
  const response = await request.post('/api/users', {
    data: { name: 'Test User', email: 'test@example.com' }
  });
  expect(response.status()).toBe(201);
  const user = await response.json();
  expect(user).toHaveProperty('id');
});
```

### Network Interception
```javascript
// Mock API response
await page.route('**/api/users', route => {
  route.fulfill({
    status: 200,
    contentType: 'application/json',
    body: JSON.stringify([{ id: 1, name: 'Mock User' }])
  });
});

// Modify request headers
await page.route('**/api/**', route => {
  route.continue({
    headers: { ...route.request().headers(), 'authorization': 'Bearer token' }
  });
});
```

## Authentication Patterns

### Login Flow
```javascript
test('login', async ({ page, context }) => {
  await page.goto('/login');
  await page.getByLabel('Username').fill('user');
  await page.getByLabel('Password').fill('password');
  await page.getByRole('button', { name: 'Login' }).click();
  
  // Save auth state
  await context.storageState({ path: 'auth.json' });
});

// Use saved auth
test.use({ storageState: 'auth.json' });
```

## Error Handling

### Try-Catch with Timeouts
```javascript
try {
  await page.getByText('Element').waitFor({ timeout: 5000 });
} catch (error) {
  if (error.name === 'TimeoutError') {
    console.log('Element not found, using fallback');
    await page.getByText('Fallback').click();
  }
}
```

### Soft Assertions
```javascript
await expect.soft(page.getByText('Optional')).toBeVisible();
await expect.soft(page.getByText('Another')).toHaveText('Expected');
// Test continues even if soft assertions fail
```

## Python Equivalents

### Basic Test (Python)
```python
def test_example(page: Page):
    page.goto("https://example.com")
    page.get_by_role("button", name="Submit").click()
    expect(page.get_by_text("Success")).to_be_visible()
```

### Method Name Conversion
```python
# JavaScript → Python
page.getByRole() → page.get_by_role()
page.waitForSelector() → page.wait_for_selector()
page.addInitScript() → page.add_init_script()
```

## Configuration Essentials

### Playwright Config
```javascript
module.exports = {
  testDir: './tests',
  timeout: 30000,
  retries: 2,
  workers: process.env.CI ? 1 : undefined,
  use: {
    browserName: 'chromium',
    headless: true,
    screenshot: 'only-on-failure',
    video: 'retain-on-failure',
    trace: 'on-first-retry'
  },
  projects: [
    { name: 'Desktop Chrome', use: { browserName: 'chromium' } },
    { name: 'Desktop Firefox', use: { browserName: 'firefox' } },
    { name: 'Desktop Safari', use: { browserName: 'webkit' } }
  ]
};
```

## CI/CD Quick Setup

### GitHub Actions
```yaml
- name: Install Playwright
  run: npx playwright install --with-deps
- name: Run tests
  run: npx playwright test
- name: Upload reports
  uses: actions/upload-artifact@v4
  if: always()
  with:
    name: playwright-report
    path: playwright-report/
```

### Docker
```dockerfile
FROM mcr.microsoft.com/playwright:v1.40.0-focal
WORKDIR /app
COPY . .
RUN npm ci
CMD ["npx", "playwright", "test"]
```

## Debugging Tools

### Debug Mode
```bash
npx playwright test --debug
npx playwright test --headed
npx playwright codegen https://example.com
```

### Screenshots & Traces
```javascript
await page.screenshot({ path: 'debug.png' });
await page.context().tracing.start({ screenshots: true });
// ... test actions
await page.context().tracing.stop({ path: 'trace.zip' });
```

## Performance Testing

### Timing Measurements
```javascript
const start = Date.now();
await page.goto('https://example.com');
await page.waitForLoadState('networkidle');
const loadTime = Date.now() - start;
expect(loadTime).toBeLessThan(3000);
```

### Core Web Vitals
```javascript
const metrics = await page.evaluate(() => {
  const navigation = performance.getEntriesByType('navigation')[0];
  return {
    FCP: performance.getEntriesByName('first-contentful-paint')[0]?.startTime,
    LCP: performance.getEntriesByName('largest-contentful-paint')[0]?.startTime,
    loadTime: navigation.loadEventEnd - navigation.loadEventStart
  };
});
```

## Common Patterns for AI Development

### Data Extraction
```javascript
const data = await page.locator('.data-row').evaluateAll(elements => 
  elements.map(el => ({
    name: el.querySelector('.name').textContent,
    value: el.querySelector('.value').textContent
  }))
);
```

### Form Automation
```javascript
const formData = [
  { label: 'Name', value: 'John Doe' },
  { label: 'Email', value: 'john@example.com' },
  { label: 'Phone', value: '555-1234' }
];

for (const field of formData) {
  await page.getByLabel(field.label).fill(field.value);
}
await page.getByRole('button', { name: 'Submit' }).click();
```

### Dynamic Content Handling
```javascript
// Wait for dynamic content to load
await page.waitForFunction(() => 
  document.querySelectorAll('.dynamic-item').length >= 5
);

// Handle infinite scroll
while (await page.getByText('Load More').isVisible()) {
  await page.getByText('Load More').click();
  await page.waitForTimeout(1000);
}
```

## Best Practices Checklist

✅ **Use user-facing locators** (`getByRole`, `getByText`, `getByLabel`)  
✅ **Leverage auto-waiting** (avoid manual timeouts)  
✅ **Use auto-retrying assertions** (`expect(locator).toBeVisible()`)  
✅ **Test across browsers** (Chromium, Firefox, WebKit)  
✅ **Keep tests isolated** (each test should be independent)  
✅ **Use Page Object Model** for complex applications  
✅ **Handle authentication state** (save/restore login sessions)  
✅ **Configure proper timeouts** for CI environments  
✅ **Use traces and screenshots** for debugging  
✅ **Mock external APIs** in tests  

## Troubleshooting

### Common Issues
```javascript
// Element not found → Use better locators
// ❌ page.locator('.btn-submit')
// ✅ page.getByRole('button', { name: 'Submit' })

// Flaky tests → Add proper waiting
// ❌ await page.click('button')
// ✅ await page.getByRole('button').click() // Auto-waits

// Timeout errors → Increase timeout or fix waiting strategy
await page.getByText('Slow element').waitFor({ timeout: 10000 });
```

### Debug Commands
```bash
npx playwright test --debug                    # Interactive debugging
npx playwright test --trace on               # Generate traces
npx playwright show-trace trace.zip          # View traces
npx playwright codegen example.com           # Generate test code
```