#!/usr/bin/env python3
"""
Test script to verify cache paths are working correctly
"""
import os
import json
import sys
from pathlib import Path

# Add ScrapeSystem to path
sys.path.append(str(Path(__file__).parent.parent.parent / "ScrapeSystem"))

def test_cache_paths():
    """Test that cache paths are correctly configured"""
    print("🧪 Testing Cache Paths")
    print("=" * 40)
    
    try:
        from SiteScrapers.landsearch_scraper import (
            LANDSEARCH_CACHE_DIR,
            LANDSEARCH_CACHE_FILE,
            PROGRESS_FILE
        )
        
        print(f"📁 Cache directory: {LANDSEARCH_CACHE_DIR}")
        print(f"📁 Cache file: {LANDSEARCH_CACHE_FILE}")
        print(f"📁 Progress file: {PROGRESS_FILE}")
        
        # Check if paths exist
        cache_dir_exists = os.path.exists(LANDSEARCH_CACHE_DIR)
        cache_file_exists = os.path.exists(LANDSEARCH_CACHE_FILE)
        progress_file_exists = os.path.exists(PROGRESS_FILE)
        
        print(f"\n📊 Path Status:")
        print(f"   Cache directory exists: {'✅' if cache_dir_exists else '❌'}")
        print(f"   Cache file exists: {'✅' if cache_file_exists else '❌'}")
        print(f"   Progress file exists: {'✅' if progress_file_exists else '❌'}")
        
        if cache_file_exists:
            with open(LANDSEARCH_CACHE_FILE, 'r') as f:
                data = json.load(f)
            print(f"   Cache file contains: {len(data)} properties")
            if data:
                print(f"   Sample property: {data[0].get('address', 'N/A')}")
        
        return cache_dir_exists
        
    except Exception as e:
        print(f"❌ Error testing cache paths: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_post_to_database_paths():
    """Test that post_to_database.py can find the cache file"""
    print("\n🧪 Testing post_to_database.py Paths")
    print("=" * 40)
    
    try:
        from post_to_database import CACHE_FILE, load_scraped_data
        
        print(f"📁 post_to_database.py looking for: {CACHE_FILE}")
        
        cache_exists = os.path.exists(CACHE_FILE)
        print(f"   Cache file exists: {'✅' if cache_exists else '❌'}")
        
        if cache_exists:
            data = load_scraped_data()
            print(f"   Loaded {len(data)} properties from cache")
            if data:
                print(f"   Sample property: {data[0].get('address', 'N/A')}")
            return True
        else:
            print("   ❌ Cache file not found by post_to_database.py")
            return False
            
    except Exception as e:
        print(f"❌ Error testing post_to_database paths: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_filepath_compendium():
    """Test that FilePathCompendium.json is being read correctly"""
    print("\n🧪 Testing FilePathCompendium.json")
    print("=" * 40)
    
    try:
        # Load FilePathCompendium.json
        project_root = Path(__file__).parent.parent.parent
        config_file = project_root / "Utilities" / "FilePathCompendium.json"
        
        with open(config_file, 'r') as f:
            config = json.load(f)
        
        scraper_cache_dir = config.get('scraperCacheDirectory', './ScrapeSystem/ScrapedDataCache/')
        print(f"📁 scraperCacheDirectory: {scraper_cache_dir}")
        
        # Convert to absolute path
        if scraper_cache_dir.startswith('./'):
            abs_path = str(project_root / scraper_cache_dir[2:])
        else:
            abs_path = scraper_cache_dir
        
        print(f"📁 Absolute path: {abs_path}")
        print(f"📁 Path exists: {'✅' if os.path.exists(abs_path) else '❌'}")
        
        return os.path.exists(abs_path)
        
    except Exception as e:
        print(f"❌ Error testing FilePathCompendium: {e}")
        return False

def main():
    """Main test function"""
    print("🚀 Cache Paths Test Suite")
    print("=" * 50)
    
    # Change to project root
    project_root = Path(__file__).parent.parent.parent
    os.chdir(project_root)
    print(f"📁 Working directory: {os.getcwd()}")
    
    # Run tests
    scraper_paths_ok = test_cache_paths()
    post_db_paths_ok = test_post_to_database_paths()
    compendium_ok = test_filepath_compendium()
    
    print("\n" + "=" * 50)
    print("📊 Test Results Summary:")
    print(f"   Scraper Cache Paths: {'✅' if scraper_paths_ok else '❌'}")
    print(f"   post_to_database Paths: {'✅' if post_db_paths_ok else '❌'}")
    print(f"   FilePathCompendium: {'✅' if compendium_ok else '❌'}")
    
    if all([scraper_paths_ok, post_db_paths_ok, compendium_ok]):
        print("\n🎉 All cache paths are working correctly!")
        print("✅ Scraper and database transfer should work properly now")
    else:
        print("\n❌ Some cache path issues found!")
        print("💡 Check the FilePathCompendium.json configuration")

if __name__ == "__main__":
    main()
