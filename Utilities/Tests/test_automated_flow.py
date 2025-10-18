#!/usr/bin/env python3
"""
Test script to verify the automated scraper -> database flow
"""
import os
import sys
import json
import time
import requests
from pathlib import Path

# Add ScrapeSystem to path
sys.path.append(str(Path(__file__).parent.parent.parent / "ScrapeSystem"))

def test_database_connection():
    """Test if the database API is available"""
    print("🧪 Testing Database Connection")
    print("=" * 40)
    
    try:
        response = requests.get("http://localhost:5000/api/property", timeout=5)
        if response.status_code == 200:
            properties = response.json()
            print(f"✅ Database API is available with {len(properties)} properties")
            return True
        else:
            print(f"❌ Database API returned status {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Cannot connect to database API: {e}")
        return False

def test_scraper_endpoint():
    """Test if the scraper endpoint is available"""
    print("\n🧪 Testing Scraper Endpoint")
    print("=" * 40)
    
    try:
        response = requests.get("http://localhost:5001/api/initiate-scrape", timeout=5)
        print(f"✅ Scraper endpoint is available (status: {response.status_code})")
        return True
    except requests.exceptions.RequestException as e:
        print(f"❌ Cannot connect to scraper endpoint: {e}")
        return False

def test_automated_flow():
    """Test the complete automated flow"""
    print("\n🚀 Testing Automated Scraper -> Database Flow")
    print("=" * 50)
    
    # Check if both services are running
    db_available = test_database_connection()
    scraper_available = test_scraper_endpoint()
    
    if not db_available:
        print("❌ Database API not available. Please start the .NET backend first.")
        return False
    
    if not scraper_available:
        print("❌ Scraper endpoint not available. Please start the Flask scraper service first.")
        return False
    
    print("\n✅ Both services are available!")
    
    # Get initial property count
    try:
        response = requests.get("http://localhost:5000/api/property", timeout=5)
        initial_count = len(response.json())
        print(f"📊 Initial property count: {initial_count}")
    except:
        print("❌ Could not get initial property count")
        return False
    
    # Test the scraper endpoint
    print("\n🔄 Testing scraper endpoint...")
    try:
        response = requests.post("http://localhost:5001/api/initiate-scrape", timeout=5)
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Scraper initiated: {result.get('message', 'Unknown')}")
        else:
            print(f"❌ Scraper initiation failed: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Error initiating scraper: {e}")
        return False
    
    # Wait for scraping to complete
    print("\n⏳ Waiting for scraping to complete...")
    print("   (This may take a few minutes)")
    
    # Check for completion by monitoring the log file
    log_file = "scraper_run.log"
    max_wait = 300  # 5 minutes
    start_time = time.time()
    
    while time.time() - start_time < max_wait:
        if os.path.exists(log_file):
            with open(log_file, 'r') as f:
                content = f.read()
                if "Scraping and database transfer completed successfully!" in content:
                    print("✅ Scraping completed successfully!")
                    break
                elif "Error" in content and "Scraping completed" not in content:
                    print("❌ Scraping failed")
                    return False
        
        time.sleep(10)  # Check every 10 seconds
        print("   ⏳ Still waiting...")
    else:
        print("⚠️ Scraping took longer than expected")
    
    # Check final property count
    try:
        response = requests.get("http://localhost:5000/api/property", timeout=5)
        final_count = len(response.json())
        print(f"📊 Final property count: {final_count}")
        
        if final_count > initial_count:
            print(f"🎉 SUCCESS! {final_count - initial_count} new properties added!")
            return True
        else:
            print("⚠️ No new properties were added")
            return False
    except:
        print("❌ Could not get final property count")
        return False

def main():
    """Main test function"""
    print("🧪 Automated Flow Test Suite")
    print("=" * 50)
    
    # Change to project root
    project_root = Path(__file__).parent.parent.parent
    os.chdir(project_root)
    print(f"📁 Working directory: {os.getcwd()}")
    
    print("\nThis test will verify that:")
    print("1. Database API is running (port 5000)")
    print("2. Scraper endpoint is running (port 5001)")
    print("3. Scraping automatically transfers data to database")
    print("\nMake sure both services are running before continuing.")
    
    response = input("\nContinue with test? (y/n): ")
    if response.lower() != 'y':
        print("Test cancelled.")
        return
    
    success = test_automated_flow()
    
    if success:
        print("\n🎉 Automated flow test PASSED!")
        print("✅ Scraper -> Database connection is working!")
    else:
        print("\n❌ Automated flow test FAILED!")
        print("💡 Check that both services are running:")
        print("   - .NET backend on port 5000")
        print("   - Flask scraper service on port 5001")

if __name__ == "__main__":
    main()
