# Playwright Integration Guide

Comprehensive guide for integrating Playwright with various tools, frameworks, and CI/CD systems.

## CI/CD Integration

### GitHub Actions

#### Basic Setup
```yaml
name: Playwright Tests
on:
  push:
    branches: [ main, master ]
  pull_request:
    branches: [ main, master ]

jobs:
  test:
    timeout-minutes: 60
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    - uses: actions/setup-node@v4
      with:
        node-version: lts/*
    - name: Install dependencies
      run: npm ci
    - name: Install Playwright Browsers
      run: npx playwright install --with-deps
    - name: Run Playwright tests
      run: npx playwright test
    - uses: actions/upload-artifact@v4
      if: always()
      with:
        name: playwright-report
        path: playwright-report/
        retention-days: 30
```

#### Matrix Testing (Multiple Browsers)
```yaml
strategy:
  matrix:
    browser: [chromium, firefox, webkit]
steps:
  - name: Run Playwright tests
    run: npx playwright test --project=${{ matrix.browser }}
```

#### Sharding for Large Test Suites
```yaml
strategy:
  matrix:
    shard: [1/4, 2/4, 3/4, 4/4]
steps:
  - name: Run Playwright tests
    run: npx playwright test --shard=${{ matrix.shard }}
```

### Docker Integration

#### Dockerfile for Playwright Tests
```dockerfile
FROM mcr.microsoft.com/playwright:v1.40.0-focal

# Set the working directory
WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm ci

# Copy test files
COPY . .

# Run tests
CMD ["npx", "playwright", "test"]
```

#### Docker Compose for Development
```yaml
version: '3.8'
services:
  playwright-tests:
    build: .
    volumes:
      - ./tests:/app/tests
      - ./test-results:/app/test-results
    environment:
      - CI=true
    command: npx playwright test --reporter=html
```

### Azure DevOps

```yaml
trigger:
- main

pool:
  vmImage: 'ubuntu-latest'

steps:
- task: NodeTool@0
  inputs:
    versionSpec: '18'
  displayName: 'Install Node.js'

- script: |
    npm ci
    npx playwright install --with-deps
  displayName: 'Install dependencies'

- script: npx playwright test
  displayName: 'Run Playwright tests'

- task: PublishTestResults@2
  condition: always()
  inputs:
    testResultsFormat: 'JUnit'
    testResultsFiles: 'test-results/junit.xml'
    testRunTitle: 'Playwright Tests'

- task: PublishHtmlReport@1
  condition: always()
  inputs:
    reportDir: 'playwright-report'
```

### GitLab CI

```yaml
stages:
  - test

playwright-tests:
  stage: test
  image: mcr.microsoft.com/playwright:v1.40.0-focal
  script:
    - npm ci
    - npx playwright test
  artifacts:
    when: always
    paths:
      - playwright-report/
    reports:
      junit: test-results/junit.xml
  only:
    - main
    - merge_requests
```

### Jenkins Pipeline

```groovy
pipeline {
    agent {
        docker {
            image 'mcr.microsoft.com/playwright:v1.40.0-focal'
        }
    }
    stages {
        stage('Install Dependencies') {
            steps {
                sh 'npm ci'
            }
        }
        stage('Run Tests') {
            steps {
                sh 'npx playwright test'
            }
        }
    }
    post {
        always {
            publishHTML([
                allowMissing: false,
                alwaysLinkToLastBuild: true,
                keepAll: true,
                reportDir: 'playwright-report',
                reportFiles: 'index.html',
                reportName: 'Playwright Report'
            ])
        }
    }
}
```

## Testing Framework Integration

### Jest Integration
```javascript
// jest.config.js
module.exports = {
  testTimeout: 30000,
  setupFilesAfterEnv: ['<rootDir>/jest.setup.js']
};

// jest.setup.js
const { chromium } = require('playwright');

beforeAll(async () => {
  global.browser = await chromium.launch();
});

afterAll(async () => {
  await global.browser.close();
});

beforeEach(async () => {
  global.page = await global.browser.newPage();
});

afterEach(async () => {
  await global.page.close();
});
```

### Mocha Integration
```javascript
// test/setup.js
const { chromium } = require('playwright');

let browser, context, page;

before(async () => {
  browser = await chromium.launch();
});

after(async () => {
  await browser.close();
});

beforeEach(async () => {
  context = await browser.newContext();
  page = await context.newPage();
});

afterEach(async () => {
  await context.close();
});

module.exports = { getBrowser: () => browser, getPage: () => page };
```

### Cucumber Integration
```javascript
// features/support/world.js
const { setWorldConstructor, Before, After } = require('@cucumber/cucumber');
const { chromium } = require('playwright');

class CustomWorld {
  async openBrowser() {
    this.browser = await chromium.launch();
    this.context = await this.browser.newContext();
    this.page = await this.context.newPage();
  }

  async closeBrowser() {
    await this.browser.close();
  }
}

setWorldConstructor(CustomWorld);

Before(async function () {
  await this.openBrowser();
});

After(async function () {
  await this.closeBrowser();
});
```

## Language-Specific Integrations

