# Whole30 Recipe Agent Specification v1

## Project Overview

A cost-effective web application that helps users find Whole30-compliant recipes by intelligently matching ingredients against their available pantry (free) and commissary (reduced cost) inventories. The system prioritizes recipes that maximize the use of already-available ingredients, reducing grocery costs and food waste.

### Core Value Proposition
- **Cost Optimization**: Prioritizes free pantry items, then reduced-cost commissary items
- **Smart Matching**: Fuzzy ingredient matching handles variations in naming
- **Minimal Infrastructure**: Designed for low-cost deployment and maintenance
- **User-Friendly**: Simple interface with sensible defaults

## Architecture: Client-Heavy Approach

To minimize hosting costs and server load, this specification adopts a **client-side heavy architecture** where most processing happens in the browser, with minimal backend API calls only for recipe fetching.

### Key Architectural Decisions:
- **Client-side Excel parsing**: Uses SheetJS in browser (no server processing cost)
- **Static file hosting**: Can be deployed on GitHub Pages, Netlify free tier, or local file system
- **Minimal backend**: Only needed for recipe API proxy (to hide API keys)
- **Progressive enhancement**: Works offline with cached recipes
- **Mobile responsive**: Ensures accessibility on all devices

## Output Structure

**Directory Structure**: `recipe_agent/`

```
recipe_agent/
├── index.html          # Main application interface
├── styles.css          # All styling and responsive design
├── app.js             # Core application logic
├── api-proxy.js       # Minimal Node.js backend (optional)
├── data/              # Default data files
│   ├── pantry.csv     # Default pantry inventory
│   └── commissary.csv # Default commissary inventory
└── README.md          # Setup and deployment instructions
```

## File Specifications

### **index.html** - Application Structure
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Whole30 Recipe Finder - Smart Ingredient Matching</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <div class="app-container">
        <header class="app-header">
            <h1>🥗 Whole30 Recipe Finder</h1>
            <p class="tagline">Find recipes using your pantry & commissary items</p>
        </header>

        <main class="app-main">
            <!-- Step 1: Recipe Preferences -->
            <section class="input-section" id="preferences-section">
                <h2>What are you looking for?</h2>
                <div class="preference-inputs">
                    <div class="form-group">
                        <label for="recipe-type">Recipe Type:</label>
                        <select id="recipe-type" data-preference="type">
                            <option value="">Any type</option>
                            <option value="breakfast">Breakfast</option>
                            <option value="main course">Main Dish</option>
                            <option value="side dish">Side Dish</option>
                            <option value="snack">Snack</option>
                            <option value="dessert">Dessert</option>
                        </select>
                    </div>
                    
                    <div class="form-group">
                        <label for="flavor-profile">Flavor Profile:</label>
                        <input type="text" id="flavor-profile" 
                               placeholder="e.g., spicy, mild, savory"
                               data-preference="flavor">
                    </div>
                    
                    <div class="form-group">
                        <label for="cuisine-type">Cuisine:</label>
                        <input type="text" id="cuisine-type" 
                               placeholder="e.g., Mediterranean, Thai, Mexican"
                               data-preference="cuisine">
                    </div>
                </div>
                
                <button class="primary-button" id="find-recipes">
                    Find Recipes
                </button>
            </section>

            <!-- Step 2: Inventory Management -->
            <section class="inventory-section" id="inventory-section">
                <h2>Your Inventory</h2>
                <div class="inventory-tabs">
                    <button class="tab-button active" data-tab="pantry">
                        Pantry (Free)
                    </button>
                    <button class="tab-button" data-tab="commissary">
                        Commissary (Reduced Cost)
                    </button>
                </div>
                
                <div class="inventory-content">
                    <div class="file-upload-area">
                        <p>Using default inventory. Upload custom Excel file:</p>
                        <input type="file" id="inventory-upload" accept=".xlsx,.xls,.csv">
                        <button class="secondary-button" id="reset-inventory">
                            Reset to Default
                        </button>
                    </div>
                    
                    <div class="inventory-preview" id="inventory-preview">
                        <!-- Dynamically populated inventory items -->
                    </div>
                </div>
            </section>

            <!-- Step 3: Recipe Results -->
            <section class="results-section" id="results-section" style="display: none;">
                <h2>Recipe Matches</h2>
                <div class="results-container" id="recipe-results">
                    <!-- Dynamically populated recipe cards -->
                </div>
            </section>

            <!-- Step 4: Recipe Details -->
            <section class="details-section" id="details-section" style="display: none;">
                <button class="back-button" id="back-to-results">
                    ← Back to Results
                </button>
                <div class="recipe-details" id="recipe-details">
                    <!-- Dynamically populated recipe details -->
                </div>
            </section>
        </main>

        <footer class="app-footer">
            <p>Whole30 Recipe Finder • Prioritizing your pantry & commissary items</p>
        </footer>
    </div>

    <!-- Loading indicator -->
    <div class="loading-overlay" id="loading" style="display: none;">
        <div class="spinner"></div>
        <p>Finding the best recipes for you...</p>
    </div>

    <!-- External libraries -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/xlsx/0.18.5/xlsx.full.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/fuse.js/6.6.2/fuse.min.js"></script>
    <script src="app.js"></script>
