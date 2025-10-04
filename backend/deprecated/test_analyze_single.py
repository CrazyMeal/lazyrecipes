"""
Test script to analyze a single store's flyers.
Useful for testing before running full analysis.
"""

import sys
from analyze_flyers import analyze_store_flyers
from openai import OpenAI
import os
from dotenv import load_dotenv
import json

load_dotenv()

def main():
    store_key = sys.argv[1] if len(sys.argv) > 1 else "costco"

    print(f"Testing analysis on: {store_key}")
    print("="*60)

    # Initialize OpenAI client
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

    # Analyze single store
    result = analyze_store_flyers(client, store_key)

    if result:
        # Save test result
        output_file = f"test_promotions_{store_key}.json"
        with open(output_file, 'w') as f:
            json.dump(result, f, indent=2)

        print(f"\n✓ Test result saved to: {output_file}")

        # Show sample promotions
        if result['promotions']:
            print("\nSample promotions (first 5):")
            for promo in result['promotions'][:5]:
                print(f"  - {promo['item']}: ${promo['price']}/{promo['unit']} ({promo['discount']})")
    else:
        print("✗ Analysis failed")

if __name__ == "__main__":
    main()
