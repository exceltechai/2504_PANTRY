/**
 * Pantry & Commissary Recipe System - Frontend Application
 * Handles file uploads, recipe searches, and UI interactions
 */

// Configuration
const API_BASE_URL = window.location.hostname === 'localhost' ? 'http://localhost:5001' : '';

// DOM Elements
const pantryUpload = document.getElementById('pantry-upload');
const commissaryUpload = document.getElementById('commissary-upload');
const uploadBtn = document.getElementById('upload-btn');
const searchSection = document.querySelector('.search-section');
const resultsSection = document.querySelector('.results-section');
const searchBtn = document.getElementById('search-btn');
const loadingOverlay = document.getElementById('loading');
const resultsContainer = document.getElementById('results-container');
const inventorySummary = document.getElementById('inventory-summary');

// State management
let uploadedFiles = {
    pantry: null,
    commissary: null
};

let currentInventory = {
    pantry: [],
    commissary: [],
    using_sample_data: true
};

// Event listeners
pantryUpload.addEventListener('change', handleFileSelect);
commissaryUpload.addEventListener('change', handleFileSelect);
uploadBtn.addEventListener('click', handleUpload);
searchBtn.addEventListener('click', handleSearch);

// Initialize app
document.addEventListener('DOMContentLoaded', function() {
    console.log('Pantry & Commissary Recipe System initialized');
    checkAPIConnection();
    loadSampleData();
});

/**
 * Check if the API is accessible
 */
async function checkAPIConnection() {
    try {
        const response = await fetch(`${API_BASE_URL}/health`);
        const data = await response.json();
        
        if (data.status === 'healthy') {
            console.log('API connection established');
        } else {
            showError('API connection failed');
        }
    } catch (error) {
        console.error('API connection error:', error);
        showError('Unable to connect to the recipe service. Please ensure the backend is running.');
    }
}

/**
 * Load sample inventory data automatically
 */
async function loadSampleData() {
    try {
        const response = await fetch(`${API_BASE_URL}/api/sample-data`);
        const data = await response.json();
        
        if (response.ok && data.status === 'success') {
            currentInventory.pantry = data.pantry;
            currentInventory.commissary = data.commissary;
            currentInventory.using_sample_data = true;
            
            // Update UI to show loaded inventory
            displayInventorySummary(data);
            
            console.log(`Loaded ${data.summary.total_items} total ingredient availability items`);
            
            // Show ready message under search button
            showReadyMessage('Ready to search for recipes!');
        } else {
            throw new Error(data.message || 'Failed to load sample data');
        }
    } catch (error) {
        console.error('Error loading sample data:', error);
        inventorySummary.innerHTML = `
            <div class="error-message">
                <i class="fas fa-exclamation-triangle"></i>
                <p>Unable to load sample availability data. Please try uploading your own files.</p>
            </div>
        `;
    }
}

/**
 * Display inventory summary
 */
function displayInventorySummary(data) {
    const { summary } = data;
    const dataSource = currentInventory.using_sample_data ? 'sample' : 'uploaded';
    
    inventorySummary.innerHTML = `
        <div class="inventory-cards">
            <div class="inventory-card pantry-card">
                <div class="card-header">
                    <i class="fas fa-home"></i>
                    <h3>Pantry</h3>
                    <span class="badge">${summary.pantry_count} items</span>
                </div>
                <p>Free ingredients available at pantry</p>
            </div>
            
            <div class="inventory-card commissary-card">
                <div class="card-header">
                    <i class="fas fa-store"></i>
                    <h3>Commissary</h3>
                    <span class="badge">${summary.commissary_count} items</span>
                </div>
                <p>Reduced-cost ingredients available at commissary</p>
            </div>
            
            <div class="inventory-card total-card">
                <div class="card-header">
                    <i class="fas fa-list"></i>
                    <h3>Total</h3>
                    <span class="badge">${summary.total_items} items</span>
                </div>
                <p>Using ${dataSource === 'sample' ? 'default' : dataSource} availability data</p>
            </div>
        </div>
        
    `;
}

/**
 * Handle file selection
 */
function handleFileSelect(event) {
    const fileInput = event.target;
    const file = fileInput.files[0];
    const fileType = fileInput.id.includes('pantry') ? 'pantry' : 'commissary';
    
    if (file) {
        // Validate file type
        const allowedTypes = ['.csv', '.xlsx', '.xls'];
        const fileExtension = '.' + file.name.split('.').pop().toLowerCase();
        
        if (!allowedTypes.includes(fileExtension)) {
            showError(`Invalid file type. Please upload a CSV or Excel file.`);
            fileInput.value = '';
            return;
        }
        
        // Store the file
        uploadedFiles[fileType] = file;
        
        // Update UI
        const label = fileInput.nextElementSibling;
        label.innerHTML = `<i class="fas fa-check"></i> ${file.name}`;
        label.style.backgroundColor = '#28a745';
        
        // Enable upload button if at least one file is selected
        checkUploadReadiness();
    }
}