</body>
</html>
```

### **styles.css** - Visual Design & Responsiveness
```css
/* CSS Variables for Theming */
:root {
    --primary-color: #2ecc71;      /* Whole30 green */
    --secondary-color: #27ae60;     
    --accent-color: #e74c3c;        /* For warnings/important */
    --text-primary: #2c3e50;
    --text-secondary: #7f8c8d;
    --bg-primary: #ffffff;
    --bg-secondary: #f8f9fa;
    --bg-tertiary: #ecf0f1;
    --border-color: #dde1e3;
    --shadow: 0 2px 8px rgba(0,0,0,0.1);
    --radius: 8px;
    --spacing-unit: 1rem;
}

/* Reset and Base Styles */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    line-height: 1.6;
    color: var(--text-primary);
    background-color: var(--bg-secondary);
}

/* Layout Components */
.app-container {
    min-height: 100vh;
    display: flex;
    flex-direction: column;
}

.app-header {
    background: var(--bg-primary);
    padding: calc(var(--spacing-unit) * 2);
    text-align: center;
    border-bottom: 1px solid var(--border-color);
    box-shadow: var(--shadow);
}

.app-header h1 {
    color: var(--primary-color);
    font-size: 2rem;
    margin-bottom: 0.5rem;
}

.tagline {
    color: var(--text-secondary);
    font-size: 1.1rem;
}

.app-main {
    flex: 1;
    max-width: 1200px;
    margin: 0 auto;
    padding: calc(var(--spacing-unit) * 2);
    width: 100%;
}

/* Section Styling */
section {
    background: var(--bg-primary);
    border-radius: var(--radius);
    padding: calc(var(--spacing-unit) * 2);
    margin-bottom: calc(var(--spacing-unit) * 2);
    box-shadow: var(--shadow);
}

section h2 {
    color: var(--text-primary);
    margin-bottom: calc(var(--spacing-unit) * 1.5);
    font-size: 1.5rem;
}

/* Form Elements */
.preference-inputs {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: var(--spacing-unit);
    margin-bottom: calc(var(--spacing-unit) * 2);
}

.form-group {
    display: flex;
    flex-direction: column;
}

.form-group label {
    margin-bottom: 0.5rem;
    font-weight: 500;
    color: var(--text-primary);
}

.form-group input,
.form-group select {
    padding: 0.75rem;
    border: 1px solid var(--border-color);
    border-radius: calc(var(--radius) / 2);
    font-size: 1rem;
    transition: border-color 0.3s;
}

.form-group input:focus,
.form-group select:focus {
    outline: none;
    border-color: var(--primary-color);
}

/* Buttons */
.primary-button,
.secondary-button {
    padding: 0.75rem 2rem;
    border: none;
    border-radius: calc(var(--radius) / 2);
    font-size: 1rem;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.3s;
}

.primary-button {
    background: var(--primary-color);
    color: white;
}

.primary-button:hover {
    background: var(--secondary-color);
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(46, 204, 113, 0.3);
}

.secondary-button {
    background: var(--bg-tertiary);
    color: var(--text-primary);
}

.secondary-button:hover {
    background: var(--border-color);
}

/* Inventory Section */
.inventory-tabs {
    display: flex;
    gap: var(--spacing-unit);
    margin-bottom: calc(var(--spacing-unit) * 1.5);
}

.tab-button {
    padding: 0.5rem 1.5rem;
    background: var(--bg-tertiary);
    border: 1px solid var(--border-color);
    border-radius: calc(var(--radius) / 2);
    cursor: pointer;
    transition: all 0.3s;
}

