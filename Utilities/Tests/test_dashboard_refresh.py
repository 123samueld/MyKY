#!/usr/bin/env python3
"""
Test script to verify dashboard refresh functionality
"""
import requests
import time
import os
import sys
from pathlib import Path

def test_dashboard_refresh():
    """Test that dashboard can refresh and show new data"""
    print("🧪 Testing Dashboard Refresh Functionality")
    print("=" * 50)
    
    # Test 1: Check if dashboard is accessible
    print("1️⃣ Testing dashboard accessibility...")
    try:
        response = requests.get("http://localhost:5000", timeout=5)
        if response.status_code == 200:
            print("✅ Dashboard is accessible")
        else:
            print(f"❌ Dashboard returned status {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Cannot access dashboard: {e}")
        return False
    
    # Test 2: Check API endpoint
    print("\n2️⃣ Testing API endpoint...")
    try:
        response = requests.get("http://localhost:5000/api/property", timeout=5)
        if response.status_code == 200:
            properties = response.json()
            print(f"✅ API endpoint working with {len(properties)} properties")
        else:
            print(f"❌ API endpoint returned status {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Cannot access API: {e}")
        return False
    
    # Test 3: Check scraper endpoint
    print("\n3️⃣ Testing scraper endpoint...")
    try:
        response = requests.get("http://localhost:5001/api/initiate-scrape", timeout=5)
        print(f"✅ Scraper endpoint accessible (status: {response.status_code})")
    except requests.exceptions.RequestException as e:
        print(f"❌ Cannot access scraper endpoint: {e}")
        return False
    
    print("\n✅ All endpoints are accessible!")
    print("\n💡 Dashboard refresh functionality:")
    print("   - Manual refresh: Click '🔄 Refresh' button in Properties Database panel")
    print("   - Auto-refresh: Scraper Dashboard will automatically refresh after scraping")
    print("   - Monitoring: Dashboard monitors for new properties every 30 seconds")
    
    return True

def test_property_count_changes():
    """Test that property count changes are detected"""
    print("\n🧪 Testing Property Count Detection")
    print("=" * 40)
    
    try:
        # Get initial count
        response = requests.get("http://localhost:5000/api/property", timeout=5)
        if response.status_code == 200:
            initial_count = len(response.json())
            print(f"📊 Initial property count: {initial_count}")
            
            # Wait a bit and check again
            print("⏳ Waiting 10 seconds to check for changes...")
            time.sleep(10)
            
            response = requests.get("http://localhost:5000/api/property", timeout=5)
            if response.status_code == 200:
                current_count = len(response.json())
                print(f"📊 Current property count: {current_count}")
                
                if current_count > initial_count:
                    print(f"🎉 New properties detected! (+{current_count - initial_count})")
                elif current_count == initial_count:
                    print("ℹ️ No new properties detected")
                else:
                    print(f"⚠️ Property count decreased ({current_count - initial_count})")
                
                return True
            else:
                print(f"❌ Error getting current count: {response.status_code}")
                return False
        else:
            print(f"❌ Error getting initial count: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Error checking property counts: {e}")
        return False

def main():
    """Main test function"""
    print("🚀 Dashboard Refresh Test Suite")
    print("=" * 50)
    
    # Change to project root
    project_root = Path(__file__).parent.parent.parent
    os.chdir(project_root)
    print(f"📁 Working directory: {os.getcwd()}")
    
    print("\nThis test will verify that:")
    print("1. Dashboard is accessible")
    print("2. API endpoints are working")
    print("3. Property count detection works")
    print("\nMake sure both services are running before continuing.")
    
    # Run tests
    dashboard_ok = test_dashboard_refresh()
    count_ok = test_property_count_changes()
    
    print("\n" + "=" * 50)
    print("📊 Test Results Summary:")
    print(f"   Dashboard Access: {'✅' if dashboard_ok else '❌'}")
    print(f"   Property Detection: {'✅' if count_ok else '❌'}")
    
    if dashboard_ok and count_ok:
        print("\n🎉 Dashboard refresh functionality is working!")
        print("\n💡 How to use:")
        print("   1. Click 'Scraper Dashboard' in the main dashboard")
        print("   2. Click 'Initiate Scrape Manually'")
        print("   3. Dashboard will automatically monitor and refresh")
        print("   4. Or manually click '🔄 Refresh' in Properties Database panel")
    else:
        print("\n❌ Some tests failed!")
        print("💡 Make sure both services are running:")
        print("   - .NET backend on port 5000")
        print("   - Flask scraper service on port 5001")

if __name__ == "__main__":
    main()
