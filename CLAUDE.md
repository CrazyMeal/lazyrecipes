# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**LazyRecipes** is a hackathon PoC application that helps users plan weekly groceries by generating recipes based on current store promotions and rebates.

### Core Concept
1. **Scrape** grocery store flyers for promotions/rebates
2. **Generate** recipes using OpenAI based on available deals
3. **Display** recipes with highlighted sale items
4. **Create** shopping lists from selected recipes

### Target Use Case
Users check weekly grocery flyers manually (e.g., ReFlagDeals) to find deals. LazyRecipes automates this by scraping promotions, then suggesting recipes that maximize savings on ingredients currently on sale.

## Tech Stack

### Backend
- **Framework**: Flask (Python)
- **Scraping**: Playwright (handles dynamic JS content)
- **AI**: OpenAI API (GPT-3.5-turbo for recipe generation)
- **Dependencies**: flask-cors, python-dotenv

### Frontend
- **Framework**: React
- **Styling**: Tailwind CSS
- **Routing**: React Router (if needed)

### Architecture Flow
```
User Request → Flask API → Playwright Scraper → OpenAI API → React Display
```

## Commit Message Convention

This project follows the Conventional Commits specification. All commit messages must adhere to the following format:

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types
- **feat**: A new feature
- **fix**: A bug fix
- **docs**: Documentation only changes
- **style**: Changes that do not affect the meaning of the code (white-space, formatting, etc)
- **refactor**: A code change that neither fixes a bug nor adds a feature
- **perf**: A code change that improves performance
- **test**: Adding missing tests or correcting existing tests
- **build**: Changes that affect the build system or external dependencies
- **ci**: Changes to CI configuration files and scripts
- **chore**: Other changes that don't modify src or test files

### Examples
```
feat(auth): add user login functionality
fix(api): resolve null pointer exception in user service
docs(readme): update installation instructions
chore: initialize project with CLAUDE.md
```

### Rules
- Use lowercase for type and scope
- Keep subject line under 50 characters
- Use imperative mood in the subject line ("add" not "added")
- Separate subject from body with a blank line
- Wrap body at 72 characters
- Use body to explain what and why, not how

## Project Structure

```
lazyrecipes/
├── backend/
│   ├── app.py                 # Flask API with endpoints
│   ├── scraper.py             # Playwright web scraper
│   ├── recipe_generator.py    # OpenAI recipe generation
│   ├── requirements.txt       # Python dependencies
│   └── .env                   # API keys (OPENAI_API_KEY)
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── RecipeCard.jsx        # Individual recipe display
│   │   │   ├── PromotionsList.jsx    # Show scraped promotions
│   │   │   └── ShoppingList.jsx      # Combined shopping list
│   │   ├── pages/
│   │   │   ├── Home.jsx              # Landing page
│   │   │   └── Recipes.jsx           # Recipe display page
│   │   ├── App.jsx
│   │   └── index.css
│   ├── package.json
│   └── tailwind.config.js
└── README.md
```

## API Endpoints

### Backend (Flask)

#### `POST /api/scrape`
Triggers Playwright scraper to fetch current store promotions.

**Response:**
```json
{
  "promotions": [
    {
      "item": "Chicken breast",
      "price": 4.99,
      "unit": "lb",
      "store": "Metro",
      "discount": "30% off"
    }
  ]
}
```

#### `POST /api/recipes/generate`
Takes promotion data and generates recipes via OpenAI.

**Request:**
```json
{
  "promotions": [...],
  "num_recipes": 5,
  "preferences": {
    "dietary": "vegetarian",  // optional
    "servings": 4             // optional
  }
}
```

**Response:**
```json
{
  "recipes": [
    {
      "id": "recipe_1",
      "name": "Honey Garlic Chicken",
      "description": "Quick weeknight dinner",
      "ingredients": [
        {"item": "Chicken breast", "amount": "1.5 lb", "on_sale": true},
        {"item": "Honey", "amount": "3 tbsp", "on_sale": false}
      ],
      "instructions": ["Step 1...", "Step 2..."],
      "cooking_time": "30 mins",
      "servings": 4
    }
  ]
}
```

#### `POST /api/shopping-list`
Combines selected recipes into shopping list.

**Request:**
```json
{
  "recipe_ids": ["recipe_1", "recipe_3"]
}
```

**Response:**
```json
{
  "shopping_list": [
    {"item": "Chicken breast", "amount": "3 lb", "on_sale": true, "price": 14.97},
    {"item": "Honey", "amount": "6 tbsp", "on_sale": false, "price": 4.99}
  ],
  "total_cost": 19.96,
  "estimated_savings": 6.50
}
```

