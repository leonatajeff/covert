import os
import urllib.parse
import cloudscraper
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
API_KEY = os.getenv("CSFLOAT_API_KEY")

# Constants
MARKET_HASH_NAME = "★ M9 Bayonet | Tiger Tooth (Factory New)"

def fetch_listings():
    """
    Fetches the lowest price listings and returns a list of dictionaries.
    """
    url = "https://csfloat.com/api/v1/listings"
    
    params = {
        "market_hash_name": MARKET_HASH_NAME,
        "sort_by": "lowest_price",
        "limit": 10,
        "type": "buy_now"
    }
    
    headers = {
        "Accept": "application/json",
        "Authorization": API_KEY
    }

    scraper = cloudscraper.create_scraper()

    try:
        response = scraper.get(url, params=params, headers=headers)
        response.raise_for_status()
        
        # Safely get the data list
        listings_data = response.json().get('data', [])
        
        # Clean the data for consumption
        results = []
        for listing in listings_data:
            item = listing.get('item', {})
            
            results.append({
                "price": listing.get('price', 0) / 100.0,
                "float_value": item.get('float_value', 0.0),
                "paint_seed": item.get('paint_seed', 'N/A'),
                "id": listing.get('id'),
                "inspect_link": item.get('inspect_link', ''),
                "image": item.get('icon_url', '')
            })
            
        return results

    except Exception as e:
        print(f"Error in scraper: {e}")
        return []

# This block only runs when you execute 'uv run scraper.py'
if __name__ == "__main__":
    data = fetch_listings()
    print(f"Found {len(data)} listings for {MARKET_HASH_NAME}")
    print("-" * 50)
    print(f"{'PRICE':<10} | {'FLOAT':<10} | {'ID'}")
    for item in data:
        print(f"${item['price']:<9.2f} | {item['float_value']:.6f}   | {item['id']}")
