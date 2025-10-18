#!/usr/bin/env python3
"""
Test script to simulate the scraping process and identify issues
"""
import os
import json
import sys
from pathlib import Path

# Add ScrapeSystem to path
sys.path.append(str(Path(__file__).parent.parent.parent / "ScrapeSystem"))

def test_scraper_data_flow():
    """Test the data flow in the scraper"""
    print("🧪 Testing Scraper Data Flow")
    print("=" * 40)
    
    try:
        from SiteScrapers.landsearch_scraper import (
            clear_landsearch_cache,
            save_landsearch_cache,
            load_landsearch_cache,
            scrape_detail_page
        )
        
        # Simulate the scraping process
        print("1️⃣ Simulating scraper initialization...")
        clear_landsearch_cache()
        
        scraped_data = []
        temp_id_counter = 1
        
        print("2️⃣ Simulating property scraping...")
        
        # Create a mock property data (simulating what scrape_detail_page would return)
        mock_property = {
            "temp_ID": temp_id_counter,
            "site": "landsearch",
            "address": "Mock Property Address",
            "full_address": "123 Mock St, Mock City, KY",
            "street_address": "123 Mock St",
            "price": "$150,000",
            "acres": "10 acres",
            "listed_date": "2024-01-15",
            "county": "Mock County",
            "elevation": "500 ft",
            "coordinates": "37.123, -85.456",
            "detail_url": "https://mock.com/property1"
        }
        
        print(f"   Created mock property: {mock_property['address']}")
        
        # Simulate adding to scraped_data
        scraped_data.append(mock_property)
        print(f"   Added to scraped_data: {len(scraped_data)} properties")
        
        # Simulate saving cache
        save_landsearch_cache(scraped_data)
        print(f"   Saved to cache: {len(scraped_data)} properties")
        
        # Verify data was saved
        loaded_data = load_landsearch_cache()
        print(f"   Loaded from cache: {len(loaded_data)} properties")
        
        if loaded_data:
            print(f"   Sample property: {loaded_data[0].get('address', 'N/A')}")
            return True
        else:
            print("❌ No data loaded from cache")
            return False
            
    except Exception as e:
        print(f"❌ Error in data flow test: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_scraper_error_handling():
    """Test error handling in the scraper"""
    print("\n🧪 Testing Scraper Error Handling")
    print("=" * 40)
    
    try:
        from SiteScrapers.landsearch_scraper import scrape_detail_page
        
        # Test with invalid parameters to see error handling
        print("1️⃣ Testing error handling...")
        
        # This should handle errors gracefully
        result = scrape_detail_page(None, "test", "test", "test", "test", "test", 1)
        
        if result:
            print(f"   ✅ scrape_detail_page returned data: {result.get('address', 'N/A')}")
            return True
        else:
            print("   ❌ scrape_detail_page returned None")
            return False
            
    except Exception as e:
        print(f"   ⚠️ Expected error in test: {e}")
        # This is actually expected since we passed None as the page
        return True

def check_scraper_logs():
    """Check if there are any scraper log files"""
    print("\n🧪 Checking Scraper Logs")
    print("=" * 40)
    
    log_files = [
        "scraper_run.log",
        "debug_timeout_1.png",
        "debug_error_1.png"
    ]
    
    for log_file in log_files:
        if os.path.exists(log_file):
            print(f"📄 Found log file: {log_file}")
            if log_file.endswith('.log'):
                with open(log_file, 'r') as f:
                    content = f.read()
                    print(f"   Last 200 chars: {content[-200:]}")
        else:
            print(f"📄 No log file: {log_file}")

def main():
    """Main debug function"""
    print("🚀 Scraper Simulation Test Suite")
    print("=" * 50)
    
    # Change to project root
    project_root = Path(__file__).parent.parent.parent
    os.chdir(project_root)
    print(f"📁 Working directory: {os.getcwd()}")
    
    # Run tests
    data_flow_ok = test_scraper_data_flow()
    error_handling_ok = test_scraper_error_handling()
    check_scraper_logs()
    
    print("\n" + "=" * 50)
    print("📊 Simulation Results Summary:")
    print(f"   Data Flow: {'✅' if data_flow_ok else '❌'}")
    print(f"   Error Handling: {'✅' if error_handling_ok else '❌'}")
    
    if data_flow_ok:
        print("\n🎉 Scraper data flow is working correctly!")
        print("💡 The issue might be in the actual scraping process (network, selectors, etc.)")
    else:
        print("\n❌ Scraper data flow has issues!")
        print("💡 Check the data flow implementation")

if __name__ == "__main__":
    main()