### Python with Pytest

#### Configuration
```python
# conftest.py
import pytest
from playwright.sync_api import sync_playwright

@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        yield browser
        browser.close()

@pytest.fixture
def page(browser):
    context = browser.new_context()
    page = context.new_page()
    yield page
    context.close()
```

#### Django Integration
```python
# conftest.py
import pytest
from django.test import LiveServerTestCase
from playwright.sync_api import sync_playwright

@pytest.fixture(scope="session")
def live_server():
    from django.core.management import execute_from_command_line
    execute_from_command_line(['manage.py', 'runserver', '0:8081'])

@pytest.fixture
def django_page(live_server):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto("http://localhost:8081")
        yield page
        browser.close()
```

#### Flask Integration
```python
import pytest
from flask import Flask
from playwright.sync_api import sync_playwright
import threading
import time

@pytest.fixture(scope="session")
def flask_app():
    app = Flask(__name__)
    
    @app.route('/')
    def index():
        return '<h1>Test App</h1>'
    
    thread = threading.Thread(
        target=lambda: app.run(port=5001, debug=False, use_reloader=False)
    )
    thread.daemon = True
    thread.start()
    time.sleep(1)  # Give server time to start
    
    yield app

@pytest.fixture
def flask_page(flask_app):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto("http://localhost:5001")
        yield page
        browser.close()
```

### .NET Integration

```csharp
// PlaywrightTests.cs
using Microsoft.Playwright;
using Microsoft.Playwright.NUnit;
using NUnit.Framework;

[Parallelizable(ParallelScope.Self)]
[TestFixture]
public class PlaywrightTests : PageTest
{
    [Test]
    public async Task BasicTest()
    {
        await Page.GotoAsync("https://example.com");
        await Expect(Page).ToHaveTitleAsync(new Regex("Example"));
    }
}
```

### Java Integration

```java
// PlaywrightTest.java
import com.microsoft.playwright.*;
import org.junit.jupiter.api.*;

public class PlaywrightTest {
    private Playwright playwright;
    private Browser browser;
    private Page page;

    @BeforeAll
    void launchBrowser() {
        playwright = Playwright.create();
        browser = playwright.chromium().launch();
    }

    @BeforeEach
    void createPage() {
        page = browser.newPage();
    }

    @Test
    void basicTest() {
        page.navigate("https://example.com");
        assertThat(page).hasTitle(Pattern.compile("Example"));
    }

    @AfterEach
    void closePage() {
        page.close();
    }

    @AfterAll
    void closeBrowser() {
        browser.close();
        playwright.close();
    }
}
```

## Database Integration

### Database Setup and Teardown
```javascript
// Database integration with Playwright
const { test, expect } = require('@playwright/test');
const { Pool } = require('pg');

const pool = new Pool({
  user: 'testuser',
  host: 'localhost',
  database: 'testdb',
  password: 'password',
  port: 5432,
});

test.beforeEach(async () => {
  // Setup test data
  await pool.query('TRUNCATE TABLE users CASCADE');
  await pool.query(`
    INSERT INTO users (name, email) VALUES 
    ('Test User', 'test@example.com'),
    ('Another User', 'another@example.com')
  `);
});

test('user list displays correctly', async ({ page }) => {
  await page.goto('http://localhost:3000/users');
  
  await expect(page.getByText('Test User')).toBeVisible();
  await expect(page.getByText('Another User')).toBeVisible();
});

test.afterAll(async () => {
  await pool.end();
});
```

### MongoDB Integration
```javascript
const { MongoClient } = require('mongodb');

let client, db;

test.beforeAll(async () => {
  client = new MongoClient('mongodb://localhost:27017');
  await client.connect();
  db = client.db('testdb');
});

test.beforeEach(async () => {
  await db.collection('users').deleteMany({});
  await db.collection('users').insertMany([
    { name: 'Test User', email: 'test@example.com' },
    { name: 'Another User', email: 'another@example.com' }
  ]);
});

test.afterAll(async () => {
  await client.close();
});
```

## API Integration

### REST API Testing
```javascript
test('API and UI integration', async ({ request, page }) => {
  // Create data via API
  const response = await request.post('/api/users', {
    data: {
      name: 'API User',
      email: 'api@example.com'
    }
  });
  
  const user = await response.json();
  
  // Verify in UI
  await page.goto('/users');
  await expect(page.getByText(user.name)).toBeVisible();
  
  // Update via UI
  await page.getByTestId(`edit-${user.id}`).click();
  await page.getByLabel('Name').fill('Updated Name');
  await page.getByRole('button', { name: 'Save' }).click();
  
  // Verify via API
  const updatedResponse = await request.get(`/api/users/${user.id}`);
  const updatedUser = await updatedResponse.json();
  expect(updatedUser.name).toBe('Updated Name');
});
```

