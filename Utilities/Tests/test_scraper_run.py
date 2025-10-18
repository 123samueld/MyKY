#!/usr/bin/env python3
"""
Test script to run the scraper and verify progress tracking works
"""
import os
import sys
import time
from pathlib import Path

# Add ScrapeSystem to path
sys.path.append(str(Path(__file__).parent.parent.parent / "ScrapeSystem"))

def test_scraper_run():
    """Test running the scraper with progress tracking"""
    print("🚀 Testing Scraper Run with Progress Tracking")
    print("=" * 50)
    
    try:
        from SiteScrapers.landsearch_scraper import scrape_site
        from playwright.sync_api import sync_playwright
        
        print("📋 Starting scraper test...")
        print("⚠️  This will open a browser and scrape real data")
        print("⚠️  It will stop after 3 properties as configured")
        
        # Run the scraper
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)  # Set to True for headless
            page = browser.new_page()
            
            try:
                scraped_data = scrape_site(page)
                print(f"✅ Scraper completed! Found {len(scraped_data)} properties")
                
                # Verify progress was saved
                progress_file = "ScrapedDataCache/landsearch_progress.json"
                cache_file = "ScrapedDataCache/landsearch_scrape_cache.json"
                
                if os.path.exists(cache_file):
                    print("✅ Cache file was created/updated")
                else:
                    print("❌ Cache file was not created")
                
                if os.path.exists(progress_file):
                    print("⚠️ Progress file still exists (scraper may not have completed)")
                else:
                    print("✅ Progress file was cleaned up (scraper completed)")
                
            finally:
                browser.close()
                
    except Exception as e:
        print(f"❌ Scraper test failed: {e}")
        import traceback
        traceback.print_exc()

def test_scraper_functions_only():
    """Test just the scraper functions without running the full scraper"""
    print("🧪 Testing Scraper Functions Only")
    print("=" * 40)
    
    try:
        from SiteScrapers.landsearch_scraper import (
            load_landsearch_cache,
            save_landsearch_cache,
            load_progress,
            save_progress,
            clear_landsearch_cache
        )
        
        # Test clearing cache
        print("🗑️ Testing cache clearing...")
        clear_landsearch_cache()
        
        # Test progress tracking
        print("📊 Testing progress tracking...")
        save_progress(1)
        assert load_progress() == 1
        print("✅ Progress save/load works")
        
        save_progress(5)
        assert load_progress() == 5
        print("✅ Progress update works")
        
        # Test cache operations
        print("💾 Testing cache operations...")
        test_data = [{"test": "data", "id": 1}]
        save_landsearch_cache(test_data)
        
        loaded_data = load_landsearch_cache()
        assert len(loaded_data) == 1
        print("✅ Cache save/load works")
        
        print("🎯 All function tests passed!")
        
    except Exception as e:
        print(f"❌ Function test failed: {e}")
        import traceback
        traceback.print_exc()

def main():
    """Main test function"""
    print("🧪 Scraper Progress Test Suite")
    print("=" * 50)
    
    # Change to project root
    project_root = Path(__file__).parent.parent.parent
    os.chdir(project_root)
    print(f"📁 Working directory: {os.getcwd()}")
    
    print("\nChoose test type:")
    print("1. Test scraper functions only (safe, no browser)")
    print("2. Test full scraper run (opens browser, scrapes real data)")
    print("3. Just check existing progress files")
    
    choice = input("\nEnter choice (1-3): ").strip()
    
    if choice == "1":
        test_scraper_functions_only()
    elif choice == "2":
        test_scraper_run()
    elif choice == "3":
        # Just check existing files
        import json
        progress_file = "ScrapedDataCache/landsearch_progress.json"
        cache_file = "ScrapedDataCache/landsearch_scrape_cache.json"
        
        if os.path.exists(progress_file):
            with open(progress_file, 'r') as f:
                progress = json.load(f)
            print(f"📊 Current progress: {progress}")
        else:
            print("ℹ️ No progress file found")
            
        if os.path.exists(cache_file):
            with open(cache_file, 'r') as f:
                cache = json.load(f)
            print(f"💾 Cache has {len(cache)} properties")
        else:
            print("ℹ️ No cache file found")
    else:
        print("❌ Invalid choice")

if __name__ == "__main__":
    main()
