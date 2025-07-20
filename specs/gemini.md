# Recipe Agent Specification v1

## 1\. Project Vision & Core Goal

To create a web-based assistant that simplifies healthy eating and reduces food costs. [cite\_start]The application will accept user-provided lists of available ingredients—one for a personal "Pantry" (free) and one for a "Commissary" (reduced-cost)—and recommend Whole30-compliant recipes that maximize the use of these on-hand items[cite: 2, 39]. The ultimate goal is to evolve this tool into a conversational "agent" that provides a seamless, guided user experience.

## 2\. Architectural Approach: Modular & Scalable

This project will adopt a modular architecture with a clear **separation of concerns** to ensure maintainability, scalability, and a professional development workflow. The architecture is split between a dynamic frontend that the user interacts with and a powerful backend that handles data processing and external communication.

  * **Frontend**: A modern, single-page application responsible for all user interface elements and interactions. It will be built with clean, semantic HTML, styled with CSS, and driven by JavaScript.
  * [cite\_start]**Backend**: A Python-based API server responsible for the core logic: processing uploaded Excel files, querying the external recipe database, performing ingredient matching, and returning prioritized results to the frontend[cite: 3, 7].

This two-part structure ensures that the complex data operations on the backend do not interfere with a fast, responsive user experience on the frontend.

## 3\. Core User Flow (MVP)

The initial version of the tool will guide the user through a simple, linear process:

1.  **Upload:** The user visits the application and is prompted to upload their `pantry.xlsx` and `commissary.xlsx` files.
2.  [cite\_start]**Query:** After the files are successfully processed, the user specifies the type of recipe they are looking for (e.g., breakfast, side dish, main dish)[cite: 10].
3.  **Process:** The frontend sends the recipe request to the backend. The backend then:
      * [cite\_start]Queries the Spoonacular API for relevant Whole30-compliant recipes[cite: 3, 43].
      * [cite\_start]For each recipe, it programmatically checks every ingredient against the user's pantry and commissary lists using fuzzy string matching[cite: 3, 45].
      * It calculates a "match score" for each recipe based on ingredient availability.
4.  [cite\_start]**Recommend:** The backend returns a list of the top 3-5 recipes, prioritized by the highest match score[cite: 47]. These are displayed to the user as visual "cards."
5.  [cite\_start]**Details:** The user selects a recipe card to view the full details, including a complete ingredient list clearly marking the source of each item (Pantry, Commissary, or Supermarket) and step-by-step cooking instructions[cite: 48, 51].

## 4\. Component Specification

The frontend will be built from the following reusable components, each with its own dedicated, modular file structure (`index.html`, `styles.css`, `script.js`).

### **`FileUploader` Component**

  * **Vision:** A clean, intuitive interface for uploading the two required Excel files, based directly on your sketch.
  * **Structure (`index.html`):**
      * A main container with two distinct sub-sections for "Pantry" and "Commissary."
      * Each section contains a file input and a drop zone area.
      * Includes visual feedback for upload states (e.g., "waiting," "uploading," "success," "error").
  * **Functionality (`script.js`):**
      * Handles file selection, drag-and-drop events.
      * Provides client-side validation for file types (e.g., `.xlsx`, `.csv`).
      * Sends the files to the backend `/upload` endpoint.

### **`RecipeQuery` Component**

  * **Vision:** A simple form that appears after files are uploaded, allowing the user to specify their desired meal.
  * **Structure (`index.html`):**
      * [cite\_start]A dropdown menu for `Meal Type` (e.g., Breakfast, Main Dish, Side Dish, Snack)[cite: 10, 11].
      * An optional text input for `Key Ingredient` (e.g., "chicken," "broccoli").
      * A "Find Recipes" submission button.
  * **Functionality (`script.js`):**
      * Collects user selections.
      * On submit, sends a request to the backend `/recipes` endpoint.
      * Manages a "loading" state while waiting for the backend to respond.

### **`RecipeCard` Component**

  * **Vision:** A visually appealing card to display each recipe suggestion in a grid or list.
  * **Structure (`index.html`):**
      * Contains an `<img>` tag for the recipe image.
      * Displays the recipe title (`<h2>`).
      * Shows a summary of ingredient availability (e.g., "Pantry: 5, Commissary: 2, Supermarket: 3").
  * **Functionality (`script.js`):**
      * Acts as a link or button that, when clicked, transitions the user to the `RecipeDetail` view for that recipe.

### **`RecipeDetail` Component**

  * **Vision:** A comprehensive view of a single selected recipe.
  * **Structure (`index.html`):**
      * Recipe title and image.
      * [cite\_start]An organized ingredient list presented in a table with columns: `Ingredient`, `Quantity`, `Source (Pantry/Commissary/Supermarket)`[cite: 7, 48].
      * [cite\_start]A numbered list of cooking instructions[cite: 21, 22, 23, 24, 25].
      * [cite\_start]A link to the original recipe source[cite: 49].
  * **Functionality (`script.js`):**
      * Dynamically renders the ingredient table and instructions based on data received from the backend.

## 5\. Technical Specification

  * **Directory Structure:** The project will follow a clean, organized structure. Frontend components will be modular, and the backend will be a self-contained application.

    ```
    /recipe-agent/
    ├── /frontend/
    │   ├── /components/
    │   │   ├── /FileUploader/
    │   │   ├── /RecipeQuery/
    │   │   └── ...
    │   ├── index.html      # Main app shell
    │   ├── styles.css      # Global styles
    │   └── app.js          # Main frontend logic
    ├── /backend/
    [cite_start]│   ├── app.py          # Flask application [cite: 7]
    [cite_start]│   ├── requirements.txt # Python dependencies [cite: 7]
    └── ...
    ```

  * **Backend API Endpoints:**

      * `POST /upload`: Accepts `multipart/form-data` with two files. It parses them with pandas, stores the ingredient lists in a server-side session or temporary cache, and returns a success status.
      * `GET /recipes`: Accepts query parameters like `dish_type` and `ingredient`. [cite\_start]It executes the core logic of fetching from Spoonacular, matching against the stored lists, and returning a prioritized JSON array of recipes[cite: 6].

  * [cite\_start]**Ingredient Matching Logic:** The backend will use the `rapidfuzz` library to perform partial ratio string matching, which is robust against minor differences in ingredient names[cite: 3].

## 6\. MVP & Future Roadmap

### **Minimum Viable Product (MVP):**

The initial release will be a functional **tool** that successfully implements the complete user flow described in Section 3. It will correctly process uploaded files, fetch and filter recipes, and display the results and details as specified.

### **Future Enhancements (Roadmap):**

Once the MVP is stable, we can iterate and evolve the tool into a true **agent**:

  * [cite\_start]**Conversational UI:** Transition the `RecipeQuery` form into a chatbot interface that can parse natural language requests (e.g., "What's a good Mediterranean breakfast?")[cite: 12, 13].
  * [cite\_start]**Ingredient Substitution:** If a recipe requires a "Supermarket" item, the agent could suggest a substitute that exists in the user's Pantry or Commissary[cite: 32, 52].
  * **Saved Profiles:** Allow users to save their ingredient lists so they don't have to upload the files on every visit.
  * [cite\_start]**Advanced Filtering:** Introduce more complex search filters, such as cuisine, flavor profiles, and specific dietary restrictions beyond Whole30[cite: 5].
  * [cite\_start]**Containerization:** Wrap the backend in a Docker container for easy and consistent deployment[cite: 5].