"""
Download Super C flyer images directly from extracted URLs.
No browser navigation required!
"""

import requests
import os
from urllib.parse import urlparse


def download_images_from_file(url_file="flyer_image_urls.txt", output_folder="flyer_images/super-c-direct"):
    """Download all images from URL list."""

    # Create output folder
    os.makedirs(output_folder, exist_ok=True)

    # Read URLs
    with open(url_file, 'r') as f:
        urls = [line.strip() for line in f if line.strip()]

    print(f"Found {len(urls)} images to download\n")

    downloaded = 0
    failed = []

    for idx, url in enumerate(urls, 1):
        try:
            print(f"[{idx}/{len(urls)}] Downloading: {url}")

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
            filename = f"super-c_page_{idx:03d}.jpg"
            filepath = os.path.join(output_folder, filename)

            # Save image
            with open(filepath, 'wb') as f:
                f.write(response.content)

            size_mb = len(response.content) / (1024 * 1024)
            print(f"  ✓ Saved: {filepath} ({size_mb:.2f} MB)\n")
            downloaded += 1

        except Exception as e:
            print(f"  ✗ Failed: {e}\n")
            failed.append((idx, url))

    print(f"{'='*60}")
    print(f"✓ Download complete!")
    print(f"  Success: {downloaded}/{len(urls)}")
    if failed:
        print(f"  Failed: {len(failed)}")
        for idx, url in failed:
            print(f"    - Page {idx}: {url}")
    print(f"  Saved to: {output_folder}/")
    print(f"{'='*60}")


if __name__ == "__main__":
    download_images_from_file()
