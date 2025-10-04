"""
Download flyer images for all discovered stores.
Uses extracted image URLs to download directly via HTTP.
"""

import requests
import os
import json
from urllib.parse import urlparse

def download_store_images(store_key, store_data, base_folder="flyer_images"):
    """
    Download all images for a single store.

    Args:
        store_key: Clean store name (e.g., 'super-c')
        store_data: Dictionary with store info and image URLs
        base_folder: Base directory for all flyer images

    Returns:
        Number of successfully downloaded images
    """

    store_name = store_data['store']
    image_urls = store_data['image_urls']
    output_folder = os.path.join(base_folder, store_key)

    print(f"\n{'='*60}")
    print(f"Downloading: {store_name.title()}")
    print(f"Pages: {len(image_urls)}")
    print(f"Output: {output_folder}/")
    print(f"{'='*60}\n")

    # Create output folder
    os.makedirs(output_folder, exist_ok=True)

    downloaded = 0
    failed = []

    for idx, url in enumerate(image_urls, 1):
        try:
            print(f"[{idx}/{len(image_urls)}] Downloading page {idx}...")

            # Download image with proper headers
            headers = {
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Referer': 'https://www.redflagdeals.com/',
                'Accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept-Language': 'en-US,en;q=0.9',
            }

            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()

            # Generate filename
            filename = f"{store_key}_page_{idx:03d}.jpg"
            filepath = os.path.join(output_folder, filename)

            # Save image
            with open(filepath, 'wb') as f:
                f.write(response.content)

            size_mb = len(response.content) / (1024 * 1024)
            print(f"  ✓ Saved ({size_mb:.2f} MB)\n")
            downloaded += 1

        except Exception as e:
            print(f"  ✗ Failed: {e}\n")
            failed.append((idx, url))

    # Print store summary
    print(f"{'─'*60}")
    print(f"{store_name.title()} Summary:")
    print(f"  Success: {downloaded}/{len(image_urls)}")
    if failed:
        print(f"  Failed: {len(failed)} pages")
    print(f"{'─'*60}")

    return downloaded

def download_all_flyers(image_urls_json="flyer_image_urls.json"):
    """
    Download images for all stores from extracted URL data.

    Args:
        image_urls_json: JSON file containing extracted image URLs

    Returns:
        Dictionary with download statistics
    """

    # Load image URLs
    with open(image_urls_json, 'r') as f:
        all_stores = json.load(f)

    print("="*60)
    print(f"Downloading Flyers for {len(all_stores)} Stores")
    print("="*60)

    stats = {
        'stores_processed': 0,
        'stores_succeeded': 0,
        'total_images': 0,
        'total_downloaded': 0,
        'failed_stores': []
    }

    for store_key, store_data in all_stores.items():
        try:
            stats['stores_processed'] += 1
            stats['total_images'] += store_data['image_count']

            downloaded = download_store_images(store_key, store_data)

            if downloaded > 0:
                stats['stores_succeeded'] += 1
                stats['total_downloaded'] += downloaded
            else:
                stats['failed_stores'].append(store_data['store'])

        except Exception as e:
            print(f"\n✗ Error downloading {store_data['store']}: {e}")
            stats['failed_stores'].append(store_data['store'])

    # Print final summary
    print(f"\n{'='*60}")
    print("FINAL SUMMARY")
    print(f"{'='*60}")
    print(f"Stores processed: {stats['stores_processed']}")
    print(f"Stores succeeded: {stats['stores_succeeded']}")
    print(f"Images downloaded: {stats['total_downloaded']}/{stats['total_images']}")

    if stats['failed_stores']:
        print(f"\nFailed stores:")
        for store in stats['failed_stores']:
            print(f"  - {store}")

    print(f"{'='*60}\n")

    return stats

if __name__ == "__main__":
    download_all_flyers()
