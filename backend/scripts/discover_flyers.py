"""
Discover the latest grocery store flyer URLs from RedFlagDeals.
Automatically finds current flyers for all major grocery stores.
"""

from playwright.sync_api import sync_playwright
import json
import time

def discover_latest_flyers():
    """Discover latest flyer URLs for all grocery stores."""

    flyers = []

    with sync_playwright() as p:
        print("Launching browser...")
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        # Navigate to flyers page
        print("Navigating to RedFlagDeals flyers page...")
        page.goto("https://www.redflagdeals.com/flyers/", wait_until="domcontentloaded")

        # Wait for content to load
        time.sleep(3)

        # Close any popups
        try:
            # Try multiple popup close selectors
            popup_selectors = [
                'button:has-text("Close")',
                '[aria-label="Close"]',
                '.close-button',
                'button.btn-close'
            ]
            for selector in popup_selectors:
                try:
                    page.click(selector, timeout=2000)
                    print("  Closed popup")
                except:
                    pass

            # Press ESC key to close any remaining popups
            page.keyboard.press("Escape")
        except:
            pass

        # Wait for flyer cards to load
        print("\nWaiting for flyer cards to load...")
        page.wait_for_selector('.flyer_listing', timeout=10000)

        # Extract all flyer cards
        print("Extracting flyer information...")
        flyer_cards = page.query_selector_all('.flyer_listing')
        print(f"Found {len(flyer_cards)} total flyers\n")

        # List of grocery stores to look for
        grocery_stores = [
            'super c', 'metro', 'walmart', 'iga', 'maxi',
            'provigo', 'loblaws', 'no frills', 'food basics',
            'freshco', 'costco', 'carrefour'
        ]

        for card in flyer_cards:
            try:
                # Get store name from data attribute
                store_name = card.get_attribute('data-dealer-name')
                if not store_name:
                    continue

                store_name = store_name.strip().lower()

                # Check if it's a grocery store
                is_grocery = any(grocery in store_name for grocery in grocery_stores)
                if not is_grocery:
                    continue

                # Get flyer link
                link_elem = card.query_selector('a.flyer_image')
                if not link_elem:
                    continue

                flyer_url = link_elem.get_attribute('href')
                if not flyer_url:
                    continue

                # Make absolute URL
                if not flyer_url.startswith('http'):
                    flyer_url = f"https://www.redflagdeals.com/flyers/{flyer_url}"

                # Get flyer title
                title_elem = card.query_selector('.flyer_title')
                title = title_elem.inner_text().strip() if title_elem else "Weekly Savings"

                # Get date range
                date_elem = card.query_selector('.flyer_dates')
                date_range = date_elem.inner_text().strip() if date_elem else "Current Week"

                flyer_info = {
                    'store': store_name,
                    'title': title,
                    'date_range': date_range,
                    'url': flyer_url
                }

                flyers.append(flyer_info)
                print(f"✓ Found: {store_name.title()}")
                print(f"  Title: {title}")
                print(f"  Dates: {date_range}")
                print(f"  URL: {flyer_url}\n")

            except Exception as e:
                print(f"Error processing flyer card: {e}")
                continue

        browser.close()

    return flyers

def save_flyer_urls(flyers, output_file="discovered_flyers.json"):
    """Save discovered flyer URLs to JSON file."""

    with open(output_file, 'w') as f:
        json.dump(flyers, f, indent=2)

    print(f"\n{'='*60}")
    print(f"✓ Saved {len(flyers)} grocery store flyers to {output_file}")
    print(f"{'='*60}\n")

    return output_file

if __name__ == "__main__":
    print("="*60)
    print("RedFlagDeals Flyer Discovery")
    print("="*60 + "\n")

    # Discover flyers
    flyers = discover_latest_flyers()

    # Save results
    if flyers:
        save_flyer_urls(flyers)

        # Print summary
        print("Discovered stores:")
        for flyer in flyers:
            print(f"  - {flyer['store'].title()}")
    else:
        print("⚠ No grocery store flyers found!")
