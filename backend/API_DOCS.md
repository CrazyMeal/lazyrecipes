# LazyRecipes API Documentation

Base URL: `http://localhost:5000`

## Endpoints

### 1. Health Check
**GET** `/api/health`

Check if the API is running.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2025-10-04T14:26:55.711419"
}
```

---

### 2. Get Promotions
**GET** `/api/promotions`

Get all current grocery promotions from analyzed flyers.

**Response:**
```json
{
  "count": 156,
  "last_updated": "2025-10-04T14:26:55.865031",
  "promotions": [
    {
      "item": "Broccoli",
      "price": 0.55,
      "unit": "each",
      "discount": "Économisez 73%",
      "store": "maxi"
    }
    // ... more promotions
  ]
}
```

---

### 3. Trigger Scraping and Analysis
**POST** `/api/scrape`

Manually trigger the flyer scraping and analysis pipeline. This will:
1. Discover latest flyers from RedFlagDeals
2. Extract image URLs
3. Download flyer images
4. Analyze images with OpenAI (first 2 pages per store)

**Note:** This process takes 5-10 minutes depending on the number of stores.

**Response:**
```json
{
  "status": "success",
  "message": "Scraping and analysis completed",
  "count": 156,
  "promotions": [...]
}
```

---

### 4. Generate Recipes
**POST** `/api/recipes/generate`

Generate recipes based on current promotions using OpenAI.

**Request Body:**
```json
{
  "num_recipes": 5,
  "preferences": {
    "dietary": "vegetarian",  // optional
    "servings": 4             // optional (default: 4)
  }
}
```

**Response:**
```json
{
  "count": 3,
  "recipes": [
    {
      "id": "recipe_1",
      "name": "Garlic Mushroom Spaghetti",
      "description": "A delicious pasta dish with sautéed garlic mushrooms served over spaghettini.",
      "cooking_time": "25 mins",
      "servings": 4,
      "ingredients": [
        {
          "item": "White Mushrooms",
          "amount": "227 g",
          "on_sale": true
        },
        {
          "item": "Primo Spaghettini",
          "amount": "300 g",
          "on_sale": true
        }
        // ... more ingredients
      ],
      "instructions": [
        "Cook spaghettini according to package instructions.",
        "In a pan, heat olive oil and sauté minced garlic until fragrant.",
        // ... more steps
      ]
    }
    // ... more recipes
  ]
}
```

---

### 5. Create Shopping List
**POST** `/api/shopping-list`

Create a shopping list from selected recipes. Aggregates ingredients and calculates total cost and savings.

**Request Body:**
```json
{
  "recipe_ids": ["recipe_1", "recipe_3"]
}
```

**Response:**
```json
{
  "shopping_list": [
    {
      "item": "White Mushrooms",
      "amount": "227 g",
      "on_sale": true,
      "price": 0.55
    },
    {
      "item": "Olive Oil",
      "amount": "2 tbsp + 1 tbsp",
      "on_sale": false,
      "price": 5.0
    }
    // ... more items
  ],
  "total_cost": 29.41,
  "estimated_savings": 2.82
}
```

---

## Background Scheduler

The API includes a background scheduler that automatically runs the scraping and analysis pipeline:

- **Schedule:** Every Monday at 1:00 AM
- **Task:** Complete flyer scraping and OpenAI analysis
- **Processing:** First 2 pages per store (configurable)
- **Excluded stores:** `super-c-direct` (old test folder)

---

## Configuration

### Environment Variables

Create a `.env` file in the backend directory:

```env
OPENAI_API_KEY=your_openai_api_key_here
FLASK_ENV=development
```

### Directories

- `flyer_images/` - Downloaded flyer images organized by store
- `promotion_results/` - JSON files with analyzed promotions per store

---

## Example Usage

### 1. Get Current Promotions
```bash
curl http://localhost:5000/api/promotions
```

### 2. Generate 3 Recipes
```bash
curl -X POST http://localhost:5000/api/recipes/generate \
  -H "Content-Type: application/json" \
  -d '{
    "num_recipes": 3,
    "preferences": {
      "servings": 4
    }
  }'
```

### 3. Create Shopping List
```bash
curl -X POST http://localhost:5000/api/shopping-list \
  -H "Content-Type: application/json" \
  -d '{
    "recipe_ids": ["recipe_1", "recipe_2"]
  }'
```

### 4. Trigger Manual Scraping (Long-running)
```bash
curl -X POST http://localhost:5000/api/scrape
```

---

## Notes

- **Recipe Generation:** Uses GPT-3.5-turbo for fast, cost-effective recipe generation
- **Image Analysis:** Uses GPT-4o Vision API with high detail mode
- **Processing Time:** Recipe generation takes ~5-10 seconds, scraping takes ~5-10 minutes
- **Caching:** Generated recipes are cached in memory for shopping list creation
- **Demo Mode:** Only processes first 2 pages per store to manage API costs
