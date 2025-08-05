# Pantry-First Recipe Recommendation System Specification

This specification document outlines the architecture and implementation details for a Whole30-compliant recipe recommendation system that prioritizes ingredients from pantry (free) and commissary (reduced cost) sources over supermarket purchases.

## Core Concept

The system is designed as a streamlined web application that helps users find Whole30-compliant recipes which maximize the use of ingredients they already have access to. By creating a clear visual hierarchy between free pantry ingredients, reduced-cost commissary items, and full-price supermarket purchases, users can make economical meal choices while maintaining dietary compliance.

### Key Objectives

- Recommend strictly Whole30-compliant recipes, keeping broader health categories for future iterations
- Provide an intuitive, minimal dashboard interface that emphasizes usability
- Implement efficient ingredient matching with 80% threshold using fuzzy string comparison
- Utilize session-based storage for temporary file handling without persistent data

## System Architecture

The application follows a modular architecture with clear separation of concerns between frontend and backend components. This approach ensures maintainability and allows for iterative development as new features are added in the future.

### Frontend Components

The system presents a clean, minimal dashboard interface that focuses attention on recipe discovery. The design emphasizes white space, clear visual hierarchy, and color-coding to make the experience intuitive for users.

Key interface elements include:
- A prominent search bar for recipe queries
- Recipe cards showing ingredient source distribution
- A subtle file upload option tucked away in the footer
- Clear visual indicators for pantry (green), commissary (yellow), and supermarket (red) ingredients

### Backend Implementation

The system uses Flask for backend processing due to its simplicity and suitability for smaller applications. This lightweight Python framework handles API requests, session management, and data processing with minimal overhead.

Core backend functions include:
- Spoonacular API integration for retrieving Whole30-compliant recipes
- Fuzzy string matching for ingredient comparison at 80% threshold
- Session-based temporary storage for uploaded Excel files
- Recipe ranking based on pantry/commissary ingredient availability

## User Flow

The primary user flow is designed to be straightforward and efficient, accommodating the 98% use case where users don't need to upload custom inventory files. Users can immediately search for recipes upon arriving at the dashboard, with results ranked by ingredient availability from their pantry and commissary.

For the less common case where users want to use custom inventory data, a subtle "Upload Inventory" option is available but doesn't dominate the interface.

### File Upload Handling

When needed, the file upload panel provides a clean, focused interface for uploading Excel files. This component is intentionally minimalistic, using a modal approach that appears only when requested.

The system handles Excel parsing through Pandas, extracting structured data from the uploaded files and storing it temporarily in the session. No persistent storage is implemented in this version, keeping the architecture simple for initial deployment.

## Ingredient Matching Logic

A core technical feature of the system is its ingredient matching algorithm. This component uses fuzzy string matching to compare recipe ingredients against pantry and commissary inventory.

The matching process:
1. Cleans ingredient strings to remove quantities and descriptors
2. Compares the core ingredient name against inventory items
3. Returns matches above the 80% similarity threshold
4. Prioritizes pantry matches over commissary when both are available

This approach handles real-world variations in how ingredients are named and described, making the system practical for everyday use.

## Implementation Timeline

The development plan breaks down the project into manageable phases that can be completed in 4-6 weeks:

1. **Backend API Development** (1-2 weeks): Setting up Flask application structure, implementing Spoonacular API integration, and building ingredient matching logic
2. **Frontend Development** (1-2 weeks): Creating the responsive dashboard UI, implementing search and filtering interfaces, and building recipe card components
3. **Integration & Testing** (1 week): Connecting frontend to backend API, testing with sample data, and optimizing performance
4. **Deployment & Documentation** (1 week): Preparing the deployment environment and creating user/technical documentation

## Technical Requirements

### Backend Stack
- **Framework**: Flask (Python)
- **API Integration**: Spoonacular API for recipe data
- **Data Processing**: Pandas for Excel file handling
- **String Matching**: RapidFuzz for ingredient comparison
- **Session Management**: Flask sessions for temporary storage

