"""
Analyze a sample of flyer images (first N pages per store).
Optimized for hackathon demo - processes fewer pages to save time and API costs.
"""

import os
import json
import base64
from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

MAX_PAGES_PER_STORE = 3  # Only process first 3 pages per store

def encode_image(image_path):
    """Encode image to base64 for OpenAI API."""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def analyze_flyer_image(client, image_path, store_name):
    """Analyze a single flyer image using OpenAI Vision API."""

    print(f"  Analyzing {os.path.basename(image_path)}...")

    try:
        # Encode image
        base64_image = encode_image(image_path)

        # Create prompt for promotion extraction
        prompt = """
Analyze this grocery store flyer image and extract ALL promotions, discounts, and sale items.

For each item, extract:
- item: Product name
- price: Regular or sale price (as a number)
- unit: Unit of measurement (e.g., "lb", "kg", "each", "pkg")
- discount: Discount description (e.g., "30% off", "Save $2", "2 for $5")

Return ONLY a valid JSON array with this exact structure:
[
  {
    "item": "Product name",
    "price": 4.99,
    "unit": "lb",
    "discount": "30% off"
  }
]

If no promotions are visible in this image, return an empty array: []

Important:
- Extract ALL visible items with prices
- Convert prices to numbers (remove $ and other symbols)
- Be specific with product names
- Include the discount/promotion text exactly as shown
"""

        # Call OpenAI Vision API
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}",
                                "detail": "high"
                            }
                        }
                    ]
                }
            ],
            max_tokens=2000,
            temperature=0.2
        )

        # Parse response
        content = response.choices[0].message.content.strip()

        # Extract JSON from response (handle markdown code blocks)
        if content.startswith("```json"):
            content = content.split("```json")[1].split("```")[0].strip()
        elif content.startswith("```"):
            content = content.split("```")[1].split("```")[0].strip()

        promotions = json.loads(content)

        # Add store name to each promotion
        for promo in promotions:
            promo['store'] = store_name

        print(f"    ✓ Found {len(promotions)} promotions")
        return promotions

    except json.JSONDecodeError as e:
        print(f"    ✗ JSON parsing error: {e}")
        print(f"    Raw response: {content[:200]}")
        return []

    except Exception as e:
        print(f"    ✗ Error: {e}")
        return []

def analyze_store_flyers_sample(client, store_key, flyer_images_dir="flyer_images", max_pages=MAX_PAGES_PER_STORE):
    """Analyze sample of flyer images for a single store (first N pages only)."""

    store_dir = os.path.join(flyer_images_dir, store_key)

    if not os.path.exists(store_dir):
        print(f"✗ Store directory not found: {store_dir}")
        return None

    # Get all image files
    all_image_files = sorted([
        f for f in os.listdir(store_dir)
        if f.endswith(('.jpg', '.jpeg', '.png'))
    ])

    if not all_image_files:
        print(f"✗ No images found in {store_dir}")
        return None

    # Limit to first N pages
    image_files = all_image_files[:max_pages]

    print(f"\n{'='*60}")
    print(f"Analyzing: {store_key.replace('-', ' ').title()}")
    print(f"Pages: {len(image_files)}/{len(all_image_files)} (sample)")
    print(f"{'='*60}")

    all_promotions = []

    for image_file in image_files:
        image_path = os.path.join(store_dir, image_file)
        promotions = analyze_flyer_image(
            client,
            image_path,
            store_key.replace('-', ' ')
        )
        all_promotions.extend(promotions)

    print(f"{'─'*60}")
    print(f"Total promotions extracted: {len(all_promotions)}")
    print(f"{'─'*60}")

    return {
        'store': store_key.replace('-', ' '),
        'store_key': store_key,
        'page_count': len(image_files),
        'total_pages': len(all_image_files),
        'promotion_count': len(all_promotions),
        'promotions': all_promotions
    }

def analyze_all_flyers_sample(flyer_images_dir="flyer_images", output_file="promotions.json", max_pages=MAX_PAGES_PER_STORE):
    """Analyze sample flyer images (first N pages per store) and extract promotions."""

    # Initialize OpenAI client
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

    if not os.path.exists(flyer_images_dir):
        print(f"✗ Flyer images directory not found: {flyer_images_dir}")
        return {}

    # Get all store directories
    store_dirs = sorted([
        d for d in os.listdir(flyer_images_dir)
        if os.path.isdir(os.path.join(flyer_images_dir, d))
    ])

    if not store_dirs:
        print(f"✗ No store directories found in {flyer_images_dir}")
        return {}

    print("="*60)
    print(f"Analyzing Flyer Samples ({max_pages} pages per store)")
    print("="*60)
    print(f"Stores: {', '.join([s.replace('-', ' ').title() for s in store_dirs])}")
    print()

    all_results = {}
    stats = {
        'stores_processed': 0,
        'stores_succeeded': 0,
        'total_pages': 0,
        'total_promotions': 0,
        'failed_stores': []
    }

    for store_key in store_dirs:
        try:
            stats['stores_processed'] += 1

            result = analyze_store_flyers_sample(client, store_key, flyer_images_dir, max_pages)

            if result and result['promotions']:
                all_results[store_key] = result
                stats['stores_succeeded'] += 1
                stats['total_pages'] += result['page_count']
                stats['total_promotions'] += result['promotion_count']
            else:
                stats['failed_stores'].append(store_key)

        except Exception as e:
            print(f"\n✗ Error analyzing {store_key}: {e}")
            stats['failed_stores'].append(store_key)

    # Save results
    with open(output_file, 'w') as f:
        json.dump(all_results, f, indent=2)

    # Print final summary
    print(f"\n{'='*60}")
    print("ANALYSIS COMPLETE")
    print(f"{'='*60}")
    print(f"Stores processed: {stats['stores_processed']}")
    print(f"Stores succeeded: {stats['stores_succeeded']}")
    print(f"Total pages analyzed: {stats['total_pages']}")
    print(f"Total promotions extracted: {stats['total_promotions']}")

    if stats['failed_stores']:
        print(f"\nFailed stores:")
        for store in stats['failed_stores']:
            print(f"  - {store}")

    print(f"\n✓ Results saved to: {output_file}")
    print(f"{'='*60}\n")

    return all_results

if __name__ == "__main__":
    print("="*60)
    print("FLYER PROMOTION ANALYZER (SAMPLE MODE)")
    print(f"Processing first {MAX_PAGES_PER_STORE} pages per store")
    print("="*60)
    print()

    # Analyze sample flyers
    results = analyze_all_flyers_sample()

    if results:
        # Print summary by store
        print("\nPromotions by Store:")
        for store_key, data in results.items():
            print(f"  {data['store'].title()}: {data['promotion_count']} items ({data['page_count']}/{data['total_pages']} pages)")
    else:
        print("⚠ No promotions extracted!")
