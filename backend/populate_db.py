"""
One-time script to populate TinyDB with existing promotions data.
"""

import os
import json
import glob
from datetime import datetime
from tinydb import TinyDB

PROMOTIONS_DIR = "data/promotion_results"
DB_PATH = "data/promotions.json"

def load_promotions_from_files():
    """Load all promotions from the promotion_results directory."""
    promotions = []

    if not os.path.exists(PROMOTIONS_DIR):
        return promotions

    # Load all store promotion files
    for filepath in glob.glob(os.path.join(PROMOTIONS_DIR, "*_promotions.json")):
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
                promotions.extend(data.get('promotions', []))
        except Exception as e:
            print(f"Error loading {filepath}: {e}")

    return promotions


def save_to_db(promotions):
    """Save promotions to TinyDB."""
    db = TinyDB(DB_PATH)
    promotions_table = db.table('promotions')
    scrapes_table = db.table('scrapes')

    scrape_id = datetime.now().isoformat()

    # Clear old promotions
    promotions_table.truncate()

    # Insert new promotions with scrape_id
    for promo in promotions:
        promo_with_id = promo.copy()
        promo_with_id['scrape_id'] = scrape_id
        promotions_table.insert(promo_with_id)

    # Record the scrape metadata
    scrapes_table.insert({
        'scrape_id': scrape_id,
        'timestamp': scrape_id,
        'promotion_count': len(promotions)
    })

    print(f"✓ Saved {len(promotions)} promotions to database")
    print(f"✓ Scrape ID: {scrape_id}")

    db.close()


if __name__ == '__main__':
    print("Loading promotions from files...")
    promotions = load_promotions_from_files()
    print(f"Found {len(promotions)} promotions")

    print("\nSaving to database...")
    save_to_db(promotions)

    print("\n✓ Done!")