.tab-button.active {
    background: var(--primary-color);
    color: white;
    border-color: var(--primary-color);
}

.file-upload-area {
    background: var(--bg-secondary);
    padding: var(--spacing-unit);
    border-radius: calc(var(--radius) / 2);
    margin-bottom: var(--spacing-unit);
    text-align: center;
}

.inventory-preview {
    max-height: 200px;
    overflow-y: auto;
    border: 1px solid var(--border-color);
    border-radius: calc(var(--radius) / 2);
    padding: var(--spacing-unit);
}

/* Recipe Cards */
.results-container {
    display: grid;
    gap: var(--spacing-unit);
}

.recipe-card {
    background: var(--bg-secondary);
    border-radius: var(--radius);
    padding: calc(var(--spacing-unit) * 1.5);
    cursor: pointer;
    transition: all 0.3s;
    border: 1px solid var(--border-color);
}

.recipe-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 8px 16px rgba(0,0,0,0.1);
    border-color: var(--primary-color);
}

.recipe-title {
    font-size: 1.25rem;
    color: var(--text-primary);
    margin-bottom: 0.5rem;
}

.ingredient-match {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    margin-bottom: 0.5rem;
}

.match-percentage {
    font-weight: bold;
    color: var(--primary-color);
}

.ingredient-sources {
    display: flex;
    gap: 0.5rem;
    flex-wrap: wrap;
}

.source-badge {
    padding: 0.25rem 0.75rem;
    border-radius: 1rem;
    font-size: 0.875rem;
    font-weight: 500;
}

.source-badge.pantry {
    background: #d4edda;
    color: #155724;
}

.source-badge.commissary {
    background: #cce5ff;
    color: #004085;
}

.source-badge.store {
    background: #f8d7da;
    color: #721c24;
}

/* Recipe Details */
.recipe-details {
    display: grid;
    gap: calc(var(--spacing-unit) * 2);
}

.ingredients-table {
    width: 100%;
    border-collapse: collapse;
}

.ingredients-table th,
.ingredients-table td {
    padding: 0.75rem;
    text-align: left;
    border-bottom: 1px solid var(--border-color);
}

.ingredients-table th {
    background: var(--bg-tertiary);
    font-weight: 600;
}

/* Loading State */
.loading-overlay {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(255, 255, 255, 0.95);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    z-index: 1000;
}

.spinner {
    width: 50px;
    height: 50px;
    border: 4px solid var(--border-color);
    border-top-color: var(--primary-color);
    border-radius: 50%;
    animation: spin 1s linear infinite;
}

@keyframes spin {
    to { transform: rotate(360deg); }
}

/* Responsive Design */
@media (max-width: 768px) {
    .app-main {
        padding: var(--spacing-unit);
    }
    
    section {
        padding: var(--spacing-unit);
    }
    
    .preference-inputs {
        grid-template-columns: 1fr;
    }
    
    .inventory-tabs {
        flex-direction: column;
    }
    
    .tab-button {
        width: 100%;
    }
}

/* Print Styles */
@media print {
    .app-header,
    .app-footer,
    .back-button,
    .file-upload-area {
        display: none;
    }
    
    .recipe-details {
        color: black;
    }
}
```

### **app.js** - Core Application Logic
```javascript
'use strict';

// Application State
const AppState = {
    pantryItems: [],
    commissaryItems: [],
    currentRecipes: [],
    selectedRecipe: null,
    preferences: {
        type: '',
        flavor: '',
        cuisine: ''
    },
    // Configuration
    config: {
        fuzzyThreshold: 80,
        minIngredientMatch: 0.9,
        recipesPerSearch: 3,
        apiEndpoint: '/api/recipes' // Or direct Spoonacular with API key
    }
};

// Initialize Fuse.js for fuzzy matching
let pantryFuse, commissaryFuse;

// DOM Elements
const elements = {
    findRecipesBtn: document.getElementById('find-recipes'),
    recipeType: document.getElementById('recipe-type'),
    flavorProfile: document.getElementById('flavor-profile'),
    cuisineType: document.getElementById('cuisine-type'),
    inventoryUpload: document.getElementById('inventory-upload'),
    resetInventory: document.getElementById('reset-inventory'),
    inventoryPreview: document.getElementById('inventory-preview'),
    resultsSection: document.getElementById('results-section'),
    recipeResults: document.getElementById('recipe-results'),
    detailsSection: document.getElementById('details-section'),
    recipeDetails: document.getElementById('recipe-details'),
    backToResults: document.getElementById('back-to-results'),
    loading: document.getElementById('loading'),
    tabButtons: document.querySelectorAll('.tab-button')
};