/**
 * Check if upload button should be enabled
 */
function checkUploadReadiness() {
    const hasFiles = uploadedFiles.pantry || uploadedFiles.commissary;
    uploadBtn.disabled = !hasFiles;
}

/**
 * Handle file upload
 */
async function handleUpload() {
    if (!uploadedFiles.pantry && !uploadedFiles.commissary) {
        showError('Please select at least one file to upload');
        return;
    }
    
    showLoading('Processing your inventory files...');
    
    try {
        const formData = new FormData();
        
        if (uploadedFiles.pantry) {
            formData.append('pantry', uploadedFiles.pantry);
        }
        
        if (uploadedFiles.commissary) {
            formData.append('commissary', uploadedFiles.commissary);
        }
        
        const response = await fetch(`${API_BASE_URL}/api/upload`, {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (response.ok) {
            showSuccess('Custom files uploaded successfully!');
            
            // Mark as using custom data
            currentInventory.using_sample_data = false;
            
            // Update inventory display to show custom files are being used
            inventorySummary.innerHTML = `
                <div class="inventory-cards">
                    <div class="inventory-card custom-card">
                        <div class="card-header">
                            <i class="fas fa-upload"></i>
                            <h3>Custom Files</h3>
                            <span class="badge">Uploaded</span>
                        </div>
                        <p>Using your uploaded availability lists</p>
                    </div>
                </div>
                
            `;
            
            // Show ready message for custom data
            showReadyMessage('Ready to search for recipes with your custom availability data!');
            
            // Scroll to search section
            searchSection.scrollIntoView({ behavior: 'smooth' });
        } else {
            showError(`Upload failed: ${data.message}`);
        }
    } catch (error) {
        console.error('Upload error:', error);
        showError('Upload failed. Please try again.');
    } finally {
        hideLoading();
    }
}

/**
 * Handle recipe search
 */
async function handleSearch() {
    const dishType = document.getElementById('dish-type').value;
    const cuisine = document.getElementById('cuisine').value;
    
    showLoading('Searching for recipes...');
    
    try {
        const params = new URLSearchParams({
            type: dishType,
            limit: '10'
        });
        
        if (cuisine) {
            params.append('cuisine', cuisine);
        }
        
        const response = await fetch(`${API_BASE_URL}/api/recipes?${params}`);
        const data = await response.json();
        
        if (response.ok) {
            displayResults(data.recipes);
            
            // Show results section
            resultsSection.style.display = 'block';
            
            // Scroll to results section
            resultsSection.scrollIntoView({ behavior: 'smooth' });
        } else {
            showError(`Search failed: ${data.message}`);
        }
    } catch (error) {
        console.error('Search error:', error);
        showError('Search failed. Please try again.');
    } finally {
        hideLoading();
    }
}

/**
 * Display recipe results
 */
function displayResults(recipes) {
    if (!recipes || recipes.length === 0) {
        resultsContainer.innerHTML = `
            <div class="text-center">
                <i class="fas fa-utensils" style="font-size: 3rem; color: #ccc; margin-bottom: 20px;"></i>
                <h3>No recipes found</h3>
                <p>Try adjusting your search criteria or uploading different inventory files.</p>
            </div>
        `;
        return;
    }
    
    resultsContainer.innerHTML = recipes.map(recipe => {
        const analysis = recipe.ingredient_analysis || {};
        return `
        <div class="recipe-card">
            <h3><i class="fas fa-utensils"></i> ${recipe.title}</h3>
            <p>${recipe.summary ? recipe.summary.substring(0, 150) + '...' : 'A delicious Whole30-compliant recipe'}</p>
            
            <div class="match-percentage">
                <i class="fas fa-percentage"></i> ${analysis.match_percentage || 0}% ingredients available
            </div>
            
            <div class="ingredient-sources">
                <span class="source-tag source-pantry">
                    <i class="fas fa-home"></i> Pantry: ${analysis.pantry_count || 0}
                </span>
                <span class="source-tag source-commissary">
                    <i class="fas fa-store"></i> Commissary: ${analysis.commissary_count || 0}
                </span>
                <span class="source-tag source-store">
                    <i class="fas fa-shopping-cart"></i> Store: ${analysis.store_count || 0}
                </span>
            </div>
            
            <div class="grocery-lists" style="margin-top: 15px;">
                <details class="grocery-details">
                    <summary style="cursor: pointer; color: #666; font-size: 0.9rem;">
                        <i class="fas fa-shopping-list"></i> View Shopping Lists
                    </summary>
                    <div class="grocery-breakdown" style="margin-top: 10px; padding: 10px; background: #f8f9fa; border-radius: 5px;">
                        ${generateGroceryList(analysis)}
                    </div>
                </details>
            </div>
            
            <div class="priority-score" style="margin-top: 10px;">
                <i class="fas fa-star"></i> Priority Score: ${analysis.priority_score ? (analysis.priority_score * 100).toFixed(1) : 0}%
            </div>
            
            <div style="margin-top: 15px;">
                <span style="color: #666;">
                    <i class="fas fa-list"></i> ${analysis.total_ingredients || 0} total ingredients
                </span>
            </div>
            
            ${recipe.spoonacular_url ? `
                <div style="margin-top: 15px;">
                    <a href="${recipe.spoonacular_url}" target="_blank" class="btn-primary" style="display: inline-block; text-decoration: none;">
                        <i class="fas fa-external-link-alt"></i> View Recipe
                    </a>
                </div>
            ` : ''}
        </div>
        `
    }).join('');
}

/**
 * Generate detailed grocery list breakdown by source
 */
function generateGroceryList(analysis) {
    let html = '';
    
    // Pantry items (free)
    if (analysis.pantry_ingredients && analysis.pantry_ingredients.length > 0) {
        html += `
            <div class="grocery-section" style="margin-bottom: 15px;">
                <h4 style="color: #28a745; margin-bottom: 8px; font-size: 0.9rem;">
                    <i class="fas fa-home"></i> Pantry (Free)
                </h4>
                <ul style="margin: 0; padding-left: 20px; color: #666;">
                    ${analysis.pantry_ingredients.map(ingredient => 
                        `<li style="margin-bottom: 3px;">${ingredient}</li>`
                    ).join('')}
                </ul>
            </div>
        `;
    }
    
    // Commissary items (reduced cost)
    if (analysis.commissary_ingredients && analysis.commissary_ingredients.length > 0) {
        html += `
            <div class="grocery-section" style="margin-bottom: 15px;">
                <h4 style="color: #007bff; margin-bottom: 8px; font-size: 0.9rem;">
                    <i class="fas fa-store"></i> Commissary (Reduced Cost)
                </h4>
                <ul style="margin: 0; padding-left: 20px; color: #666;">
                    ${analysis.commissary_ingredients.map(ingredient => 
                        `<li style="margin-bottom: 3px;">${ingredient}</li>`
                    ).join('')}
                </ul>
            </div>
        `;
    }
    
    // Store items (full price)
    if (analysis.store_ingredients && analysis.store_ingredients.length > 0) {
        html += `
            <div class="grocery-section">
                <h4 style="color: #dc3545; margin-bottom: 8px; font-size: 0.9rem;">
                    <i class="fas fa-shopping-cart"></i> Supermarket (Full Price)
                </h4>
                <ul style="margin: 0; padding-left: 20px; color: #666;">
                    ${analysis.store_ingredients.map(ingredient => 
                        `<li style="margin-bottom: 3px;">${ingredient}</li>`
                    ).join('')}
                </ul>
            </div>
        `;
    }
    
    if (!html) {
        html = '<p style="color: #999; font-style: italic;">No ingredient breakdown available</p>';
    }
    
    return html;
}

/**
 * Show loading overlay
 */
function showLoading(message = 'Processing...') {
    const spinner = loadingOverlay.querySelector('.loading-spinner p');
    spinner.textContent = message;
    loadingOverlay.style.display = 'flex';
}

/**
 * Hide loading overlay
 */
function hideLoading() {
    loadingOverlay.style.display = 'none';
}

/**
 * Show success message
 */
function showSuccess(message) {
    showNotification(message, 'success');
}

/**
 * Show error message
 */
function showError(message) {
    showNotification(message, 'error');
}

/**
 * Show notification
 */
function showNotification(message, type = 'info') {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.innerHTML = `
        <i class="fas fa-${type === 'success' ? 'check-circle' : 'exclamation-triangle'}"></i>
        <span>${message}</span>
        <button onclick="this.parentElement.remove()" class="notification-close">
            <i class="fas fa-times"></i>
        </button>
    `;
    
    // Add styles
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: ${type === 'success' ? '#d4edda' : '#f8d7da'};
        color: ${type === 'success' ? '#155724' : '#721c24'};
        padding: 15px 20px;
        border-radius: 5px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        z-index: 1001;
        display: flex;
        align-items: center;
        gap: 10px;
        max-width: 400px;
        border: 1px solid ${type === 'success' ? '#c3e6cb' : '#f5c6cb'};
    `;
    
    // Add close button styles
    const closeBtn = notification.querySelector('.notification-close');
    closeBtn.style.cssText = `
        background: none;
        border: none;
        color: inherit;
        cursor: pointer;
        font-size: 0.9rem;
        padding: 0;
        margin-left: 10px;
    `;
    
    // Add to page
    document.body.appendChild(notification);
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
        if (notification.parentElement) {
            notification.remove();
        }
    }, 5000);
}

// Utility functions
/**
 * Show ready message under search button
 */
function showReadyMessage(message) {
    const readyMessage = document.getElementById('ready-message');
    if (readyMessage) {
        readyMessage.querySelector('span').textContent = message;
        readyMessage.style.display = 'block';
    }
}

function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}