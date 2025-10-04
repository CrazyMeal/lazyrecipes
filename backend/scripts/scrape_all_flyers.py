"""
Master script to scrape all grocery store flyers.
Orchestrates the complete pipeline:
1. Discover latest flyer URLs
2. Extract image URLs from each flyer
3. Download all images
"""

import sys
import os

# Import our scraping modules
from scripts.discover_flyers import discover_latest_flyers, save_flyer_urls
from scripts.extract_flyer_urls import extract_all_flyers, save_image_urls
from scripts.download_all_flyers import download_all_flyers

def main():
    """Run the complete flyer scraping pipeline."""

    print("="*60)
    print("LAZYRECIPES FLYER SCRAPER")
    print("="*60)
    print("\nThis will:")
    print("1. Discover latest grocery store flyers")
    print("2. Extract image URLs from each flyer")
    print("3. Download all flyer images")
    print()

    try:
        # Step 1: Discover flyers
        print("\n" + "="*60)
        print("STEP 1: Discovering Latest Flyers")
        print("="*60 + "\n")

        flyers = discover_latest_flyers()

        if not flyers:
            print("✗ No flyers discovered. Exiting.")
            return 1

        flyers_file = save_flyer_urls(flyers)
        print(f"✓ Discovered {len(flyers)} grocery store flyers\n")

        # Step 2: Extract image URLs
        print("\n" + "="*60)
        print("STEP 2: Extracting Image URLs")
        print("="*60 + "\n")

        image_data = extract_all_flyers(flyers_file)

        if not image_data:
            print("✗ No images extracted. Exiting.")
            return 1

        urls_file = save_image_urls(image_data)
        total_images = sum(data['image_count'] for data in image_data.values())
        print(f"✓ Extracted {total_images} image URLs from {len(image_data)} stores\n")

        # Step 3: Download images
        print("\n" + "="*60)
        print("STEP 3: Downloading Images")
        print("="*60 + "\n")

        stats = download_all_flyers(urls_file)

        # Final summary
        print("\n" + "="*60)
        print("PIPELINE COMPLETE!")
        print("="*60)
        print(f"✓ {stats['stores_succeeded']}/{stats['stores_processed']} stores downloaded")
        print(f"✓ {stats['total_downloaded']}/{stats['total_images']} images saved")
        print(f"✓ Images saved to: flyer_images/")
        print("="*60 + "\n")

        return 0

    except KeyboardInterrupt:
        print("\n\n✗ Interrupted by user. Exiting.")
        return 1

    except Exception as e:
        print(f"\n\n✗ Pipeline failed: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())
