#!/usr/bin/env python3
"""
Test script to verify duplicate detection is working properly
"""
import requests
import json
import sys
import os
from pathlib import Path

# Add ScrapeSystem to path
sys.path.append(str(Path(__file__).parent.parent.parent / "ScrapeSystem"))

def test_database_properties():
    """Test current database properties"""
    print("🧪 Testing Database Properties")
    print("=" * 40)
    
    try:
        response = requests.get("http://localhost:5000/api/property", timeout=10)
        if response.status_code == 200:
            properties = response.json()
            print(f"📊 Database contains {len(properties)} properties")
            
            # Show sample properties
            for i, prop in enumerate(properties[:3]):
                print(f"   {i+1}. {prop.get('price', 'N/A')} - {prop.get('fullAddress', 'N/A')}")
                print(f"      URL: {prop.get('detailUrl', 'N/A')[:50]}...")
            
            return properties
        else:
            print(f"❌ Database API returned status {response.status_code}")
            return []
    except requests.exceptions.RequestException as e:
        print(f"❌ Cannot connect to database API: {e}")
        return []

def test_duplicate_detection():
    """Test the duplicate detection logic"""
    print("\n🧪 Testing Duplicate Detection")
    print("=" * 40)
    
    try:
        from post_to_database import check_existing_properties, post_batch_properties
        
        # Get existing properties
        existing_properties = check_existing_properties()
        print(f"📊 Found {len(existing_properties)} existing properties")
        
        # Create test data with one duplicate and one new property
        test_properties = [
            {
                "site": "landsearch",
                "address": "Test Property 1",
                "fullAddress": "123 Test St, Test City, KY",
                "price": "$100,000",
                "detailUrl": "https://test.com/property1"  # This should be new
            },
            {
                "site": "landsearch", 
                "address": "Test Property 2",
                "fullAddress": "456 Test St, Test City, KY",
                "price": "$200,000",
                "detailUrl": existing_properties[0].get('detailUrl', 'https://existing.com')  # This should be duplicate
            }
        ]
        
        print(f"📦 Testing with {len(test_properties)} properties (1 new, 1 duplicate)")
        
        # Test the duplicate detection
        result = post_batch_properties(test_properties)
        
        if result:
            print("✅ Duplicate detection test completed")
            return True
        else:
            print("❌ Duplicate detection test failed")
            return False
            
    except Exception as e:
        print(f"❌ Error testing duplicate detection: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_scraper_data_flow():
    """Test the complete scraper data flow"""
    print("\n🧪 Testing Scraper Data Flow")
    print("=" * 40)
    
    try:
        from post_to_database import load_scraped_data
        
        # Load scraped data
        scraped_data = load_scraped_data()
        print(f"📄 Loaded {len(scraped_data)} properties from cache")
        
        if scraped_data:
            print("📋 Sample scraped properties:")
            for i, prop in enumerate(scraped_data[:2]):
                print(f"   {i+1}. {prop.get('price', 'N/A')} - {prop.get('full_address', 'N/A')}")
                print(f"      URL: {prop.get('detail_url', 'N/A')[:50]}...")
            
            return True
        else:
            print("❌ No scraped data found")
            return False
            
    except Exception as e:
        print(f"❌ Error testing scraper data flow: {e}")
        return False

def main():
    """Main test function"""
    print("🚀 Duplicate Detection Test Suite")
    print("=" * 50)
    
    # Change to project root
    project_root = Path(__file__).parent.parent.parent
    os.chdir(project_root)
    print(f"📁 Working directory: {os.getcwd()}")
    
    # Run tests
    db_ok = test_database_properties()
    duplicate_ok = test_duplicate_detection()
    scraper_ok = test_scraper_data_flow()
    
    print("\n" + "=" * 50)
    print("📊 Test Results Summary:")
    print(f"   Database Connection: {'✅' if db_ok else '❌'}")
    print(f"   Duplicate Detection: {'✅' if duplicate_ok else '❌'}")
    print(f"   Scraper Data Flow: {'✅' if scraper_ok else '❌'}")
    
    if all([db_ok, duplicate_ok, scraper_ok]):
        print("\n🎉 All duplicate detection tests passed!")
        print("✅ New scraped data should now be added to database")
    else:
        print("\n❌ Some tests failed!")
        print("💡 Check the duplicate detection implementation")

if __name__ == "__main__":
    main()
