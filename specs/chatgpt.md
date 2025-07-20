# Pantry & Commissary Recipe Agent UI (Draft 2)

## Purpose

A web-based agent/assistant for meal planning. User uploads two Excel workbooks:

* `Pantry.xlsx`: List of free items available from a pantry
* `Commissary.xlsx`: List of discounted items available from a commissary

The system recommends healthy recipes, strictly prioritizing ingredients in the following order:

1. Pantry (free)
2. Commissary (discounted)
3. Supermarket (full price)

## High-Level User Flow

1. **User uploads Pantry.xlsx and Commissary.xlsx**
2. **User requests a recipe suggestion** (optionally specifying type, cuisine, dietary preference, or flavor profile)
3. **Agent suggests 3 recipes**

   * All recipes are filtered to maximize Pantry/Commissary ingredients. Start with a 90% threshold; if no results, lower threshold as needed.
   * Each ingredient is tagged: \[Pantry] \[Commissary] \[Not Available]
   * Prioritize recipes maximizing \[Pantry], then \[Commissary], minimize \[Not Available].
4. **User selects a recipe**
5. **Agent displays:**

   * Full recipe (title, picture, 1-sentence description, detailed instructions)
   * Ingredient list, source-tagged
   * Link to recipe source
   * Suggested substitutions for any \[Not Available] ingredients (prioritize Pantry/Commissary, but allow common culinary substitutions)

## Core Architecture

* **Frontend:** Minimal web UI (Gradio prototype; migration to other stacks is possible)
* **Backend:**

  * Flask or FastAPI server
  * Handles Excel file ingestion, recipe selection logic, and filtering
  * Integrates with Spoonacular API (Yummly, Edamam: future)
  * Fuzzy-matching of recipe ingredients to inventory lists using rapidfuzz
  * Exposes `/get_recipes` endpoint for UI
* **LLM Integration:**

  * Interprets free-text user requests (intent parsing)
  * (Optional/future) LLM-based substitution reasoning

## Key Functions

* `fuzzy_match(ingredient, threshold)` — Fuzzy-match recipe ingredient to Pantry/Commissary
* `get_matching_recipes(query, threshold)` — Search/filter for max Pantry/Commissary ingredient use; lower threshold if zero results
* `ingredient_source_table(recipe)` — Show Pantry/Commissary/Not Available status for each item

## UI/UX States

1. **On Load**

   * Upload fields: Pantry.xlsx, Commissary.xlsx
   * Status: "Awaiting inventory uploads."
2. **Inventory Uploaded**

   * Prompt: "What kind of meal are you looking for?"
3. **User Query (recipe type, flavor, etc.)**

   * Suggest 3 best-fit recipes (title, image, brief description)
4. **User Selects Recipe**

   * Show full recipe
   * Table: Ingredient | Source
   * Suggest substitutions for \[Not Available]

## Example API

```http
GET /get_recipes?dish_type=side%20dish&cuisine=thai
{
  "recipes": [
    {
      "title": "Whole30 Thai Larb (Spicy Pork Salad)",
      "url": "https://thedefineddish.com/whole30-thai-larb-spicy-pork-salad/",
      "image_url": "https://...jpg",
      "description": "A spicy, fresh Thai salad with pork, herbs, and lime.",
      "ingredients": [
        {"name": "ground pork", "source": "Commissary"},
        {"name": "shallot", "source": "Pantry"},
        {"name": "thai chiles", "source": "Not Available"},
        ...
      ]
    },
    ...
  ]
}
```

## Design Notes / Principles

* **All ingredient availability is programmatically verified against Excel files, not assumed.**
* **If ingredient is missing, agent must propose substitutions—prefer Pantry/Commissary, allow common culinary subs if not present.**
* **Users should never have to check or verify ingredient matches themselves.**
* **Recipe suggestion process must degrade gracefully: if no matches at high threshold, reduce and try again.**
* **Stateful UI: inventory upload > recipe query > user selection > result.**

## Extensibility / Future Work

* Ingredient synonym dictionary ("scallion" vs. "green onion"), manual override table
* Support additional recipe APIs (Yummly, Edamam, etc.)
* Google Sheets integration; persistent user inventories
* Meal planning (multi-day/week batch)
* Export shopping list for Not Available items
* Dietary filters (gluten-free, vegan, etc.)
* LLM-based substitution reasoning
* Batch recipe suggestion for meal prep
* Dockerization, NAS/local deployment scripts
* User authentication/persistent accounts
* Error reporting, logging, and user-friendly Excel ingest
* React/TypeScript UI

## Known Issues

* Fuzzy-matching may fail for uncommon ingredient variants or nonstandard phrasing
* Recipes/APIs may include ingredients not standard (e.g., "everything bagel seasoning")
* Ingredient data in user files may be inconsistent; robust cleaning required
* Edge-case: no recipes meet even minimal match—return best-effort or prompt user to relax requirements

## File Index

* `app.py` — Backend logic (Flask API)
* `gradio_ui.py` — Gradio interface
* `requirements.txt` — Python dependencies
* `pantry.xlsx` — Pantry inventory (user upload)
* `commissary.xlsx` — Commissary inventory (user upload)
* (future) `substitutions.json` — Substitution mapping

## Credits / Sources

* Based on "invent\_new\_ui\_v4.md"
* Whole30/meal-planning agent experiment
* [Spoonacular API](https://spoonacular.com/food-api)
* [rapidfuzz](https://maxbachmann.github.io/RapidFuzz/)