### Frontend Stack
- **Architecture**: Modular HTML/CSS/JavaScript approach
- **Styling**: CSS with custom properties for theming
- **Interactivity**: Vanilla JavaScript with modern ES6+ patterns
- **Responsive Design**: Mobile-first approach

### File Structure
```
pantry-recipe-system/
â”œâ”€â”€ backend/
â”‚   â”œâ”€â”€ app.py
â”‚   â”œâ”€â”€ ingredient_matcher.py
â”‚   â””â”€â”€ requirements.txt
â”œâ”€â”€ frontend/
â”‚   â”œâ”€â”€ index.html
â”‚   â”œâ”€â”€ styles.css
â”‚   â””â”€â”€ script.js
â””â”€â”€ README.md
```

## API Endpoints

### GET /recipes/search
**Parameters:**
- `query` (string): Recipe search query
- `type` (string): Recipe type (breakfast, lunch, dinner, snack, side)

**Response:**
```json
{
  "recipes": [
    {
      "id": "12345",
      "title": "Mediterranean Breakfast Hash",
      "image": "https://...",
      "pantry_score": 0.85,
      "ingredient_breakdown": {
        "pantry": ["eggs", "olive oil", "onions"],
        "commissary": ["bell peppers", "tomatoes"],
        "supermarket": ["feta cheese"]
      }
    }
  ]
}
```

### GET /recipes/:id
**Response:**
```json
{
  "recipe": {
    "title": "Mediterranean Breakfast Hash",
    "instructions": ["Step 1...", "Step 2..."],
    "ingredients": [
      {
        "name": "eggs",
        "amount": "6 large",
        "source": "pantry"
      }
    ],
    "source_url": "https://...",
    "prep_time": 15,
    "cook_time": 20
  }
}
```

## User Interface Design

### Color Coding System
- **Green (#4CAF50)**: Pantry ingredients (free)
- **Orange (#FF9800)**: Commissary ingredients (reduced cost)
- **Red (#F44336)**: Supermarket ingredients (full price)

### Typography
- **Headers**: System font stack with fallbacks
- **Body**: Clean, readable font optimized for recipe content
- **Accent**: Monospace for ingredient quantities

### Layout Principles
- **Mobile-first**: Responsive design prioritizing mobile experience
- **Minimal interface**: Clean, uncluttered design
- **Progressive disclosure**: Advanced features available but not prominent

## Future Enhancements

While the initial version focuses on core functionality, several enhancements are planned for future iterations:

### Phase 2 Features
- Configurable fuzzy matching threshold for more precise ingredient matching
- Persistent storage options for saving pantry and commissary lists
- Enhanced ingredient substitution suggestions based on nutritional similarity
- Meal planning and automated shopping list generation

### Phase 3 Features
- Broader health category support beyond Whole30
- User accounts and recipe favorites
- Integration with grocery delivery services
- Nutritional analysis and dietary tracking

### Phase 4 Features
- Machine learning recommendations based on user preferences
- Community features and recipe sharing
- Mobile app development
- Advanced inventory management

## Testing Strategy

### Unit Testing
- Ingredient matching algorithm accuracy
- API endpoint responses
- Frontend component functionality

### Integration Testing
- Frontend-backend communication
- Third-party API reliability
- File upload and processing

### User Acceptance Testing
- Recipe discovery workflow
- Ingredient source accuracy
- Mobile responsiveness

## Deployment

### Development Environment
- Local Flask development server
- Live reload for frontend changes
- Mock data for testing without API limits

### Production Environment
- Cloud hosting (recommended: Heroku, Railway, or similar)
- Environment variables for API keys
- CDN for static assets
- SSL certificate for secure connections

## Conclusion

This specification provides a comprehensive blueprint for developing a Pantry-First Recipe Recommendation System that meets the specific requirements outlined. By focusing on simplicity, usability, and core functionality in the initial version, the system will provide immediate value while establishing a foundation for future enhancements.

The design prioritizes the most common use cases while still accommodating edge cases through thoughtful UI decisions and technical architecture choices. This balanced approach will result in a system that is both powerful and approachable for users seeking Whole30-compliant recipes that maximize their existing ingredient inventory.