"""
LazyRecipes Flask API
Provides endpoints for grocery promotion scraping, recipe generation, and shopping list creation.
"""

import os
import json
import glob
from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS
from apscheduler.schedulers.background import BackgroundScheduler
from dotenv import load_dotenv
from openai import OpenAI
from tinydb import TinyDB, Query

# Import our scraping and analysis modules
from scripts.discover_flyers import discover_latest_flyers, save_flyer_urls
from scripts.extract_flyer_urls import extract_all_flyers, save_image_urls
from scripts.download_all_flyers import download_all_flyers
from scripts.analyze_all_stores_partial import analyze_all_stores_partial

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Configuration
PROMOTIONS_DIR = "data/promotion_results"
FLYER_IMAGES_DIR = "data/flyer_images"
DB_PATH = "data/promotions.json"
NUM_PAGES_PER_STORE = 2
EXCLUDE_STORES = ['super-c-direct']  # Old test folder

# Initialize OpenAI client
openai_client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# Initialize TinyDB
db = TinyDB(DB_PATH)
promotions_table = db.table('promotions')
scrapes_table = db.table('scrapes')

# In-memory storage for generated recipes
recipes_cache = {}
recipe_counter = 0


def run_weekly_scrape_and_analysis():
    """
    Background task that runs weekly to scrape flyers and analyze promotions.
    """
    print("\n" + "="*60)
    print(f"[{datetime.now()}] Running weekly scrape and analysis...")
    print("="*60)

    try:
        # Step 1: Discover latest flyers
        print("\n[1/4] Discovering latest flyers...")
        flyers = discover_latest_flyers()
        flyers_file = save_flyer_urls(flyers)
        print(f"✓ Found {len(flyers)} flyers")

        # Step 2: Extract image URLs
        print("\n[2/4] Extracting image URLs...")
        image_data = extract_all_flyers(flyers_file)
        urls_file = save_image_urls(image_data)
        total_images = sum(len(data['image_urls']) for data in image_data.values())
        print(f"✓ Extracted {total_images} image URLs")

        # Step 3: Download images
        print("\n[3/4] Downloading flyer images...")
        stats = download_all_flyers(urls_file, FLYER_IMAGES_DIR)
        print(f"✓ Downloaded {stats['images_succeeded']}/{stats['total_images']} images")

        # Step 4: Analyze with OpenAI (first 2 pages per store)
        print("\n[4/4] Analyzing flyers with OpenAI...")
        results = analyze_all_stores_partial(
            num_pages=NUM_PAGES_PER_STORE,
            exclude_stores=EXCLUDE_STORES,
            flyer_images_dir=FLYER_IMAGES_DIR,
            output_dir=PROMOTIONS_DIR
        )
        total_promotions = sum(r['promotion_count'] for r in results.values())
        print(f"✓ Extracted {total_promotions} promotions from {len(results)} stores")

        # Step 5: Save to database
        print("\n[5/5] Saving promotions to database...")
        promotions = load_all_promotions_from_files()
        save_promotions_to_db(promotions)
        print(f"✓ Saved {len(promotions)} promotions to database")

        print("\n" + "="*60)
        print(f"[{datetime.now()}] Weekly task completed successfully!")
        print("="*60 + "\n")

    except Exception as e:
        print(f"\n✗ Error during weekly task: {e}")
        print("="*60 + "\n")


def load_all_promotions_from_files():
    """Load all promotions from the promotion_results directory."""
    promotions = []

    if not os.path.exists(PROMOTIONS_DIR):
        return promotions

    # Load all store promotion files
    for filepath in glob.glob(os.path.join(PROMOTIONS_DIR, "*_promotions.json")):
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
                promotions.extend(data.get('promotions', []))
        except Exception as e:
            print(f"Error loading {filepath}: {e}")

    return promotions


def save_promotions_to_db(promotions):
    """
    Save promotions to TinyDB with a timestamp.
    Each scrape is stored as a separate record with all promotions.
    """
    scrape_id = datetime.now().isoformat()

    # Clear old promotions
    promotions_table.truncate()

    # Insert new promotions with scrape_id
    for promo in promotions:
        promo_with_id = promo.copy()
        promo_with_id['scrape_id'] = scrape_id
        promotions_table.insert(promo_with_id)

    # Record the scrape metadata
    scrapes_table.insert({
        'scrape_id': scrape_id,
        'timestamp': scrape_id,
        'promotion_count': len(promotions)
    })


def load_all_promotions():
    """
    Load the latest promotions from TinyDB.
    Returns promotions from the most recent scrape only.
    """
    # Get the latest scrape
    all_scrapes = scrapes_table.all()

    if not all_scrapes:
        # Fallback to file-based loading if no database records
        return load_all_promotions_from_files()

    # Find the most recent scrape
    latest_scrape = max(all_scrapes, key=lambda x: x['timestamp'])
    scrape_id = latest_scrape['scrape_id']

    # Get all promotions from that scrape
    Promo = Query()
    promotions = promotions_table.search(Promo.scrape_id == scrape_id)

    # Remove scrape_id from the output
    return [
        {k: v for k, v in promo.items() if k not in ['scrape_id', 'doc_id']}
        for promo in promotions
    ]


