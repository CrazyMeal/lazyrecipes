"""
Unified Flyer Processing Pipeline

Consolidates the complete flyer processing workflow:
1. Discover grocery store flyers from RedFlagDeals
2. Extract image URLs from each flyer page
3. Download all flyer images
4. Analyze images with OpenAI Vision API to extract promotions

Usage:
    python flyer_processor.py                    # Process all stores, all pages
    python flyer_processor.py --pages 2          # Process first 2 pages per store
    python flyer_processor.py --exclude costco   # Exclude specific stores
"""

import os
import json
import time
import base64
import re
from pathlib import Path
from playwright.sync_api import sync_playwright
import requests
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


# ============================================================================
# STEP 1: DISCOVER FLYERS
# ============================================================================

def discover_flyers():
    """
    Discover latest grocery store flyer URLs from RedFlagDeals.

    Returns:
        List of flyer dictionaries with store, title, date_range, and url
    """
    flyers = []

    print("\n" + "="*60)
    print("STEP 1: DISCOVERING FLYERS")
    print("="*60)

    with sync_playwright() as p:
        print("Launching browser...")
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        print("Navigating to RedFlagDeals flyers page...")
        page.goto("https://www.redflagdeals.com/flyers/", wait_until="domcontentloaded")
        time.sleep(3)

        # Close popups
        try:
            popup_selectors = [
                'button:has-text("Close")',
                '[aria-label="Close"]',
                '.close-button',
                'button.btn-close'
            ]
            for selector in popup_selectors:
                try:
                    page.click(selector, timeout=2000)
                except:
                    pass
            page.keyboard.press("Escape")
        except:
            pass

        # Wait for flyer cards
        print("Extracting flyer information...")
        page.wait_for_selector('.flyer_listing', timeout=10000)
        flyer_cards = page.query_selector_all('.flyer_listing')
        print(f"Found {len(flyer_cards)} total flyers\n")

        # Target grocery stores
        grocery_stores = [
            'super c', 'metro', 'walmart', 'iga', 'maxi',
            'provigo', 'loblaws', 'no frills', 'food basics',
            'freshco', 'costco', 'carrefour'
        ]

        for card in flyer_cards:
            try:
                store_name = card.get_attribute('data-dealer-name')
                if not store_name:
                    continue

                store_name = store_name.strip().lower()

                # Check if grocery store
                if not any(grocery in store_name for grocery in grocery_stores):
                    continue

                # Get flyer link
                link_elem = card.query_selector('a.flyer_image')
                if not link_elem:
                    continue

                flyer_url = link_elem.get_attribute('href')
                if not flyer_url:
                    continue

                if not flyer_url.startswith('http'):
                    flyer_url = f"https://www.redflagdeals.com/flyers/{flyer_url.lstrip('/')}"

                # Get metadata
                title_elem = card.query_selector('.flyer_title')
                title = title_elem.inner_text().strip() if title_elem else "Weekly Savings"

                date_elem = card.query_selector('.flyer_dates')
                date_range = date_elem.inner_text().strip() if date_elem else "Current Week"

                flyer_info = {
                    'store': store_name,
                    'title': title,
                    'date_range': date_range,
                    'url': flyer_url
                }

                flyers.append(flyer_info)
                print(f"✓ {store_name.title()} - {date_range}")

            except Exception as e:
                print(f"✗ Error processing flyer: {e}")
                continue

        browser.close()

    print(f"\n✓ Discovered {len(flyers)} grocery store flyers")
    return flyers


# ============================================================================
# STEP 2: EXTRACT IMAGE URLs
# ============================================================================

def extract_image_urls(flyer_url, store_name):
    """
    Extract all image URLs from a flyer page.

    Args:
        flyer_url: Full URL to the flyer page
        store_name: Name of the store

    Returns:
        List of image URLs
    """
    image_urls = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        page.goto(flyer_url, wait_until="domcontentloaded")
        time.sleep(2)

        html_content = page.content()
        browser.close()

        # Extract image URLs from tileSources
        pattern = r'https://[a-z]\.dam-img\.rfdcontent\.com/cms/[0-9/]+_original\.jpg'
        matches = re.findall(pattern, html_content)

        if matches:
            seen = set()
            for url in matches:
                if url not in seen:
                    seen.add(url)
                    image_urls.append(url)

    return image_urls


