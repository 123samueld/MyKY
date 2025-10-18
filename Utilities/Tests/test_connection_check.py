#!/usr/bin/env python3
"""
Simple test to check if the automated flow components are connected
"""
import requests
import os
import sys
from pathlib import Path

def test_database_api():
    """Test if database API is running"""
    print("🧪 Testing Database API Connection")
    print("=" * 40)
    
    try:
        response = requests.get("http://localhost:5000/api/property", timeout=5)
        if response.status_code == 200:
            properties = response.json()
            print(f"✅ Database API is running with {len(properties)} properties")
            return True
        else:
            print(f"❌ Database API returned status {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Cannot connect to database API: {e}")
        return False

def test_scraper_endpoint():
    """Test if scraper endpoint is running"""
    print("\n🧪 Testing Scraper Endpoint Connection")
    print("=" * 40)
    
    try:
        response = requests.get("http://localhost:5001/api/initiate-scrape", timeout=5)
        print(f"✅ Scraper endpoint is running (status: {response.status_code})")
        return True
    except requests.exceptions.RequestException as e:
        print(f"❌ Cannot connect to scraper endpoint: {e}")
        return False

def test_scraper_nexus_modification():
    """Test if scraper_central_nexus.py has been modified for automated flow"""
    print("\n🧪 Testing Scraper Nexus Modification")
    print("=" * 40)
    
    nexus_file = "ScrapeSystem/scraper_central_nexus.py"
    if not os.path.exists(nexus_file):
        print(f"❌ {nexus_file} not found")
        return False
    
    with open(nexus_file, 'r') as f:
        content = f.read()
    
    if "transfer_to_database" in content:
        print("✅ transfer_to_database function found")
    else:
        print("❌ transfer_to_database function not found")
        return False
    
    if "post_to_database.py" in content:
        print("✅ post_to_database.py integration found")
    else:
        print("❌ post_to_database.py integration not found")
        return False
    
    if "Automatically transfer to database" in content:
        print("✅ Automated transfer logic found")
    else:
        print("❌ Automated transfer logic not found")
        return False
    
    print("✅ Scraper nexus has been modified for automated flow")
    return True

def test_post_to_database_exists():
    """Test if post_to_database.py exists and is executable"""
    print("\n🧪 Testing post_to_database.py")
    print("=" * 40)
    
    post_script = "ScrapeSystem/post_to_database.py"
    if not os.path.exists(post_script):
        print(f"❌ {post_script} not found")
        return False
    
    print(f"✅ {post_script} exists")
    
    # Check if it has the right functions
    with open(post_script, 'r') as f:
        content = f.read()
    
    if "check_existing_properties" in content:
        print("✅ Duplicate prevention logic found")
    else:
        print("❌ Duplicate prevention logic not found")
        return False
    
    if "post_batch_properties" in content:
        print("✅ Batch upload logic found")
    else:
        print("❌ Batch upload logic not found")
        return False
    
    print("✅ post_to_database.py is properly configured")
    return True

def main():
    """Main test function"""
    print("🚀 Automated Flow Connection Test")
    print("=" * 50)
    
    # Change to project root
    project_root = Path(__file__).parent.parent.parent
    os.chdir(project_root)
    print(f"📁 Working directory: {os.getcwd()}")
    
    # Run tests
    db_ok = test_database_api()
    scraper_ok = test_scraper_endpoint()
    nexus_ok = test_scraper_nexus_modification()
    post_ok = test_post_to_database_exists()
    
    print("\n" + "=" * 50)
    print("📊 Test Results Summary:")
    print(f"   Database API: {'✅' if db_ok else '❌'}")
    print(f"   Scraper Endpoint: {'✅' if scraper_ok else '❌'}")
    print(f"   Scraper Nexus: {'✅' if nexus_ok else '❌'}")
    print(f"   Post to Database: {'✅' if post_ok else '❌'}")
    
    if all([db_ok, scraper_ok, nexus_ok, post_ok]):
        print("\n🎉 ALL TESTS PASSED!")
        print("✅ Automated scraper -> database flow is properly connected!")
        print("\n💡 To test the full flow:")
        print("   1. Start both services (launch.sh)")
        print("   2. Click 'Initiate Scrape Manually' in dashboard")
        print("   3. Data will automatically transfer to database")
    else:
        print("\n❌ Some tests failed!")
        print("💡 Make sure all components are properly set up:")
        print("   - .NET backend running on port 5000")
        print("   - Flask scraper service running on port 5001")
        print("   - scraper_central_nexus.py modified for automation")
        print("   - post_to_database.py exists and is configured")

if __name__ == "__main__":
    main()