// Initialize Application
document.addEventListener('DOMContentLoaded', async () => {
    await loadDefaultInventories();
    setupEventListeners();
    initializeFuzzySearch();
});

// Load default CSV files
async function loadDefaultInventories() {
    try {
        const [pantryResponse, commissaryResponse] = await Promise.all([
            fetch('data/pantry.csv'),
            fetch('data/commissary.csv')
        ]);
        
        const pantryText = await pantryResponse.text();
        const commissaryText = await commissaryResponse.text();
        
        AppState.pantryItems = parseCSV(pantryText);
        AppState.commissaryItems = parseCSV(commissaryText);
        
        updateInventoryPreview('pantry');
    } catch (error) {
        console.error('Error loading default inventories:', error);
        showNotification('Using empty inventories. Please upload your files.', 'warning');
    }
}

// Parse CSV text to array of items
function parseCSV(csvText) {
    const lines = csvText.trim().split('\n');
    const headers = lines[0].split(',').map(h => h.trim());
    
    return lines.slice(1).map(line => {
        const values = line.split(',').map(v => v.trim());
        const item = {};
        headers.forEach((header, index) => {
            item[header] = values[index] || '';
        });
        return item;
    });
}

// Setup all event listeners
function setupEventListeners() {
    // Find recipes button
    elements.findRecipesBtn.addEventListener('click', handleFindRecipes);
    
    // File upload
    elements.inventoryUpload.addEventListener('change', handleFileUpload);
    
    // Reset inventory
    elements.resetInventory.addEventListener('click', loadDefaultInventories);
    
    // Tab switching
    elements.tabButtons.forEach(button => {
        button.addEventListener('click', (e) => {
            elements.tabButtons.forEach(b => b.classList.remove('active'));
            e.target.classList.add('active');
            updateInventoryPreview(e.target.dataset.tab);
        });
    });
    
    // Back button
    elements.backToResults.addEventListener('click', () => {
        elements.detailsSection.style.display = 'none';
        elements.resultsSection.style.display = 'block';
    });
    
    // Enter key on inputs
    [elements.flavorProfile, elements.cuisineType].forEach(input => {
        input.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') handleFindRecipes();
        });
    });
}

// Initialize Fuse.js for fuzzy searching
function initializeFuzzySearch() {
    const options = {
        includeScore: true,
        threshold: 0.4,
        keys: ['Item', 'Name', 'Description']
    };
    
    pantryFuse = new Fuse(AppState.pantryItems, options);
    commissaryFuse = new Fuse(AppState.commissaryItems, options);
}

// Handle file upload
async function handleFileUpload(event) {
    const file = event.target.files[0];
    if (!file) return;
    
    const reader = new FileReader();
    const isCSV = file.name.endsWith('.csv');
    
    reader.onload = async (e) => {
        try {
            let items;
            if (isCSV) {
                items = parseCSV(e.target.result);
            } else {
                // Excel file
                const workbook = XLSX.read(e.target.result, { type: 'binary' });
                const sheetName = workbook.SheetNames[0];
                const sheet = workbook.Sheets[sheetName];
                items = XLSX.utils.sheet_to_json(sheet);
            }
            
            // Determine which inventory to update based on active tab
            const activeTab = document.querySelector('.tab-button.active').dataset.tab;
            if (activeTab === 'pantry') {
                AppState.pantryItems = items;
            } else {
                AppState.commissaryItems = items;
            }
            
            updateInventoryPreview(activeTab);
            initializeFuzzySearch();
            showNotification(`${activeTab} inventory updated successfully!`, 'success');
        } catch (error) {
            console.error('Error parsing file:', error);
            showNotification('Error reading file. Please check the format.', 'error');
        }
    };
    
    if (isCSV) {
        reader.readAsText(file);
    } else {
        reader.readAsBinaryString(file);
    }
}

// Update inventory preview
function updateInventoryPreview(type) {
    const items = type === 'pantry' ? AppState.pantryItems : AppState.commissaryItems;
    const preview = elements.inventoryPreview;
    
    if (items.length === 0) {
        preview.innerHTML = '<p class="empty-state">No items loaded</p>';
        return;
    }
    
    const itemNames = items.map(item => item.Item || item.Name || 'Unknown').slice(0, 20);
    preview.innerHTML = `
        <p><strong>${items.length} items loaded</strong></p>
        <p class="item-preview">${itemNames.join(', ')}${items.length > 20 ? '...' : ''}</p>
    `;
}