def generate_recipes_with_openai(promotions, num_recipes=5, preferences=None):
    """Generate recipes using OpenAI based on current promotions."""
    global recipe_counter

    if preferences is None:
        preferences = {}

    # Extract just item names and filter out obvious non-food items
    non_food_keywords = [
        'detergent', 'bleach', 'cleaner', 'soap', 'shampoo', 'conditioner',
        'toothpaste', 'deodorant', 'tissue', 'paper towel', 'toilet paper',
        'diaper', 'wipes', 'laundry', 'dish soap', 'fabric softener'
    ]

    promo_items = [
        p['item'] for p in promotions
        if not any(keyword in p['item'].lower() for keyword in non_food_keywords)
    ]

    # Format promotions as a simple list for the prompt
    promotion_list = ", ".join(promo_items)

    # Build prompt
    dietary = preferences.get('dietary', '')
    servings = preferences.get('servings', 4)

    dietary_text = f"\n- All recipes must be {dietary}" if dietary else ""

    prompt = f"""You are a creative meal planning assistant. Generate {num_recipes} VARIED and DIFFERENT recipes that primarily use items from the following grocery promotions:

**Promoted Food Items (all suitable for cooking):**
{promotion_list}

**Instructions:**
1. Create {num_recipes} diverse recipes with different cuisines, cooking methods, and main ingredients
2. Each recipe should use MULTIPLE items from the promotion list above (aim for 3-5+ promoted items per recipe)
3. You may include common pantry staples (salt, pepper, oil, flour, spices, etc.) that aren't on the promotion list
4. Focus on creating complete, balanced, delicious meals that maximize savings from the promoted items
5. Each recipe should serve {servings} people{dietary_text}
6. DO NOT make up or invent promoted items - ONLY use items from the list above

**Quality Standards:**
- Make recipes practical and achievable for home cooks
- Provide clear, step-by-step instructions (4-6 steps)
- Include realistic cooking times
- Ensure variety across all {num_recipes} recipes (different proteins, vegetables, cooking styles)

**Output Format (ONLY valid JSON):**
[
  {{
    "name": "Recipe Name",
    "description": "Brief appetizing description of the dish",
    "ingredients": [
      {{"item": "Chicken breast", "amount": "1.5 lb", "on_sale": true}},
      {{"item": "Garlic", "amount": "3 cloves", "on_sale": true}},
      {{"item": "Olive oil", "amount": "2 tbsp", "on_sale": false}}
    ],
    "instructions": ["Step 1", "Step 2", "Step 3", "Step 4"],
    "cooking_time": "30 mins",
    "servings": {servings}
  }}
]

**Critical Rules:**
- Mark "on_sale": true ONLY for ingredients that EXACTLY match items in the promoted list above
- Mark "on_sale": false for pantry staples or items NOT in the promoted list
- Do NOT include any non-food items in recipes
"""

    try:
        response = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a creative meal planning assistant that creates diverse, delicious recipes based on grocery promotions to help users save money while eating well."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=4000,
            temperature=0.8
        )

        content = response.choices[0].message.content.strip()

        # Extract JSON from markdown code blocks if present
        if content.startswith("```json"):
            content = content.split("```json")[1].split("```")[0].strip()
        elif content.startswith("```"):
            content = content.split("```")[1].split("```")[0].strip()

        try:
            recipes = json.loads(content)
        except json.JSONDecodeError as e:
            print(f"JSON parsing error: {e}")
            print(f"Content received: {content[:500]}...")
            raise

        # Add IDs to recipes and cache them
        for recipe in recipes:
            recipe_counter += 1
            recipe_id = f"recipe_{recipe_counter}"
            recipe['id'] = recipe_id
            recipes_cache[recipe_id] = recipe

        return recipes

    except Exception as e:
        print(f"Error generating recipes: {e}")
        raise


# ============================================================================
# API ENDPOINTS
# ============================================================================

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    })


