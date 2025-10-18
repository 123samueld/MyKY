#!/usr/bin/env python3
"""
Script to POST scraped property data to the .NET backend API
"""
import json
import requests
import os
from datetime import datetime
from time import sleep
from typing import List, Dict
from pathlib import Path

# Configuration
API_BASE_URL = "http://localhost:5000/api"

# Get the correct cache directory from FilePathCompendium
def get_cache_file_path():
    """Get the correct cache file path from FilePathCompendium.json"""
    try:
        # Get the project root directory
        script_dir = Path(__file__).parent
        project_root = script_dir.parent
        
        # Load FilePathCompendium.json
        config_file = project_root / "Utilities" / "FilePathCompendium.json"
        with open(config_file, 'r') as f:
            config = json.load(f)
        
        # Get the scraper cache directory
        cache_dir = config.get('scraperCacheDirectory', './ScrapeSystem/ScrapedDataCache/')
        
        # Convert relative path to absolute path
        if cache_dir.startswith('./'):
            cache_dir = str(project_root / cache_dir[2:])
        elif not cache_dir.startswith('/'):
            cache_dir = str(project_root / cache_dir)
        
        return os.path.join(cache_dir, "landsearch_scrape_cache.json")
    except Exception as e:
        print(f"⚠️ Could not load config, using default path: {e}")
        return "ScrapedDataCache/landsearch_scrape_cache.json"

CACHE_FILE = get_cache_file_path()

def load_scraped_data() -> List[Dict]:
    """Load scraped data from cache file"""
    if not os.path.exists(CACHE_FILE):
        print(f"❌ Cache file not found: {CACHE_FILE}")
        return []
    
    with open(CACHE_FILE, 'r') as f:
        data = json.load(f)
    
    print(f"📄 Loaded {len(data)} properties from cache")
    return data

def convert_to_property_model(scraped_data: Dict) -> Dict:
    """Convert scraped data to Property model format"""
    # Parse scrape timestamp if available
    scrape_timestamp = scraped_data.get("scrape_timestamp", "")
    if scrape_timestamp:
        try:
            # Convert string timestamp to ISO format for database
            scrape_datetime = datetime.strptime(scrape_timestamp, "%Y-%m-%d %H:%M:%S")
            scrape_timestamp = scrape_datetime.isoformat()
        except ValueError:
            # If parsing fails, use current time
            scrape_timestamp = datetime.now().isoformat()
    else:
        scrape_timestamp = datetime.now().isoformat()
    
    return {
        "site": scraped_data.get("site", ""),
        "address": scraped_data.get("address", ""),
        "fullAddress": scraped_data.get("full_address", ""),
        "streetAddress": scraped_data.get("street_address", ""),
        "price": scraped_data.get("price", ""),
        "acres": scraped_data.get("acres", ""),
        "listedDate": scraped_data.get("listed_date", datetime.now().strftime("%Y-%m-%d")),
        "county": scraped_data.get("county", ""),
        "elevation": scraped_data.get("elevation", ""),
        "coordinates": scraped_data.get("coordinates", ""),
        "detailUrl": scraped_data.get("detail_url", ""),
        "scrapedAt": scrape_timestamp
    }

def post_single_property(property_data: Dict) -> bool:
    """POST a single property to the API"""
    try:
        response = requests.post(
            f"{API_BASE_URL}/property",
            json=property_data,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        if response.status_code == 201:
            print(f"✅ Property created successfully")
            return True
        else:
            print(f"❌ Failed to create property: {response.status_code} - {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Network error for property: {e}")
        return False

def check_existing_properties() -> List[Dict]:
    """Check what properties already exist in the database"""
    try:
        response = requests.get(f"{API_BASE_URL}/property", timeout=10)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"⚠️ Could not check existing properties: {response.status_code}")
            return []
    except requests.exceptions.RequestException as e:
        print(f"⚠️ Could not check existing properties: {e}")
        return []

def post_batch_properties(properties: List[Dict]) -> bool:
    """POST multiple properties in a single batch, avoiding duplicates"""
    try:
        # Check existing properties first
        existing_properties = check_existing_properties()
        existing_count = len(existing_properties)
        
        if existing_count > 0:
            print(f"📊 Database contains {existing_count} existing properties")
            
            # Check for actual duplicates by comparing detail URLs
            existing_urls = {prop.get('detailUrl', '') for prop in existing_properties}
            new_properties = []
            
            for prop in properties:
                if prop.get('detailUrl', '') not in existing_urls:
                    new_properties.append(prop)
                else:
                    print(f"⏭️ Skipping duplicate: {prop.get('detailUrl', '')[:50]}...")
            
            if not new_properties:
                print("ℹ️ All properties already exist in database - no new data to add")
                return True
            
            print(f"📦 Found {len(new_properties)} new properties to add")
            properties = new_properties
        
        response = requests.post(
            f"{API_BASE_URL}/property/batch",
            json=properties,
            headers={"Content-Type": "application/json"},
            timeout=60
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Batch created: {result.get('message', 'Unknown result')}")
            return True
        else:
            print(f"❌ Batch failed: {response.status_code} - {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Batch network error: {e}")
        return False

def main():
    """Main function to process scraped data and send to API"""
    print("🚀 Starting data transfer to .NET backend...")
    
    # Load scraped data
    scraped_data = load_scraped_data()
    if not scraped_data:
        print("❌ No data to process")
        return
    
    # Convert to Property model format
    properties = [convert_to_property_model(item) for item in scraped_data]
    print(f"🔄 Converted {len(properties)} properties to API format")
    
    # Check if API is available (with retries)
    max_retries = 10
    for attempt in range(max_retries):
        try:
            health_check = requests.get(f"{API_BASE_URL}/property", timeout=5)
            if health_check.status_code == 200:
                print("✅ API is available")
                break
            else:
                print(f"⏳ API not ready yet (attempt {attempt + 1}/{max_retries})...")
                sleep(2)
        except requests.exceptions.RequestException:
            print(f"⏳ Waiting for API (attempt {attempt + 1}/{max_retries})...")
            sleep(2)
    else:
        print("❌ Cannot connect to API after multiple attempts. Make sure .NET backend is running on port 5000")
        return
    
    print("✅ API is available")
    
    # Choose method: batch or individual
    use_batch = len(properties) > 1
    
    if use_batch:
        print("📦 Using batch upload...")
        success = post_batch_properties(properties)
    else:
        print("📄 Using individual uploads...")
        success_count = 0
        for prop in properties:
            if post_single_property(prop):
                success_count += 1
        success = success_count == len(properties)
        print(f"📊 Successfully uploaded {success_count}/{len(properties)} properties")
    
    if success:
        print("🎉 All data transferred successfully!")
    else:
        print("⚠️ Some data transfer failed")

if __name__ == "__main__":
    main()