// Handle find recipes
async function handleFindRecipes() {
    // Collect preferences
    AppState.preferences = {
        type: elements.recipeType.value,
        flavor: elements.flavorProfile.value,
        cuisine: elements.cuisineType.value
    };
    
    // Show loading
    showLoading(true);
    
    try {
        // In production, this would call your backend API
        // For now, we'll simulate with sample data
        const recipes = await fetchRecipes(AppState.preferences);
        
        // Process recipes with ingredient matching
        AppState.currentRecipes = recipes.map(recipe => {
            const analysis = analyzeIngredients(recipe.ingredients);
            return {
                ...recipe,
                ingredientAnalysis: analysis,
                matchPercentage: analysis.availableCount / analysis.totalCount
            };
        });
        
        // Sort by match percentage
        AppState.currentRecipes.sort((a, b) => b.matchPercentage - a.matchPercentage);
        
        // Display results
        displayRecipeResults();
        
    } catch (error) {
        console.error('Error fetching recipes:', error);
        showNotification('Error finding recipes. Please try again.', 'error');
    } finally {
        showLoading(false);
    }
}

// Fetch recipes (simulate API call or use real endpoint)
async function fetchRecipes(preferences) {
    // Option 1: Use your backend proxy
    if (AppState.config.apiEndpoint.startsWith('/api')) {
        const params = new URLSearchParams(preferences);
        const response = await fetch(`${AppState.config.apiEndpoint}?${params}`);
        return await response.json();
    }
    
    // Option 2: Direct Spoonacular call (requires API key in frontend - not recommended)
    // Option 3: Return mock data for testing
    return getMockRecipes();
}

// Analyze recipe ingredients against inventory
function analyzeIngredients(ingredients) {
    const analysis = {
        pantry: [],
        commissary: [],
        unavailable: [],
        totalCount: ingredients.length,
        availableCount: 0
    };
    
    ingredients.forEach(ingredient => {
        const pantryMatch = fuzzyMatch(ingredient, pantryFuse);
        const commissaryMatch = fuzzyMatch(ingredient, commissaryFuse);
        
        if (pantryMatch && pantryMatch.score >= (100 - AppState.config.fuzzyThreshold)) {
            analysis.pantry.push({ ingredient, match: pantryMatch.item });
            analysis.availableCount++;
        } else if (commissaryMatch && commissaryMatch.score >= (100 - AppState.config.fuzzyThreshold)) {
            analysis.commissary.push({ ingredient, match: commissaryMatch.item });
            analysis.availableCount++;
        } else {
            analysis.unavailable.push(ingredient);
        }
    });
    
    return analysis;
}

// Fuzzy match helper
function fuzzyMatch(ingredient, fuseInstance) {
    if (!fuseInstance) return null;
    
    const results = fuseInstance.search(ingredient);
    if (results.length > 0) {
        return {
            item: results[0].item,
            score: (1 - results[0].score) * 100 // Convert to percentage
        };
    }
    return null;
}

// Display recipe results
function displayRecipeResults() {
    elements.resultsSection.style.display = 'block';
    elements.detailsSection.style.display = 'none';
    
    elements.recipeResults.innerHTML = AppState.currentRecipes.map((recipe, index) => `
        <div class="recipe-card" onclick="showRecipeDetails(${index})">
            <h3 class="recipe-title">${recipe.title}</h3>
            <div class="ingredient-match">
                <span class="match-percentage">${Math.round(recipe.matchPercentage * 100)}% match</span>
                <span class="match-details">
                    ${recipe.ingredientAnalysis.availableCount}/${recipe.ingredientAnalysis.totalCount} ingredients available
                </span>
            </div>
            <div class="ingredient-sources">
                ${recipe.ingredientAnalysis.pantry.length > 0 ? 
                    `<span class="source-badge pantry">Pantry: ${recipe.ingredientAnalysis.pantry.length}</span>` : ''}
                ${recipe.ingredientAnalysis.commissary.length > 0 ? 
                    `<span class="source-badge commissary">Commissary: ${recipe.ingredientAnalysis.commissary.length}</span>` : ''}
                ${recipe.ingredientAnalysis.unavailable.length > 0 ? 
                    `<span class="source-badge store">Store: ${recipe.ingredientAnalysis.unavailable.length}</span>` : ''}
            </div>
        </div>
    `).join('');
}

