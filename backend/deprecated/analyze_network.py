"""
Analyze network traffic to find flyer image URLs.
"""

from playwright.sync_api import sync_playwright
import time
import json


def analyze_network_traffic():
    image_requests = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        # Listen to all network requests
        def handle_request(request):
            url = request.url
            resource_type = request.resource_type

            # Log image requests
            if resource_type == "image" or any(ext in url.lower() for ext in ['.jpg', '.jpeg', '.png', '.webp']):
                print(f"[IMAGE] {url}")
                image_requests.append({
                    'url': url,
                    'type': resource_type
                })

        page.on("request", handle_request)

        url = "https://www.redflagdeals.com/flyers/super-c/weekly-savings-oct-02-to-oct-08-2025-272304/"
        print(f"Loading: {url}\n")
        page.goto(url, wait_until="domcontentloaded", timeout=30000)

        # Wait for flyer to load
        page.wait_for_selector("#flyer_canvas", timeout=15000)
        time.sleep(3)

        # Close popups
        try:
            page.keyboard.press("Escape")
            time.sleep(1)
        except:
            pass

        print("\n=== Scrolling and navigating to trigger image loads ===\n")

        # Navigate through a few pages to see the pattern
        for i in range(5):
            print(f"\n--- Viewing page {i+1} ---")
            time.sleep(3)

            # Click next
            try:
                next_btn = page.query_selector("#flyer_next_page")
                if next_btn:
                    next_btn.click()
                    time.sleep(2)
            except:
                pass

        # Save captured image URLs
        with open('image_requests.json', 'w') as f:
            json.dump(image_requests, f, indent=2)

        print(f"\n\n{'='*60}")
        print(f"Total image requests captured: {len(image_requests)}")
        print(f"Saved to: image_requests.json")
        print(f"{'='*60}\n")

        # Analyze patterns
        print("\n=== Analyzing URL Patterns ===\n")

        # Group by domain
        domains = {}
        for req in image_requests:
            url = req['url']
            domain = url.split('/')[2] if len(url.split('/')) > 2 else 'unknown'
            if domain not in domains:
                domains[domain] = []
            domains[domain].append(url)

        for domain, urls in domains.items():
            print(f"\nDomain: {domain}")
            print(f"  Count: {len(urls)}")
            if urls:
                print(f"  Example: {urls[0][:120]}")

        input("\nPress Enter to close browser...")
        browser.close()


if __name__ == "__main__":
    analyze_network_traffic()