## OpenAI Integration

### Prompt Strategy

```python
prompt = f"""
You are a meal planning assistant. Generate {num_recipes} recipes using primarily
the following promoted grocery items:

Promotions:
{format_promotions(promotions)}

Requirements:
- Use as many promoted items as possible
- Create complete, balanced meals
- Include cooking time and servings
- Return ONLY valid JSON

Output format:
[
  {{
    "name": "Recipe Name",
    "description": "Brief description",
    "ingredients": [
      {{"item": "Chicken breast", "amount": "1 lb", "on_sale": true}},
      {{"item": "Salt", "amount": "1 tsp", "on_sale": false}}
    ],
    "instructions": ["Step 1", "Step 2"],
    "cooking_time": "30 mins",
    "servings": 4
  }}
]
"""
```

### Model Configuration
- **Model**: `gpt-3.5-turbo` (fast + cost-effective for hackathon)
- **Temperature**: `0.7` (balanced creativity)
- **Max Tokens**: `2000` (sufficient for 3-5 recipes)

## User Flow

```
1. Home Page
   ↓
2. Click "Find This Week's Best Recipes"
   ↓
3. Backend scrapes flyer (loading state)
   ↓
4. Display promotions + generate recipes via OpenAI
   ↓
5. Show recipe cards with ingredients highlighted
   ↓
6. User selects recipes → "Create Shopping List"
   ↓
7. Display combined shopping list with:
   - Grouped ingredients
   - Sale items highlighted
   - Total cost + savings
```

## Scraping Strategy

### Target Options
1. **Flipp.com** - Aggregator (multiple stores, complex JS)
2. **Metro.ca** - Single store (simpler structure)
3. **Walmart.ca** - Large inventory (structured flyers)
4. **Loblaws/PC** - Popular chain (good deals)

### Playwright Approach
```python
from playwright.sync_api import sync_playwright

def scrape_flyer(store_url):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(store_url)

        # Wait for dynamic content
        page.wait_for_selector('.product-item')

        # Extract promotions
        products = page.query_selector_all('.product-item')
        promotions = []

        for product in products:
            promotions.append({
                'item': product.query_selector('.name').inner_text(),
                'price': product.query_selector('.price').inner_text(),
                'discount': product.query_selector('.discount').inner_text()
            })

        browser.close()
        return promotions
```

## Hackathon MVP Checklist

### Must Have (Core Demo)
- ✅ Scrape ONE store flyer (10-20 items minimum)
- ✅ Generate 3-5 recipes via OpenAI
- ✅ Display recipes with sale items highlighted
- ✅ Create shopping list from selected recipes

### Nice to Have (If Time Permits)
- Dietary filters (vegetarian, gluten-free)
- Show estimated savings calculation
- Recipe images (Unsplash API or placeholders)
- Loading states and error handling

### Skip for Hackathon
- User accounts/authentication
- Database persistence
- Multiple store comparison
- Mobile-responsive optimization
- Recipe rating/favorites

## Risk Mitigation

### Scraper Reliability
- **Risk**: Website structure changes or blocks during demo
- **Mitigation**: Cache scraped data, have mock fallback JSON

### OpenAI API
- **Risk**: API timeout or rate limiting
- **Mitigation**: Pre-generate 3-5 backup recipes, show cached results

### Demo Preparation
- Run full scrape → generate → display flow before demo
- Save successful results as fallback
- Test with cached data for reliable demo

## Environment Variables

Create `.env` file in `backend/`:
```env
OPENAI_API_KEY=your_openai_key_here
FLASK_ENV=development
```

## Development Commands

### Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
pip install -r requirements.txt
playwright install chromium
python app.py
```

### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

## Key Technical Decisions

### Why Playwright over BeautifulSoup?
- Handles JavaScript-rendered content (most modern flyer sites)
- Browser automation for dynamic pages
- Screenshot capability for debugging

### Why GPT-3.5-turbo over GPT-4?
- 10x faster response time (~3s vs ~30s)
- 10x cheaper per request
- Sufficient quality for recipe generation
- Better for hackathon demo (no lag)

### Why Flask over FastAPI?
- Team member preference and familiarity
- Simpler for small hackathon scope
- Adequate performance for demo

## Notes for Future Development

### Post-Hackathon Enhancements
- Add user authentication and profiles
- Implement database (PostgreSQL) for persistence
- Multi-store comparison and optimization
- Mobile-first responsive design
- Recipe rating and community features
- Notification system for favorite item deals