// Show recipe details
function showRecipeDetails(index) {
    const recipe = AppState.currentRecipes[index];
    AppState.selectedRecipe = recipe;
    
    elements.resultsSection.style.display = 'none';
    elements.detailsSection.style.display = 'block';
    
    elements.recipeDetails.innerHTML = `
        <h2>${recipe.title}</h2>
        ${recipe.url ? `<p><a href="${recipe.url}" target="_blank">View original recipe →</a></p>` : ''}
        
        <div class="recipe-info">
            <h3>Ingredients</h3>
            <table class="ingredients-table">
                <thead>
                    <tr>
                        <th>Ingredient</th>
                        <th>Source</th>
                        <th>Status</th>
                    </tr>
                </thead>
                <tbody>
                    ${renderIngredientRows(recipe)}
                </tbody>
            </table>
        </div>
        
        <div class="recipe-instructions">
            <h3>Instructions</h3>
            ${recipe.instructions ? `<ol>${recipe.instructions.map(step => 
                `<li>${step}</li>`).join('')}</ol>` : '<p>Please visit the original recipe for instructions.</p>'}
        </div>
        
        ${recipe.nutrition ? `
        <div class="recipe-nutrition">
            <h3>Nutrition Information</h3>
            <p>Calories: ${recipe.nutrition.calories}</p>
            <p>Protein: ${recipe.nutrition.protein}g</p>
            <p>Carbs: ${recipe.nutrition.carbs}g</p>
            <p>Fat: ${recipe.nutrition.fat}g</p>
        </div>
        ` : ''}
    `;
}

// Render ingredient rows for the table
function renderIngredientRows(recipe) {
    const rows = [];
    
    // Pantry items
    recipe.ingredientAnalysis.pantry.forEach(({ ingredient, match }) => {
        rows.push(`
            <tr>
                <td>${ingredient}</td>
                <td><span class="source-badge pantry">Pantry</span></td>
                <td>✓ Available (matches: ${match.Item || match.Name})</td>
            </tr>
        `);
    });
    
    // Commissary items
    recipe.ingredientAnalysis.commissary.forEach(({ ingredient, match }) => {
        rows.push(`
            <tr>
                <td>${ingredient}</td>
                <td><span class="source-badge commissary">Commissary</span></td>
                <td>✓ Available (matches: ${match.Item || match.Name})</td>
            </tr>
        `);
    });
    
    // Unavailable items
    recipe.ingredientAnalysis.unavailable.forEach(ingredient => {
        rows.push(`
            <tr>
                <td>${ingredient}</td>
                <td><span class="source-badge store">Store</span></td>
                <td>✗ Need to purchase</td>
            </tr>
        `);
    });
    
    return rows.join('');
}

// UI Helper Functions
function showLoading(show) {
    elements.loading.style.display = show ? 'flex' : 'none';
}

function showNotification(message, type = 'info') {
    // Simple notification - could be enhanced with a toast library
    console.log(`[${type.toUpperCase()}] ${message}`);
    // TODO: Implement visual notifications
}

// Mock data for testing
function getMockRecipes() {
    return [
        {
            title: "Mediterranean Breakfast Bowl",
            ingredients: ["eggs", "spinach", "tomatoes", "olive oil", "garlic", "feta cheese"],
            url: "https://example.com/recipe1",
            instructions: ["Heat oil", "Sauté vegetables", "Add eggs", "Season and serve"]
        },
        {
            title: "Spicy Chicken Stir-Fry",
            ingredients: ["chicken breast", "broccoli", "peppers", "garlic", "ginger", "coconut aminos"],
            url: "https://example.com/recipe2"
        },
        {
            title: "Whole30 Sweet Potato Hash",
            ingredients: ["sweet potato", "ground beef", "onion", "bell pepper", "paprika", "cumin"],
            url: "https://example.com/recipe3"
        }
    ];
}

// Make showRecipeDetails available globally for onclick handlers
window.showRecipeDetails = showRecipeDetails;
```

### **api-proxy.js** - Minimal Backend (Optional)
```javascript
// Minimal Node.js/Express backend for API key protection
// Deploy to free services like Vercel, Netlify Functions, or Railway

const express = require('express');
const axios = require('axios');
const cors = require('cors');

