"""
Analyze first N pages for all stores (except specified exclusions).
Saves results to organized folder structure.
"""

import os
import json
from analyze_flyers import analyze_flyer_image
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

def analyze_store_partial(client, store_key, num_pages, flyer_images_dir="flyer_images", output_dir="promotion_results"):
    """Analyze first N pages of a store's flyers."""

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

    # Save result to organized folder
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, f"{store_key}_promotions.json")

    with open(output_file, 'w') as f:
        json.dump(result, f, indent=2)

    print(f"✓ Results saved to: {output_file}\n")

    # Show sample promotions
    if all_promotions:
        print("Sample promotions (first 5):")
        for promo in all_promotions[:5]:
            print(f"  - {promo['item']}: ${promo['price']}/{promo['unit']} ({promo['discount']})")
        print()

    return result

def analyze_all_stores_partial(num_pages=2, exclude_stores=None, flyer_images_dir="flyer_images", output_dir="promotion_results"):
    """Analyze first N pages for all stores."""

    if exclude_stores is None:
        exclude_stores = []

    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

    # Get all store directories
    all_stores = sorted([
        d for d in os.listdir(flyer_images_dir)
        if os.path.isdir(os.path.join(flyer_images_dir, d))
    ])

    # Filter out excluded stores
    stores_to_process = [s for s in all_stores if s not in exclude_stores]

    print("="*60)
    print(f"Processing {len(stores_to_process)} Stores ({num_pages} pages each)")
    print("="*60)
    print(f"Stores: {', '.join([s.replace('-', ' ').title() for s in stores_to_process])}")

    if exclude_stores:
        print(f"Excluded: {', '.join(exclude_stores)}")
    print()

    results = {}
    stats = {
        'stores_processed': 0,
        'stores_succeeded': 0,
        'total_pages': 0,
        'total_promotions': 0,
        'failed_stores': []
    }

    for store_key in stores_to_process:
        try:
            stats['stores_processed'] += 1

            result = analyze_store_partial(client, store_key, num_pages, flyer_images_dir, output_dir)

            if result and result['promotions']:
                results[store_key] = result
                stats['stores_succeeded'] += 1
                stats['total_pages'] += result['page_count']
                stats['total_promotions'] += result['promotion_count']
            else:
                stats['failed_stores'].append(store_key)

        except Exception as e:
            print(f"\n✗ Error analyzing {store_key}: {e}\n")
            stats['failed_stores'].append(store_key)

    # Save combined summary
    summary_file = os.path.join(output_dir, "_summary.json")
    with open(summary_file, 'w') as f:
        json.dump({
            'stats': stats,
            'stores': {k: {'promotion_count': v['promotion_count'], 'page_count': v['page_count']} for k, v in results.items()}
        }, f, indent=2)

    # Print final summary
    print("\n" + "="*60)
    print("ANALYSIS COMPLETE")
    print("="*60)
    print(f"Stores processed: {stats['stores_processed']}")
    print(f"Stores succeeded: {stats['stores_succeeded']}")
    print(f"Total pages analyzed: {stats['total_pages']}")
    print(f"Total promotions extracted: {stats['total_promotions']}")

    if stats['failed_stores']:
        print(f"\nFailed stores:")
        for store in stats['failed_stores']:
            print(f"  - {store}")

    print(f"\n✓ Results saved to: {output_dir}/")
    print("="*60 + "\n")

    return results

if __name__ == "__main__":
    # Process all stores except costco, 2 pages each
    analyze_all_stores_partial(
        num_pages=2,
        exclude_stores=['costco', 'super-c-direct'],  # Exclude costco and old test folder
        output_dir="promotion_results"
    )