def extract_all_image_urls(flyers):
    """
    Extract image URLs for all discovered flyers.

    Args:
        flyers: List of flyer dictionaries

    Returns:
        Dictionary mapping store keys to their image data
    """
    print("\n" + "="*60)
    print("STEP 2: EXTRACTING IMAGE URLs")
    print("="*60)

    all_image_data = {}

    for flyer in flyers:
        store = flyer['store']
        url = flyer['url']

        try:
            print(f"\nExtracting: {store.title()}...")
            image_urls = extract_image_urls(url, store)

            if image_urls:
                store_key = store.lower().replace(' ', '-')
                all_image_data[store_key] = {
                    'store': store,
                    'title': flyer['title'],
                    'date_range': flyer['date_range'],
                    'url': url,
                    'image_urls': image_urls,
                    'image_count': len(image_urls)
                }
                print(f"  ✓ Found {len(image_urls)} pages")
            else:
                print(f"  ⚠ No images found")

        except Exception as e:
            print(f"  ✗ Error: {e}")

    total_images = sum(data['image_count'] for data in all_image_data.values())
    print(f"\n✓ Extracted {total_images} images from {len(all_image_data)} stores")

    return all_image_data


# ============================================================================
# STEP 3: DOWNLOAD IMAGES
# ============================================================================

def download_store_images(store_key, store_data, base_folder="flyer_images", limit_pages=None):
    """
    Download all images for a single store.

    Args:
        store_key: Clean store name (e.g., 'super-c')
        store_data: Dictionary with store info and image URLs
        base_folder: Base directory for flyer images
        limit_pages: Optional limit on number of pages to download

    Returns:
        Number of successfully downloaded images
    """
    store_name = store_data['store']
    image_urls = store_data['image_urls']

    # Apply page limit if specified
    if limit_pages:
        image_urls = image_urls[:limit_pages]

    output_folder = os.path.join(base_folder, store_key)
    os.makedirs(output_folder, exist_ok=True)

    downloaded = 0

    for idx, url in enumerate(image_urls, 1):
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36',
                'Referer': 'https://www.redflagdeals.com/',
                'Accept': 'image/avif,image/webp,image/apng,image/*,*/*;q=0.8',
            }

            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()

            filename = f"{store_key}_page_{idx:03d}.jpg"
            filepath = os.path.join(output_folder, filename)

            with open(filepath, 'wb') as f:
                f.write(response.content)

            downloaded += 1

        except Exception as e:
            print(f"  ✗ Page {idx} failed: {e}")

    return downloaded


def download_all_images(image_data, limit_pages=None):
    """
    Download images for all stores.

    Args:
        image_data: Dictionary with store image data
        limit_pages: Optional limit on pages per store

    Returns:
        Download statistics
    """
    print("\n" + "="*60)
    print("STEP 3: DOWNLOADING IMAGES")
    print("="*60)

    stats = {
        'stores_processed': 0,
        'stores_succeeded': 0,
        'total_downloaded': 0,
        'failed_stores': []
    }

    for store_key, store_data in image_data.items():
        try:
            store_name = store_data['store']
            page_count = len(store_data['image_urls'])
            limit_msg = f" (limited to {limit_pages})" if limit_pages else ""

            print(f"\nDownloading: {store_name.title()} - {page_count} pages{limit_msg}")

            stats['stores_processed'] += 1
            downloaded = download_store_images(store_key, store_data, limit_pages=limit_pages)

            if downloaded > 0:
                stats['stores_succeeded'] += 1
                stats['total_downloaded'] += downloaded
                print(f"  ✓ Downloaded {downloaded} pages")
            else:
                stats['failed_stores'].append(store_name)
                print(f"  ✗ No pages downloaded")

        except Exception as e:
            print(f"  ✗ Error: {e}")
            stats['failed_stores'].append(store_data['store'])

    print(f"\n✓ Downloaded {stats['total_downloaded']} images from {stats['stores_succeeded']} stores")

    return stats