@app.route('/api/promotions', methods=['GET'])
def get_promotions():
    """Get all current promotions (from latest scrape only)."""
    try:
        promotions = load_all_promotions()

        # Get the latest scrape timestamp
        all_scrapes = scrapes_table.all()
        scrape_timestamp = None
        if all_scrapes:
            latest_scrape = max(all_scrapes, key=lambda x: x['timestamp'])
            scrape_timestamp = latest_scrape['timestamp']

        return jsonify({
            "promotions": promotions,
            "count": len(promotions),
            "scrape_timestamp": scrape_timestamp,
            "last_updated": datetime.now().isoformat()
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/scrape', methods=['POST'])
def trigger_scrape():
    """
    Manually trigger the scraping and analysis pipeline.
    This runs the same process as the weekly background task.
    """
    try:
        # Run scraping and analysis in foreground
        run_weekly_scrape_and_analysis()

        # Load and return the promotions
        promotions = load_all_promotions()

        return jsonify({
            "status": "success",
            "message": "Scraping and analysis completed",
            "promotions": promotions,
            "count": len(promotions)
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


@app.route('/api/recipes/generate', methods=['POST'])
def generate_recipes():
    """
    Generate recipes based on current promotions.

    Request body:
    {
      "num_recipes": 5,
      "preferences": {
        "dietary": "vegetarian",  // optional
        "servings": 4             // optional
      }
    }
    """
    try:
        data = request.get_json()

        # Get parameters
        num_recipes = data.get('num_recipes', 5)
        preferences = data.get('preferences', {})

        # Load current promotions
        promotions = load_all_promotions()

        if not promotions:
            return jsonify({
                "error": "No promotions available. Run /api/scrape first."
            }), 400

        # Generate recipes using OpenAI
        recipes = generate_recipes_with_openai(promotions, num_recipes, preferences)

        return jsonify({
            "recipes": recipes,
            "count": len(recipes)
        })

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500


@app.route('/api/shopping-list', methods=['POST'])
def create_shopping_list():
    """
    Create a shopping list from selected recipes.

    Request body:
    {
      "recipe_ids": ["recipe_1", "recipe_3"]
    }
    """
    try:
        data = request.get_json()
        recipe_ids = data.get('recipe_ids', [])

        if not recipe_ids:
            return jsonify({
                "error": "No recipe IDs provided"
            }), 400

        # Get recipes from cache
        selected_recipes = []
        for recipe_id in recipe_ids:
            if recipe_id in recipes_cache:
                selected_recipes.append(recipes_cache[recipe_id])
            else:
                return jsonify({
                    "error": f"Recipe {recipe_id} not found. Generate recipes first."
                }), 404

        # Aggregate ingredients
        ingredient_map = {}

        for recipe in selected_recipes:
            for ingredient in recipe['ingredients']:
                item_name = ingredient['item']

                if item_name in ingredient_map:
                    # For simplicity, just append amounts (proper aggregation would parse units)
                    ingredient_map[item_name]['amount'] += f" + {ingredient['amount']}"
                else:
                    ingredient_map[item_name] = {
                        'item': item_name,
                        'amount': ingredient['amount'],
                        'on_sale': ingredient.get('on_sale', False)
                    }

        shopping_list = list(ingredient_map.values())

        # Load promotions to add price info
        promotions = load_all_promotions()
        promotion_map = {p['item'].lower(): p for p in promotions}

        total_cost = 0.0
        estimated_savings = 0.0

        for item in shopping_list:
            item_lower = item['item'].lower()

            # Try to find matching promotion
            matching_promo = None
            for promo_key, promo in promotion_map.items():
                if promo_key in item_lower or item_lower in promo_key:
                    matching_promo = promo
                    break

            if matching_promo:
                item['price'] = matching_promo['price']
                item['on_sale'] = True
                total_cost += matching_promo['price']
                # Estimate 30% savings on sale items
                estimated_savings += matching_promo['price'] * 0.3
            else:
                # Estimate price for non-sale items
                item['price'] = 5.0  # Placeholder
                total_cost += 5.0

        return jsonify({
            "shopping_list": shopping_list,
            "total_cost": round(total_cost, 2),
            "estimated_savings": round(estimated_savings, 2)
        })

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500


# ============================================================================
# SCHEDULER SETUP
# ============================================================================

def initialize_scheduler():
    """Initialize and start the background scheduler for weekly tasks."""
    scheduler = BackgroundScheduler()

    # Schedule weekly task (every Monday at 1 AM)
    scheduler.add_job(
        func=run_weekly_scrape_and_analysis,
        trigger="cron",
        day_of_week="mon",
        hour=1,
        minute=0,
        id="weekly_scrape",
        name="Weekly flyer scrape and analysis",
        replace_existing=True
    )

    scheduler.start()
    print("✓ Background scheduler started (weekly task: Mondays at 1 AM)")


# ============================================================================
# APPLICATION STARTUP
# ============================================================================

if __name__ == '__main__':
    print("\n" + "="*60)
    print("LazyRecipes API Server")
    print("="*60)

    # Create directories if they don't exist
    os.makedirs(PROMOTIONS_DIR, exist_ok=True)
    os.makedirs(FLYER_IMAGES_DIR, exist_ok=True)

    # Initialize background scheduler
    initialize_scheduler()

    print(f"\nAPI Endpoints:")
    print(f"  GET  /api/health              - Health check")
    print(f"  GET  /api/promotions          - Get current promotions")
    print(f"  POST /api/scrape              - Trigger scraping & analysis")
    print(f"  POST /api/recipes/generate    - Generate recipes")
    print(f"  POST /api/shopping-list       - Create shopping list")
    print("\n" + "="*60 + "\n")

    # Run Flask app
    app.run(debug=True, host='0.0.0.0', port=5000, use_reloader=False)