### GraphQL Integration
```javascript
test('GraphQL integration', async ({ request, page }) => {
  // GraphQL query
  const response = await request.post('/graphql', {
    data: {
      query: `
        mutation CreateUser($input: UserInput!) {
          createUser(input: $input) {
            id
            name
            email
          }
        }
      `,
      variables: {
        input: {
          name: 'GraphQL User',
          email: 'graphql@example.com'
        }
      }
    }
  });
  
  const { data } = await response.json();
  const user = data.createUser;
  
  // Verify in UI
  await page.goto('/users');
  await expect(page.getByText(user.name)).toBeVisible();
});
```

## Monitoring and Reporting

### Custom Test Reporter
```javascript
// custom-reporter.js
class CustomReporter {
  onBegin(config, suite) {
    console.log(`Starting tests with ${suite.allTests().length} tests`);
  }

  onTestEnd(test, result) {
    console.log(`Test ${test.title}: ${result.status}`);
    
    if (result.status === 'failed') {
      console.log(`Error: ${result.error.message}`);
    }
  }

  onEnd(result) {
    console.log(`Tests completed: ${result.status}`);
    console.log(`Passed: ${result.passed}, Failed: ${result.failed}`);
  }
}

module.exports = CustomReporter;
```

### Slack Integration
```javascript
// slack-reporter.js
const { WebClient } = require('@slack/web-api');

class SlackReporter {
  constructor() {
    this.slack = new WebClient(process.env.SLACK_TOKEN);
  }

  async onEnd(result) {
    const message = {
      channel: '#test-results',
      text: `Test Run Complete`,
      blocks: [
        {
          type: 'section',
          text: {
            type: 'mrkdwn',
            text: `*Test Results*\n✅ Passed: ${result.passed}\n❌ Failed: ${result.failed}`
          }
        }
      ]
    };

    if (result.failed > 0) {
      message.blocks.push({
        type: 'section',
        text: {
          type: 'mrkdwn',
          text: `🔗 <${process.env.REPORT_URL}|View Full Report>`
        }
      });
    }

    await this.slack.chat.postMessage(message);
  }
}
```

## Cloud Platform Integration

### AWS CodeBuild
```yaml
version: 0.2
phases:
  install:
    runtime-versions:
      nodejs: 18
  pre_build:
    commands:
      - npm ci
      - npx playwright install --with-deps
  build:
    commands:
      - npx playwright test
  post_build:
    commands:
      - echo "Tests completed"
artifacts:
  files:
    - playwright-report/**/*
```

### Google Cloud Build
```yaml
steps:
  - name: 'node:18'
    entrypoint: 'npm'
    args: ['ci']
  
  - name: 'mcr.microsoft.com/playwright:v1.40.0-focal'
    entrypoint: 'npx'
    args: ['playwright', 'test']
    
artifacts:
  objects:
    location: 'gs://my-bucket/playwright-reports'
    paths: ['playwright-report/**/*']
```

## Performance Monitoring Integration

### Lighthouse Integration
```javascript
const { test } = require('@playwright/test');
const { playAudit } = require('playwright-lighthouse');

test('lighthouse performance audit', async ({ page }) => {
  await page.goto('https://example.com');
  
  await playAudit({
    page,
    thresholds: {
      performance: 50,
      accessibility: 50,
      'best-practices': 50,
      seo: 50,
      pwa: 50,
    },
    port: 9222,
  });
});
```

### DataDog Integration
```javascript
const { test } = require('@playwright/test');
const { StatsD } = require('node-statsd');

const client = new StatsD({
  host: 'localhost',
  port: 8125,
  prefix: 'playwright.'
});

test('performance monitoring', async ({ page }) => {
  const start = Date.now();
  
  await page.goto('https://example.com');
  await page.waitForLoadState('networkidle');
  
  const duration = Date.now() - start;
  client.timing('page.load', duration);
  client.increment('test.completed');
});
```

## Best Practices for Integration

### Environment Management
```javascript
// config/environments.js
const environments = {
  development: {
    baseURL: 'http://localhost:3000',
    apiURL: 'http://localhost:3001/api',
    timeout: 30000
  },
  staging: {
    baseURL: 'https://staging.example.com',
    apiURL: 'https://api-staging.example.com',
    timeout: 60000
  },
  production: {
    baseURL: 'https://example.com',
    apiURL: 'https://api.example.com',
    timeout: 30000
  }
};

module.exports = environments[process.env.NODE_ENV || 'development'];
```

### Secrets Management
```javascript
// config/secrets.js
const secrets = {
  development: {
    apiKey: process.env.DEV_API_KEY,
    dbPassword: process.env.DEV_DB_PASSWORD
  },
  production: {
    apiKey: process.env.PROD_API_KEY,
    dbPassword: process.env.PROD_DB_PASSWORD
  }
};

module.exports = secrets[process.env.NODE_ENV];
```

### Parallel Execution Strategies
```javascript
// playwright.config.js
module.exports = {
  workers: process.env.CI ? 1 : undefined,
  fullyParallel: true,
  retries: process.env.CI ? 2 : 0,
  use: {
    trace: 'on-first-retry',
    screenshot: 'only-on-failure'
  },
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] }
    },
    {
      name: 'firefox',
      use: { ...devices['Desktop Firefox'] }
    },
    {
      name: 'webkit',
      use: { ...devices['Desktop Safari'] }
    }
  ]
};
```