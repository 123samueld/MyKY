#!/usr/bin/env python3
"""
Test script to verify scraper progress tracking and frequent saving
"""
import os
import json
import time
import sys
from pathlib import Path

# Add ScrapeSystem to path so we can import the scraper
sys.path.append(str(Path(__file__).parent.parent.parent / "ScrapeSystem"))

def test_progress_tracking():
    """Test that progress tracking works correctly"""
    print("🧪 Testing Scraper Progress Tracking")
    print("=" * 40)
    
    # Check if progress file exists
    progress_file = "ScrapedDataCache/landsearch_progress.json"
    cache_file = "ScrapedDataCache/landsearch_scrape_cache.json"
    
    print(f"📁 Progress file: {progress_file}")
    print(f"📁 Cache file: {cache_file}")
    
    # Test 1: Check if progress file is created
    if os.path.exists(progress_file):
        with open(progress_file, 'r') as f:
            progress_data = json.load(f)
        print(f"✅ Progress file exists: {progress_data}")
    else:
        print("ℹ️ No progress file found (scraper hasn't started yet)")
    
    # Test 2: Check cache file
    if os.path.exists(cache_file):
        with open(cache_file, 'r') as f:
            cache_data = json.load(f)
        print(f"✅ Cache file exists with {len(cache_data)} properties")
        
        # Show sample data
        if cache_data:
            sample = cache_data[0]
            print(f"📋 Sample property: {sample.get('price', 'N/A')} - {sample.get('full_address', 'N/A')}")
    else:
        print("ℹ️ No cache file found (scraper hasn't started yet)")
    
    # Test 3: Check for image cache
    image_cache_dir = "ScrapedDataCache/ImageCache"
    if os.path.exists(image_cache_dir):
        image_dirs = [d for d in os.listdir(image_cache_dir) if os.path.isdir(os.path.join(image_cache_dir, d))]
        print(f"✅ Image cache exists with {len(image_dirs)} property image folders")
        
        # Show image counts
        for img_dir in image_dirs[:3]:  # Show first 3
            img_path = os.path.join(image_cache_dir, img_dir)
            images = [f for f in os.listdir(img_path) if f.endswith('.jpg')]
            print(f"   📸 Property {img_dir}: {len(images)} images")
    else:
        print("ℹ️ No image cache found")
    
    print("\n🎯 Progress Tracking Test Complete!")

def test_scraper_functions():
    """Test the scraper functions directly"""
    print("\n🧪 Testing Scraper Functions")
    print("=" * 40)
    
    try:
        from SiteScrapers.landsearch_scraper import (
            load_landsearch_cache, 
            save_landsearch_cache,
            load_progress,
            save_progress,
            clear_landsearch_cache
        )
        
        # Test cache functions
        print("📋 Testing cache functions...")
        cache_data = load_landsearch_cache()
        print(f"✅ Loaded cache: {len(cache_data)} properties")
        
        # Test progress functions
        print("📊 Testing progress functions...")
        current_progress = load_progress()
        print(f"✅ Current progress: page {current_progress}")
        
        # Test saving progress
        test_page = 5
        save_progress(test_page)
        saved_progress = load_progress()
        print(f"✅ Saved and loaded progress: {saved_progress}")
        
        # Test cache saving
        if cache_data:
            save_landsearch_cache(cache_data)
            print("✅ Cache save test successful")
        
        print("🎯 Scraper Functions Test Complete!")
        
    except ImportError as e:
        print(f"❌ Could not import scraper functions: {e}")
        print("💡 Make sure you're running from the project root directory")

def monitor_scraper_progress():
    """Monitor scraper progress in real-time"""
    print("\n👀 Monitoring Scraper Progress")
    print("=" * 40)
    print("This will monitor the scraper files for changes...")
    print("Press Ctrl+C to stop monitoring")
    
    progress_file = "ScrapedDataCache/landsearch_progress.json"
    cache_file = "ScrapedDataCache/landsearch_scrape_cache.json"
    
    last_cache_size = 0
    last_progress = None
    
    try:
        while True:
            # Check cache file
            if os.path.exists(cache_file):
                with open(cache_file, 'r') as f:
                    cache_data = json.load(f)
                current_cache_size = len(cache_data)
                
                if current_cache_size != last_cache_size:
                    print(f"📈 Cache updated: {current_cache_size} properties")
                    last_cache_size = current_cache_size
                    
                    # Show latest property
                    if cache_data:
                        latest = cache_data[-1]
                        print(f"   🏠 Latest: {latest.get('price', 'N/A')} - {latest.get('full_address', 'N/A')}")
            
            # Check progress file
            if os.path.exists(progress_file):
                with open(progress_file, 'r') as f:
                    progress_data = json.load(f)
                current_progress = progress_data.get('current_page', 1)
                
                if current_progress != last_progress:
                    print(f"📊 Progress updated: page {current_progress}")
                    last_progress = current_progress
            
            time.sleep(2)  # Check every 2 seconds
            
    except KeyboardInterrupt:
        print("\n🛑 Monitoring stopped")

def main():
    """Main test function"""
    print("🚀 Scraper Progress Testing Suite")
    print("=" * 50)
    
    # Change to project root
    project_root = Path(__file__).parent.parent.parent
    os.chdir(project_root)
    print(f"📁 Working directory: {os.getcwd()}")
    
    # Run tests
    test_progress_tracking()
    test_scraper_functions()
    
    # Ask if user wants to monitor
    print("\n" + "=" * 50)
    response = input("Would you like to monitor scraper progress in real-time? (y/n): ")
    if response.lower() == 'y':
        monitor_scraper_progress()
    
    print("\n✅ All tests complete!")

if __name__ == "__main__":
    main()
