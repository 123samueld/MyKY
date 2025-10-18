#!/usr/bin/env python3
"""
Debug script to test scraper data saving
"""
import os
import json
import sys
from pathlib import Path

# Add ScrapeSystem to path
sys.path.append(str(Path(__file__).parent.parent.parent / "ScrapeSystem"))

def test_scraper_functions():
    """Test the scraper functions individually"""
    print("🧪 Testing Scraper Functions")
    print("=" * 40)
    
    try:
        from SiteScrapers.landsearch_scraper import (
            clear_landsearch_cache,
            save_landsearch_cache,
            load_landsearch_cache,
            load_progress,
            save_progress
        )
        
        # Test 1: Clear cache
        print("1️⃣ Testing cache clearing...")
        clear_landsearch_cache()
        
        # Test 2: Load cache after clearing
        print("2️⃣ Testing cache loading after clearing...")
        cache_data = load_landsearch_cache()
        print(f"   Cache data: {len(cache_data)} properties")
        
        # Test 3: Save test data
        print("3️⃣ Testing cache saving...")
        test_data = [
            {
                "temp_ID": 1,
                "site": "landsearch",
                "address": "Test Property 1",
                "price": "$100,000",
                "acres": "5 acres",
                "full_address": "123 Test St, Test City, KY",
                "detail_url": "https://test.com/property1"
            }
        ]
        save_landsearch_cache(test_data)
        
        # Test 4: Load cache after saving
        print("4️⃣ Testing cache loading after saving...")
        loaded_data = load_landsearch_cache()
        print(f"   Loaded data: {len(loaded_data)} properties")
        if loaded_data:
            print(f"   Sample property: {loaded_data[0].get('address', 'N/A')}")
        
        # Test 5: Progress functions
        print("5️⃣ Testing progress functions...")
        save_progress(2)
        progress = load_progress()
        print(f"   Progress: page {progress}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing scraper functions: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_cache_file_creation():
    """Test if cache files are being created properly"""
    print("\n🧪 Testing Cache File Creation")
    print("=" * 40)
    
    cache_file = "ScrapedDataCache/landsearch_scrape_cache.json"
    progress_file = "ScrapedDataCache/landsearch_progress.json"
    image_cache_dir = "ScrapedDataCache/ImageCache"
    
    print(f"📁 Cache file exists: {os.path.exists(cache_file)}")
    print(f"📁 Progress file exists: {os.path.exists(progress_file)}")
    print(f"📁 Image cache dir exists: {os.path.exists(image_cache_dir)}")
    
    if os.path.exists(cache_file):
        with open(cache_file, 'r') as f:
            data = json.load(f)
        print(f"📊 Cache file contains: {len(data)} properties")
        if data:
            print(f"   Sample: {data[0].get('address', 'N/A')}")
    
    if os.path.exists(progress_file):
        with open(progress_file, 'r') as f:
            progress = json.load(f)
        print(f"📊 Progress file contains: {progress}")
    
    if os.path.exists(image_cache_dir):
        subdirs = [d for d in os.listdir(image_cache_dir) if os.path.isdir(os.path.join(image_cache_dir, d))]
        print(f"📊 Image cache contains: {len(subdirs)} property directories")
        for subdir in subdirs[:3]:  # Show first 3
            subdir_path = os.path.join(image_cache_dir, subdir)
            images = [f for f in os.listdir(subdir_path) if f.endswith('.jpg')]
            print(f"   Property {subdir}: {len(images)} images")

def test_scraper_import():
    """Test if scraper can be imported and run"""
    print("\n🧪 Testing Scraper Import")
    print("=" * 40)
    
    try:
        from SiteScrapers.landsearch_scraper import scrape_site
        print("✅ scrape_site function imported successfully")
        
        # Check if the function exists and is callable
        if callable(scrape_site):
            print("✅ scrape_site is callable")
        else:
            print("❌ scrape_site is not callable")
            return False
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Main debug function"""
    print("🚀 Scraper Debug Test Suite")
    print("=" * 50)
    
    # Change to project root
    project_root = Path(__file__).parent.parent.parent
    os.chdir(project_root)
    print(f"📁 Working directory: {os.getcwd()}")
    
    # Run tests
    functions_ok = test_scraper_functions()
    cache_ok = test_cache_file_creation()
    import_ok = test_scraper_import()
    
    print("\n" + "=" * 50)
    print("📊 Debug Results Summary:")
    print(f"   Scraper Functions: {'✅' if functions_ok else '❌'}")
    print(f"   Cache Files: {'✅' if cache_ok else '❌'}")
    print(f"   Scraper Import: {'✅' if import_ok else '❌'}")
    
    if all([functions_ok, cache_ok, import_ok]):
        print("\n🎉 All scraper components are working!")
        print("💡 The issue might be in the scraping process itself")
    else:
        print("\n❌ Some components are not working!")
        print("💡 Check the specific failing components above")

if __name__ == "__main__":
    main()