const app = express();
app.use(cors());
app.use(express.json());

// Environment variables
const SPOONACULAR_API_KEY = process.env.SPOONACULAR_API_KEY;
const PORT = process.env.PORT || 3000;

// Recipe search endpoint
app.get('/api/recipes', async (req, res) => {
    try {
        const { type, flavor, cuisine } = req.query;
        
        // Build Spoonacular query
        const params = {
            apiKey: SPOONACULAR_API_KEY,
            diet: 'whole30',
            number: 10,
            type: type || undefined,
            cuisine: cuisine || undefined,
            query: flavor || undefined,
            instructionsRequired: true,
            fillIngredients: true,
            addRecipeInformation: true
        };
        
        const response = await axios.get(
            'https://api.spoonacular.com/recipes/complexSearch',
            { params }
        );
        
        // Transform response
        const recipes = response.data.results.map(recipe => ({
            id: recipe.id,
            title: recipe.title,
            url: recipe.sourceUrl,
            ingredients: recipe.extendedIngredients?.map(ing => ing.name) || [],
            instructions: recipe.analyzedInstructions?.[0]?.steps?.map(s => s.step) || [],
            nutrition: recipe.nutrition
        }));
        
        res.json(recipes);
    } catch (error) {
        console.error('API Error:', error);
        res.status(500).json({ error: 'Failed to fetch recipes' });
    }
});

// Health check
app.get('/health', (req, res) => {
    res.json({ status: 'healthy' });
});

app.listen(PORT, () => {
    console.log(`API proxy running on port ${PORT}`);
});
```

## Key Features & Implementation Details

### 1. **Client-Side Excel Processing**
- Uses SheetJS (xlsx) library loaded from CDN
- No server processing required, reducing costs
- Handles both .xlsx and .csv formats
- Preserves original data structure

### 2. **Fuzzy Matching with Fuse.js**
- Client-side fuzzy string matching
- Configurable threshold (default: 80%)
- Searches across multiple fields (Item, Name, Description)
- Real-time performance with no API calls

### 3. **Progressive Web Approach**
- Works offline with cached default inventories
- Mobile-responsive design
- Fast initial load with minimal dependencies
- Can be installed as a PWA with minor additions

### 4. **Cost-Effective Architecture**
- Static files can be hosted free (GitHub Pages, Netlify)
- Optional minimal backend only for API key protection
- Client does heavy lifting, server just proxies API calls
- Can work entirely client-side with exposed API key for personal use

## Deployment Options

### **Option 1: Fully Static (Cheapest)**
1. Host on GitHub Pages or Netlify (free)
2. Include Spoonacular API key in frontend (only for personal use)
3. No backend required
4. Cost: $0/month

### **Option 2: Serverless Functions (Recommended)**
1. Frontend on Netlify/Vercel (free)
2. API proxy as serverless function (free tier)
3. Protects API keys
4. Cost: $0/month for light usage

### **Option 3: Self-Hosted**
1. Run on personal NAS or Raspberry Pi
2. Use nginx for static files
3. Node.js for API proxy
4. Cost: Only electricity

## Future Enhancements (TODO)

### **High Priority**
- [ ] Cache recipe searches in localStorage
- [ ] Add ingredient quantity parsing
- [ ] Implement recipe favoriting system
- [ ] Add "I made this" tracking

### **Medium Priority**
- [ ] Multi-user support with profiles
- [ ] Meal planning calendar
- [ ] Shopping list generation
- [ ] Recipe rating system

### **Low Priority**
- [ ] OCR for receipt scanning
- [ ] Barcode scanning for inventory
- [ ] Integration with grocery delivery APIs
- [ ] Social sharing features

## Development Quickstart

```bash
# Clone repository
git clone [repository-url]
cd recipe_agent

# Install dependencies (if using backend)
npm install

# Set environment variable
export SPOONACULAR_API_KEY=your_key_here

# Run locally
# Frontend only:
python -m http.server 8000
# With backend:
node api-proxy.js

# Deploy to Netlify
netlify deploy --prod
```

## Cost Analysis

**Monthly costs for different approaches:**
- GitHub Pages + Exposed API key: $0
- Netlify + Functions (10k requests): $0
- Vercel + Serverless (100k requests): $0
- AWS S3 + Lambda (light usage): ~$1-2
- Dedicated VPS: $5-10

**Recommended: Netlify with serverless functions** - provides the best balance of features, security, and cost for a small user base.