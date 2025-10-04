"""
Extract image URLs from a RedFlagDeals flyer page.
Automatically parses the OpenSeaDragon tileSources to find original image URLs.
"""

from playwright.sync_api import sync_playwright
import re
import json
import time

def extract_image_urls(flyer_url, store_name):
    """
    Extract all original image URLs from a flyer page.

    Args:
        flyer_url: Full URL to the flyer page
        store_name: Name of the store (for logging)

    Returns:
        List of image URLs
    """

    image_urls = []

    with sync_playwright() as p:
        print(f"\nExtracting images for: {store_name}")
        print(f"URL: {flyer_url}")

        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Navigate to flyer page
        page.goto(flyer_url, wait_until="domcontentloaded")

        # Wait for content to load
        time.sleep(2)

        # Get page HTML
        html_content = page.content()

        # Close browser (we only needed the HTML)
        browser.close()

        # Parse HTML to extract image URLs from tileSources
        # Look for pattern: https://[a-z].dam-img.rfdcontent.com/cms/.../*_original.jpg

        # Method 1: Look for tileSources array in OpenSeaDragon script
        pattern = r'https://[a-z]\.dam-img\.rfdcontent\.com/cms/[0-9/]+_original\.jpg'
        matches = re.findall(pattern, html_content)

        if matches:
            # Remove duplicates while preserving order
            seen = set()
            for url in matches:
                if url not in seen:
                    seen.add(url)
                    image_urls.append(url)

            print(f"  ✓ Found {len(image_urls)} images")
        else:
            print(f"  ⚠ No images found - flyer format may have changed")

        return image_urls

def extract_all_flyers(flyers_json="discovered_flyers.json"):
    """
    Extract image URLs for all discovered flyers.

    Args:
        flyers_json: Path to JSON file with flyer information

    Returns:
        Dictionary mapping store names to their image URLs
    """

    # Load discovered flyers
    with open(flyers_json, 'r') as f:
        flyers = json.load(f)

    print(f"Extracting images from {len(flyers)} flyers...\n")
    print("="*60)

    all_image_urls = {}

    for flyer in flyers:
        store = flyer['store']
        url = flyer['url']

        try:
            # Extract image URLs
            image_urls = extract_image_urls(url, store)

            if image_urls:
                # Clean store name for folder/key name
                store_key = store.lower().replace(' ', '-')
                all_image_urls[store_key] = {
                    'store': store,
                    'title': flyer['title'],
                    'date_range': flyer['date_range'],
                    'url': url,
                    'image_urls': image_urls,
                    'image_count': len(image_urls)
                }

        except Exception as e:
            print(f"  ✗ Error extracting {store}: {e}")

    return all_image_urls

def save_image_urls(image_data, output_file="flyer_image_urls.json"):
    """Save extracted image URLs to JSON file."""

    with open(output_file, 'w') as f:
        json.dump(image_data, f, indent=2)

    print(f"\n{'='*60}")
    print(f"✓ Extracted images for {len(image_data)} stores")
    print(f"✓ Saved to {output_file}")
    print(f"{'='*60}\n")

    # Print summary
    total_images = sum(data['image_count'] for data in image_data.values())
    print(f"Summary:")
    for store_key, data in image_data.items():
        print(f"  {data['store'].title()}: {data['image_count']} pages")
    print(f"\nTotal: {total_images} images across {len(image_data)} stores")

    return output_file

if __name__ == "__main__":
    print("="*60)
    print("Flyer Image URL Extractor")
    print("="*60)

    # Extract image URLs from all discovered flyers
    image_data = extract_all_flyers()

    # Save results
    if image_data:
        save_image_urls(image_data)
    else:
        print("\n⚠ No images extracted!")
