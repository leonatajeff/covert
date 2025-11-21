import os
import cloudscraper
from dotenv import load_dotenv
import pandas as pd
import datetime
import uuid
from typing import TypedDict, List

# Load environment variables
load_dotenv()
API_KEY = os.getenv("CSFLOAT_API_KEY")

# Constants
MARKET_HASH_NAME = "★ M9 Bayonet | Tiger Tooth (Factory New)"

HISTORY_DIR = os.path.join(os.path.dirname(__file__), "data")
HISTORY_CSV = os.path.join(HISTORY_DIR, "history.csv")

class Listing(TypedDict):
    price: float
    float_value: float
    paint_seed: str
    id: str
    inspect_link: str
    image: str

def save_history_csv(rows: List[Listing], path: str =HISTORY_CSV) -> None:
    """
    Append a list of Listing dicts to CSV using pandas.
    'rows' is a list where each element is one listing (one price/item).
    Adds a UTC ISO 'timestamp' for each row.
    """
    if not rows:
        return
    os.makedirs(os.path.dirname(path), exist_ok=True)
    df = pd.DataFrame(rows)
    df['timestamp'] = datetime.datetime.now().replace(microsecond=0).isoformat()
    header = not os.path.exists(path)
    df.to_csv(path, mode="a", header=header, index=False, encoding="utf-8")

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
        
        listings_data = response.json().get('data', [])
        
        # Clean the data for consumption
        results: List[Listing] = []
        for listing in listings_data:
            item = listing.get('item', {})
            
            results.append(
                {
                    "price": float(listing.get("price", 0)) / 100.0,
                    "float_value": float(item.get("float_value", 0.0)),
                    "paint_seed": str(item.get("paint_seed", "N/A")),
                    "id": str(listing.get("id", "")),
                    "inspect_link": str(item.get("inspect_link", "")),
                    "image": str(item.get("icon_url", "")),
                }
            )

        return results

    except Exception as e:
        print(f"Error in scraper: {e}")
        return []

# This block only runs when you execute 'uv run scraper.py'
if __name__ == "__main__":
    data = fetch_listings()
    
    print(f"Found {len(data)} listings for {MARKET_HASH_NAME}")
    save_history_csv(data)
    print("Saved fetch to", HISTORY_CSV)
    print("-" * 50)
    print(f"{'PRICE':<10} | {'FLOAT':<10} | {'ID'}")
    for item in data:
        print(f"${item['price']:<9.2f} | {item['float_value']:.6f}   | {item['id']}")
