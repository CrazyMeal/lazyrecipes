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

# Import our scraping and analysis modules
from discover_flyers import discover_latest_flyers, save_flyer_urls
from extract_flyer_urls import extract_all_flyers, save_image_urls
from download_all_flyers import download_all_flyers
from analyze_all_stores_partial import analyze_all_stores_partial

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Configuration
PROMOTIONS_DIR = "promotion_results"
FLYER_IMAGES_DIR = "flyer_images"
NUM_PAGES_PER_STORE = 2
EXCLUDE_STORES = ['super-c-direct']  # Old test folder

# Initialize OpenAI client
openai_client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

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

        print("\n" + "="*60)
        print(f"[{datetime.now()}] Weekly task completed successfully!")
        print("="*60 + "\n")

    except Exception as e:
        print(f"\n✗ Error during weekly task: {e}")
        print("="*60 + "\n")


def load_all_promotions():
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


def generate_recipes_with_openai(promotions, num_recipes=5, preferences=None):
    """Generate recipes using OpenAI based on current promotions."""
    global recipe_counter

    if preferences is None:
        preferences = {}

    # Format promotions for prompt
    promotion_list = "\n".join([
        f"- {p['item']}: ${p['price']}/{p['unit']} ({p['discount']}) at {p['store']}"
        for p in promotions[:30]  # Limit to first 30 to keep prompt manageable
    ])

    # Build prompt
    dietary = preferences.get('dietary', '')
    servings = preferences.get('servings', 4)

    dietary_text = f"Make the recipes {dietary}." if dietary else ""

    prompt = f"""You are a meal planning assistant. Generate {num_recipes} recipes using primarily the following promoted grocery items:

Current Promotions:
{promotion_list}

Requirements:
- Use as many promoted items as possible to maximize savings
- Create complete, balanced meals
- Each recipe should serve {servings} people
- Include cooking time
{dietary_text}
- Return ONLY valid JSON

Output format (array of recipe objects):
[
  {{
    "name": "Recipe Name",
    "description": "Brief description of the dish",
    "ingredients": [
      {{"item": "Chicken breast", "amount": "1.5 lb", "on_sale": true}},
      {{"item": "Salt", "amount": "1 tsp", "on_sale": false}}
    ],
    "instructions": ["Step 1", "Step 2", "Step 3"],
    "cooking_time": "30 mins",
    "servings": {servings}
  }}
]

Important: Mark "on_sale": true for ingredients that are in the promotions list, false otherwise.
"""

    try:
        response = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful meal planning assistant that creates recipes based on grocery promotions."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=3000,
            temperature=0.7
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
    """Get all current promotions."""
    try:
        promotions = load_all_promotions()

        return jsonify({
            "promotions": promotions,
            "count": len(promotions),
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
