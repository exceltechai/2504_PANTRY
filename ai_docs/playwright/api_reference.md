# Playwright API Reference

Comprehensive reference for Playwright's core APIs across JavaScript/TypeScript and Python.

## Core Classes

### Playwright
The main entry point for launching browsers.

#### JavaScript/TypeScript
```javascript
const { chromium, firefox, webkit } = require('playwright');
```

#### Python
```python
from playwright.sync_api import sync_playwright
from playwright.async_api import async_playwright
```

**Key Properties:**
- `chromium` - Chromium browser launcher
- `firefox` - Firefox browser launcher  
- `webkit` - WebKit browser launcher
- `devices` - Predefined device configurations
- `errors` - Custom error classes
- `request` - Web API testing utilities
- `selectors` - Custom selector engine registration

---

### Browser
Represents a browser instance.

#### Key Methods

**`newContext(options?)`**
```javascript
const context = await browser.newContext({
  viewport: { width: 1280, height: 720 },
  userAgent: 'custom-user-agent',
  locale: 'en-US',
  timezoneId: 'America/New_York'
});
```

**`newPage()`**
```javascript
const page = await browser.newPage();
```

**`close()`**
```javascript
await browser.close();
```

**`contexts()`**
```javascript
const contexts = browser.contexts();
```

**`version()`**
```javascript
const version = browser.version();
```

---

### BrowserContext
Isolated environment equivalent to an incognito profile.

#### Key Methods

**`newPage()`**
```javascript
const page = await context.newPage();
```

**`pages()`**
```javascript
const pages = context.pages();
```

**`close()`**
```javascript
await context.close();
```

**`cookies(urls?)`**
```javascript
const cookies = await context.cookies();
```

**`addCookies(cookies)`**
```javascript
await context.addCookies([{
  name: 'session',
  value: 'abc123',
  domain: 'example.com',
  path: '/'
}]);
```

**`route(url, handler)`**
```javascript
await context.route('**/api/**', route => {
  route.continue({ headers: { ...route.request().headers(), 'x-test': 'true' } });
});
```

---

### Page
Represents a single tab or popup window.

#### Navigation Methods

**`goto(url, options?)`**
```javascript
await page.goto('https://example.com', {
  waitUntil: 'domcontentloaded',
  timeout: 30000
});
```

**`reload(options?)`**
```javascript
await page.reload();
```

**`goBack(options?)`** / **`goForward(options?)`**
```javascript
await page.goBack();
await page.goForward();
```

#### Locator Methods

**`locator(selector)`**
```javascript
const button = page.locator('button');
const specificButton = page.locator('button', { hasText: 'Submit' });
```

**`getByRole(role, options?)`**
```javascript
await page.getByRole('button', { name: 'Submit' }).click();
await page.getByRole('textbox', { name: 'Email' }).fill('test@example.com');
```

**`getByText(text, options?)`**
```javascript
await page.getByText('Welcome').click();
await page.getByText(/Hello .*/i).hover();
```

**`getByLabel(text, options?)`**
```javascript
await page.getByLabel('Email address').fill('user@example.com');
```

**`getByPlaceholder(text, options?)`**
```javascript
await page.getByPlaceholder('Search...').fill('playwright');
```

**`getByTestId(testId)`**
```javascript
await page.getByTestId('submit-button').click();
```

#### Evaluation Methods

**`evaluate(pageFunction, arg?)`**
```javascript
const title = await page.evaluate(() => document.title);
const result = await page.evaluate(([a, b]) => a + b, [1, 2]);
```

**`evaluateHandle(pageFunction, arg?)`**
```javascript
const bodyHandle = await page.evaluateHandle(() => document.body);
```

**`exposeFunction(name, callback)`**
```javascript
await page.exposeFunction('sha256', text => crypto.createHash('sha256').update(text).digest('hex'));
```

**`addInitScript(script, arg?)`**
```javascript
await page.addInitScript(() => {
  window.customProperty = 'test-value';
});
```

#### Interaction Methods

**`click(selector, options?)`**
```javascript
await page.click('button');
await page.click('button', { button: 'right', clickCount: 2 });
```

**`fill(selector, value, options?)`**
```javascript
await page.fill('input[name="email"]', 'test@example.com');
```

**`type(selector, text, options?)`**
```javascript
await page.type('input', 'Hello World', { delay: 100 });
```

**`press(selector, key, options?)`**
```javascript
await page.press('input', 'Enter');
await page.press('input', 'Control+A');
```

**`dragAndDrop(source, target, options?)`**
```javascript
await page.dragAndDrop('#source', '#target');
```

#### Wait Methods

**`waitForSelector(selector, options?)`**
```javascript
await page.waitForSelector('.loading', { state: 'detached' });
```