# ============================================================================
# STEP 4: ANALYZE IMAGES
# ============================================================================

def encode_image(image_path):
    """Encode image to base64 for OpenAI API."""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


def analyze_flyer_image(client, image_path, store_name):
    """
    Analyze a single flyer image using OpenAI Vision API.

    Args:
        client: OpenAI client instance
        image_path: Path to flyer image
        store_name: Name of the store

    Returns:
        List of promotions extracted from the image
    """
    try:
        base64_image = encode_image(image_path)

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

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
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

        content = response.choices[0].message.content.strip()

        # Extract JSON from response
        if content.startswith("```json"):
            content = content.split("```json")[1].split("```")[0].strip()
        elif content.startswith("```"):
            content = content.split("```")[1].split("```")[0].strip()

        promotions = json.loads(content)

        # Add store name to each promotion
        for promo in promotions:
            promo['store'] = store_name

        return promotions

    except Exception as e:
        print(f"    ✗ Error: {e}")
        return []


def analyze_store_flyers(client, store_key, flyer_images_dir="flyer_images", limit_pages=None):
    """
    Analyze all flyer images for a single store.

    Args:
        client: OpenAI client instance
        store_key: Store directory name
        flyer_images_dir: Base directory containing store folders
        limit_pages: Optional limit on pages to analyze

    Returns:
        Dictionary with store info and extracted promotions
    """
    store_dir = os.path.join(flyer_images_dir, store_key)

    if not os.path.exists(store_dir):
        return None

    # Get image files
    image_files = sorted([
        f for f in os.listdir(store_dir)
        if f.endswith(('.jpg', '.jpeg', '.png'))
    ])

    if not image_files:
        return None

    # Apply page limit
    if limit_pages:
        image_files = image_files[:limit_pages]

    all_promotions = []

    for image_file in image_files:
        image_path = os.path.join(store_dir, image_file)
        promotions = analyze_flyer_image(
            client,
            image_path,
            store_key.replace('-', ' ')
        )
        all_promotions.extend(promotions)

    return {
        'store': store_key.replace('-', ' '),
        'store_key': store_key,
        'page_count': len(image_files),
        'promotion_count': len(all_promotions),
        'promotions': all_promotions
    }


def analyze_all_flyers(flyer_images_dir="flyer_images", exclude_stores=None, limit_pages=None):
    """
    Analyze all downloaded flyer images and extract promotions.

    Args:
        flyer_images_dir: Directory containing store folders
        exclude_stores: List of store keys to exclude
        limit_pages: Optional limit on pages per store

    Returns:
        Dictionary with all store promotions and statistics
    """
    print("\n" + "="*60)
    print("STEP 4: ANALYZING FLYERS WITH AI")
    print("="*60)

    if exclude_stores is None:
        exclude_stores = []

    # Initialize OpenAI client
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

    if not os.path.exists(flyer_images_dir):
        print(f"✗ Directory not found: {flyer_images_dir}")
        return {}

    # Get store directories
    store_dirs = sorted([
        d for d in os.listdir(flyer_images_dir)
        if os.path.isdir(os.path.join(flyer_images_dir, d))
        and d not in exclude_stores
    ])

    if not store_dirs:
        print(f"✗ No store directories found")
        return {}

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
            store_name = store_key.replace('-', ' ').title()
            print(f"\nAnalyzing: {store_name}")

            stats['stores_processed'] += 1

            result = analyze_store_flyers(client, store_key, flyer_images_dir, limit_pages)

            if result and result['promotions']:
                all_results[store_key] = result
                stats['stores_succeeded'] += 1
                stats['total_pages'] += result['page_count']
                stats['total_promotions'] += result['promotion_count']
                print(f"  ✓ Extracted {result['promotion_count']} promotions from {result['page_count']} pages")
            else:
                stats['failed_stores'].append(store_name)
                print(f"  ⚠ No promotions found")

        except Exception as e:
            print(f"  ✗ Error: {e}")
            stats['failed_stores'].append(store_key)

    print(f"\n✓ Analyzed {stats['total_pages']} pages, extracted {stats['total_promotions']} promotions")

    return {'results': all_results, 'stats': stats}


