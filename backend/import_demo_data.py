"""
Import promotion data from results folder into TinyDB database.

This script loads the promotions.json file from the results/ folder
and imports all promotions into the database for the demo.

Usage:
    python backend/import_demo_data.py
"""

import os
import json
from datetime import datetime
from tinydb import TinyDB

# Configuration
RESULTS_FILE = "results/promotions.json"
DB_PATH = "data/promotions.json"


def import_promotions():
    """Import promotions from results folder into database."""

    print("\n" + "="*70)
    print(" "*20 + "IMPORT DEMO DATA")
    print("="*70)

    # Check if results file exists
    if not os.path.exists(RESULTS_FILE):
        print(f"\n✗ Error: {RESULTS_FILE} not found!")
        print("  Run the flyer processor first to generate promotion data.\n")
        return False

    # Create data directory if needed
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

    # Load promotions from results
    print(f"\n📂 Loading promotions from {RESULTS_FILE}...")
    with open(RESULTS_FILE, 'r') as f:
        data = json.load(f)

    # Flatten all promotions from all stores
    all_promotions = []
    stores_processed = 0

    for store_key, store_data in data.items():
        promotions = store_data.get('promotions', [])
        all_promotions.extend(promotions)
        stores_processed += 1
        print(f"  ✓ {store_data['store'].title()}: {len(promotions)} promotions")

    print(f"\n📊 Total promotions loaded: {len(all_promotions)} from {stores_processed} stores")

    # Initialize TinyDB
    print(f"\n💾 Importing into database: {DB_PATH}")
    db = TinyDB(DB_PATH)
    promotions_table = db.table('promotions')
    scrapes_table = db.table('scrapes')

    # Create scrape record
    scrape_id = datetime.now().isoformat()

    # Clear existing data
    promotions_table.truncate()
    scrapes_table.truncate()

    # Insert promotions with scrape_id
    for promo in all_promotions:
        promo_with_id = promo.copy()
        promo_with_id['scrape_id'] = scrape_id
        promotions_table.insert(promo_with_id)

    # Record scrape metadata
    scrapes_table.insert({
        'scrape_id': scrape_id,
        'timestamp': scrape_id,
        'promotion_count': len(all_promotions),
        'stores_count': stores_processed
    })

    print(f"  ✓ Imported {len(all_promotions)} promotions")
    print(f"  ✓ Created scrape record: {scrape_id}")

    db.close()

    print("\n" + "="*70)
    print(" "*25 + "IMPORT COMPLETE")
    print("="*70)
    print(f"\n✓ Database ready at: {DB_PATH}")
    print(f"✓ You can now start the backend server\n")

    return True


if __name__ == "__main__":
    success = import_promotions()
    exit(0 if success else 1)
