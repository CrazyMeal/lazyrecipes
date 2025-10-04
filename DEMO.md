# LazyRecipes Demo

Ready-to-run demo using existing promotion data from the `backend/results/` folder.

## Quick Start

### 1. Import Demo Data
```bash
python backend/import_demo_data.py
```
This imports all promotions from `backend/results/promotions.json` into the TinyDB database.

### 2. Start Backend Server
```bash
# Option A: Using the startup script
./start_demo.sh

# Option B: Manual start
cd backend
python app.py
```

The server will start at `http://localhost:5000`

## Demo Data

**Current Dataset** (from `backend/results/`):
- **7 stores**: Costco, IGA, Maxi, Metro, Provigo, Super C, Walmart
- **200 promotions** total across all stores
- **14 pages** analyzed (2 pages per store)

## Available API Endpoints

### Health Check
```bash
curl http://localhost:5000/api/health
```

### Get All Promotions
```bash
curl http://localhost:5000/api/promotions
```

### Generate Recipes
```bash
curl -X POST http://localhost:5000/api/recipes/generate \
  -H "Content-Type: application/json" \
  -d '{"num_recipes": 5}'
```

### Generate Recipes with Preferences
```bash
curl -X POST http://localhost:5000/api/recipes/generate \
  -H "Content-Type: application/json" \
  -d '{
    "num_recipes": 5,
    "preferences": {
      "dietary": "vegetarian",
      "servings": 4
    }
  }'
```

### Create Shopping List
```bash
# First generate recipes to get recipe IDs, then:
curl -X POST http://localhost:5000/api/shopping-list \
  -H "Content-Type: application/json" \
  -d '{"recipe_ids": ["recipe_1", "recipe_3"]}'
```

## Sample Promotions (From Data)

**Costco**:
- Chicken breast (4 kg) - $30.99 - Save $8
- Mozzarella cheese (2 kg) - $21.99 - Save $6
- Mascarpone (2 kg) - $23.99 - Save $6

**Metro**:
- Extra lean ground beef - $5.49/lb - Save $2.50
- Chicken drumsticks - $1.69/lb
- Red peppers - $0.99/each

**Provigo**:
- Strawberries (1 lb) - $2.99 - Save $2
- Raspberries (170g) - $2.99 - Save $2
- Green beans (2 lb) - $2.99

## Demo Workflow

1. **Start Server**: `./start_demo.sh`
2. **View Promotions**: GET `/api/promotions` (200 items loaded)
3. **Generate Recipes**: POST `/api/recipes/generate` with `{"num_recipes": 5}`
4. **Create Shopping List**: POST `/api/shopping-list` with selected recipe IDs
5. **See Savings**: Response shows total cost and estimated savings

## Notes

- No scraping required - uses pre-loaded data
- Database located at: `backend/data/promotions.json`
- To refresh data: Run `python backend/scripts/flyer_processor.py --pages 2`
- Frontend integration: Connect React app to `http://localhost:5000/api/*`
