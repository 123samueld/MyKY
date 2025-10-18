#!/usr/bin/env python3
"""
Test script to verify timestamp functionality
"""
import requests
import json
import sys
import os
from datetime import datetime
from pathlib import Path

# Add ScrapeSystem to path
sys.path.append(str(Path(__file__).parent.parent.parent / "ScrapeSystem"))

def test_scraper_timestamp():
    """Test that scraper includes timestamp in data"""
    print("🧪 Testing Scraper Timestamp")
    print("=" * 40)
    
    try:
        from SiteScrapers.landsearch_scraper import load_landsearch_cache
        
        # Load cached data
        cache_data = load_landsearch_cache()
        print(f"📄 Loaded {len(cache_data)} properties from cache")
        
        if cache_data:
            # Check if timestamp is present
            sample_property = cache_data[0]
            timestamp = sample_property.get('scrape_timestamp', 'Not found')
            print(f"📅 Sample property timestamp: {timestamp}")
            
            if timestamp != 'Not found':
                print("✅ Scrape timestamp found in cached data")
                return True
            else:
                print("❌ Scrape timestamp not found in cached data")
                return False
        else:
            print("❌ No cached data found")
            return False
            
    except Exception as e:
        print(f"❌ Error testing scraper timestamp: {e}")
        return False

def test_database_timestamp():
    """Test that database includes timestamp in properties"""
    print("\n🧪 Testing Database Timestamp")
    print("=" * 40)
    
    try:
        response = requests.get("http://localhost:5000/api/property", timeout=10)
        if response.status_code == 200:
            properties = response.json()
            print(f"📊 Database contains {len(properties)} properties")
            
            if properties:
                # Check if timestamp is present in database
                sample_property = properties[0]
                scraped_at = sample_property.get('scrapedAt', 'Not found')
                created_at = sample_property.get('createdAt', 'Not found')
                
                print(f"📅 Sample property scrapedAt: {scraped_at}")
                print(f"📅 Sample property createdAt: {created_at}")
                
                if scraped_at != 'Not found':
                    print("✅ ScrapedAt timestamp found in database")
                    return True
                else:
                    print("❌ ScrapedAt timestamp not found in database")
                    return False
            else:
                print("❌ No properties found in database")
                return False
        else:
            print(f"❌ Database API returned status {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Cannot connect to database API: {e}")
        return False

def test_timestamp_conversion():
    """Test that timestamp conversion works properly"""
    print("\n🧪 Testing Timestamp Conversion")
    print("=" * 40)
    
    try:
        from post_to_database import convert_to_property_model
        
        # Test data with timestamp
        test_data = {
            "site": "landsearch",
            "address": "Test Property",
            "full_address": "123 Test St, Test City, KY",
            "price": "$100,000",
            "scrape_timestamp": "2024-10-18 15:30:45"
        }
        
        # Convert to property model
        property_model = convert_to_property_model(test_data)
        
        scraped_at = property_model.get('scrapedAt', 'Not found')
        print(f"📅 Converted timestamp: {scraped_at}")
        
        if scraped_at != 'Not found':
            print("✅ Timestamp conversion working")
            return True
        else:
            print("❌ Timestamp conversion failed")
            return False
            
    except Exception as e:
        print(f"❌ Error testing timestamp conversion: {e}")
        return False

def test_timestamp_format():
    """Test that timestamps are in the correct format"""
    print("\n🧪 Testing Timestamp Format")
    print("=" * 40)
    
    try:
        # Test current timestamp format
        current_time = datetime.now()
        timestamp_str = current_time.strftime("%Y-%m-%d %H:%M:%S")
        print(f"📅 Current timestamp format: {timestamp_str}")
        
        # Test ISO format conversion
        iso_format = current_time.isoformat()
        print(f"📅 ISO format: {iso_format}")
        
        # Test parsing
        parsed_time = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
        print(f"📅 Parsed time: {parsed_time}")
        
        print("✅ Timestamp format testing completed")
        return True
        
    except Exception as e:
        print(f"❌ Error testing timestamp format: {e}")
        return False

def main():
    """Main test function"""
    print("🚀 Timestamp Feature Test Suite")
    print("=" * 50)
    
    # Change to project root
    project_root = Path(__file__).parent.parent.parent
    os.chdir(project_root)
    print(f"📁 Working directory: {os.getcwd()}")
    
    # Run tests
    scraper_ok = test_scraper_timestamp()
    database_ok = test_database_timestamp()
    conversion_ok = test_timestamp_conversion()
    format_ok = test_timestamp_format()
    
    print("\n" + "=" * 50)
    print("📊 Test Results Summary:")
    print(f"   Scraper Timestamp: {'✅' if scraper_ok else '❌'}")
    print(f"   Database Timestamp: {'✅' if database_ok else '❌'}")
    print(f"   Timestamp Conversion: {'✅' if conversion_ok else '❌'}")
    print(f"   Timestamp Format: {'✅' if format_ok else '❌'}")
    
    if all([scraper_ok, database_ok, conversion_ok, format_ok]):
        print("\n🎉 All timestamp tests passed!")
        print("✅ Scrape timestamps are working correctly")
    else:
        print("\n❌ Some timestamp tests failed!")
        print("💡 Check the timestamp implementation")

if __name__ == "__main__":
    main()