**`waitForLoadState(state?, options?)`**
```javascript
await page.waitForLoadState('networkidle');
```

**`waitForURL(url, options?)`**
```javascript
await page.waitForURL('**/dashboard');
```

**`waitForFunction(pageFunction, arg?, options?)`**
```javascript
await page.waitForFunction(() => window.customReady === true);
```

#### Page Lifecycle

**`close(options?)`**
```javascript
await page.close();
```

**`isClosed()`**
```javascript
const closed = page.isClosed();
```

---

### Locator
Represents a way to find element(s) on the page.

#### Key Methods

**`click(options?)`**
```javascript
await locator.click();
await locator.click({ position: { x: 10, y: 10 } });
```

**`fill(value, options?)`**
```javascript
await locator.fill('new value');
```

**`hover(options?)`**
```javascript
await locator.hover();
```

**`textContent(options?)`**
```javascript
const text = await locator.textContent();
```

**`innerHTML(options?)`**
```javascript
const html = await locator.innerHTML();
```

**`getAttribute(name, options?)`**
```javascript
const href = await locator.getAttribute('href');
```

**`isVisible(options?)`**
```javascript
const visible = await locator.isVisible();
```

**`isEnabled(options?)`**
```javascript
const enabled = await locator.isEnabled();
```

**Filtering Methods:**
```javascript
const rows = page.locator('tr');
const evenRows = rows.nth(1);
const filteredRows = rows.filter({ hasText: 'Product' });
const firstVisibleRow = rows.first();
const lastVisibleRow = rows.last();
```

---

## Python API Specifics

### Sync vs Async APIs

#### Sync API
```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto("https://example.com")
    browser.close()
```

#### Async API
```python
import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto("https://example.com")
        await browser.close()

asyncio.run(main())
```

### Python Method Naming
Python methods use snake_case instead of camelCase:

```python
# JavaScript: page.getByRole()
page.get_by_role("button", name="Submit")

# JavaScript: page.waitForSelector()
page.wait_for_selector(".loading")

# JavaScript: page.addInitScript()
page.add_init_script("window.test = true")
```

---

## Test Framework API

### Test Function
```javascript
import { test, expect } from '@playwright/test';

test('basic test', async ({ page }) => {
  await page.goto('https://example.com');
  await expect(page).toHaveTitle(/Example/);
});
```

### Test Hooks
```javascript
test.describe('Feature tests', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/login');
  });

  test.afterEach(async ({ page }) => {
    await page.close();
  });

  test('should work', async ({ page }) => {
    // test implementation
  });
});
```

### Fixtures
```javascript
test('test with custom fixture', async ({ page, browser }) => {
  // page and browser are built-in fixtures
});
```

---

## Assertions

### Auto-retrying Assertions
```javascript
// Wait for element to be visible
await expect(locator).toBeVisible();

// Wait for element to have text
await expect(locator).toHaveText('Expected text');

// Wait for page to have title
await expect(page).toHaveTitle(/Page Title/);

// Wait for element to have attribute
await expect(locator).toHaveAttribute('href', '/expected-url');

// Wait for element to have count
await expect(page.locator('.item')).toHaveCount(5);
```

### Python Test Assertions
```python
from playwright.sync_api import expect

# Element assertions
expect(page.locator("button")).to_be_visible()
expect(page.locator("input")).to_have_value("expected")

# Page assertions  
expect(page).to_have_title("Expected Title")
expect(page).to_have_url("https://example.com")
```

---

## Configuration

### Playwright Config (JavaScript)
```javascript
// playwright.config.js
module.exports = {
  testDir: './tests',
  timeout: 30000,
  use: {
    browserName: 'chromium',
    headless: false,
    viewport: { width: 1280, height: 720 },
    screenshot: 'only-on-failure',
    video: 'retain-on-failure'
  },
  projects: [
    { name: 'Chrome', use: { browserName: 'chromium' } },
    { name: 'Firefox', use: { browserName: 'firefox' } },
    { name: 'Safari', use: { browserName: 'webkit' } }
  ]
};
```

### Pytest Configuration (Python)
```python
# pytest.ini
[tool:pytest]
addopts = --browser chromium --browser firefox --browser webkit
```

---

## Error Handling

### Common Error Types
```javascript
// TimeoutError
try {
  await page.waitForSelector('.missing-element', { timeout: 5000 });
} catch (error) {
  if (error.name === 'TimeoutError') {
    console.log('Element not found within timeout');
  }
}

// Strict mode errors (multiple elements found)
const button = page.locator('button').first(); // Avoid strict mode error
```

### Python Error Handling
```python
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError

try:
    page.wait_for_selector(".missing", timeout=5000)
except PlaywrightTimeoutError:
    print("Element not found")
```