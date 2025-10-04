"""
Analyze a specific number of pages for a single store.
Usage: python analyze_store_partial.py <store_name> <num_pages>
"""

import sys
import json
from analyze_flyers import analyze_flyer_image
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

def analyze_store_partial(store_key, num_pages, flyer_images_dir="flyer_images"):
    """Analyze first N pages of a store's flyers."""

    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
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
    image_files = all_image_files[:num_pages]

    print(f"\n{'='*60}")
    print(f"Analyzing: {store_key.replace('-', ' ').title()}")
    print(f"Pages: {len(image_files)}/{len(all_image_files)}")
    print(f"{'='*60}\n")

    all_promotions = []

    for image_file in image_files:
        image_path = os.path.join(store_dir, image_file)
        promotions = analyze_flyer_image(
            client,
            image_path,
            store_key.replace('-', ' ')
        )
        all_promotions.extend(promotions)

    print(f"\n{'─'*60}")
    print(f"Total promotions extracted: {len(all_promotions)}")
    print(f"{'─'*60}\n")

    result = {
        'store': store_key.replace('-', ' '),
        'store_key': store_key,
        'page_count': len(image_files),
        'total_pages': len(all_image_files),
        'promotion_count': len(all_promotions),
        'promotions': all_promotions
    }

    # Save result
    output_file = f"test_promotions_{store_key}.json"
    with open(output_file, 'w') as f:
        json.dump(result, f, indent=2)

    print(f"✓ Results saved to: {output_file}\n")

    # Show sample promotions
    if all_promotions:
        print("Sample promotions (first 10):")
        for promo in all_promotions[:10]:
            print(f"  - {promo['item']}: ${promo['price']}/{promo['unit']} ({promo['discount']})")

    return result

if __name__ == "__main__":
    store_key = sys.argv[1] if len(sys.argv) > 1 else "maxi"
    num_pages = int(sys.argv[2]) if len(sys.argv) > 2 else 2

    analyze_store_partial(store_key, num_pages)