# ============================================================================
# MAIN ORCHESTRATION FUNCTION
# ============================================================================

def process_all_flyers(num_pages=None, exclude_stores=None, output_dir="promotion_results"):
    """
    Complete flyer processing pipeline: discover → extract → download → analyze.

    Args:
        num_pages: Optional limit on pages to process per store
        exclude_stores: List of store keys to exclude (e.g., ['costco', 'walmart'])
        output_dir: Directory to save results

    Returns:
        Dictionary with complete results and statistics
    """
    print("\n" + "="*70)
    print(" "*15 + "FLYER PROCESSING PIPELINE")
    print("="*70)

    if num_pages:
        print(f"Mode: Processing first {num_pages} pages per store")
    else:
        print("Mode: Processing ALL pages")

    if exclude_stores:
        print(f"Excluding: {', '.join(exclude_stores)}")

    # Create output directory
    os.makedirs(output_dir, exist_ok=True)

    # Step 1: Discover flyers
    flyers = discover_flyers()
    if not flyers:
        print("\n✗ No flyers discovered. Exiting.")
        return None

    # Step 2: Extract image URLs
    image_data = extract_all_image_urls(flyers)
    if not image_data:
        print("\n✗ No image URLs extracted. Exiting.")
        return None

    # Step 3: Download images
    download_stats = download_all_images(image_data, limit_pages=num_pages)

    # Step 4: Analyze flyers
    analysis_results = analyze_all_flyers(
        exclude_stores=exclude_stores,
        limit_pages=num_pages
    )

    if not analysis_results:
        print("\n✗ Analysis failed. Exiting.")
        return None

    # Save results
    results_file = os.path.join(output_dir, "promotions.json")
    with open(results_file, 'w') as f:
        json.dump(analysis_results['results'], f, indent=2)

    # Save summary
    summary_file = os.path.join(output_dir, "summary.json")
    summary = {
        'download_stats': download_stats,
        'analysis_stats': analysis_results['stats'],
        'stores': {
            k: {
                'promotion_count': v['promotion_count'],
                'page_count': v['page_count']
            }
            for k, v in analysis_results['results'].items()
        }
    }

    with open(summary_file, 'w') as f:
        json.dump(summary, f, indent=2)

    # Final summary
    print("\n" + "="*70)
    print(" "*25 + "PIPELINE COMPLETE")
    print("="*70)
    print(f"Stores processed: {analysis_results['stats']['stores_processed']}")
    print(f"Stores succeeded: {analysis_results['stats']['stores_succeeded']}")
    print(f"Total pages analyzed: {analysis_results['stats']['total_pages']}")
    print(f"Total promotions extracted: {analysis_results['stats']['total_promotions']}")
    print(f"\nResults saved to: {output_dir}/")
    print("  - promotions.json (detailed promotions)")
    print("  - summary.json (statistics)")
    print("="*70 + "\n")

    return analysis_results


# ============================================================================
# CLI ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Process grocery store flyers from RedFlagDeals")
    parser.add_argument(
        '--pages',
        type=int,
        default=None,
        help='Limit number of pages to process per store (default: all pages)'
    )
    parser.add_argument(
        '--exclude',
        nargs='+',
        default=None,
        help='Store keys to exclude (e.g., --exclude costco walmart)'
    )
    parser.add_argument(
        '--output',
        type=str,
        default='promotion_results',
        help='Output directory for results (default: promotion_results)'
    )

    args = parser.parse_args()

    # Run pipeline
    process_all_flyers(
        num_pages=args.pages,
        exclude_stores=args.exclude,
        output_dir=args.output
    )
