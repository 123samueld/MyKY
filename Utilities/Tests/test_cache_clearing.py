#!/usr/bin/env python3
"""
Test script to verify cache clearing functionality
"""
import os
import json
import shutil
import sys
from pathlib import Path

# Add ScrapeSystem to path
sys.path.append(str(Path(__file__).parent.parent.parent / "ScrapeSystem"))

def test_cache_clearing():
    """Test that cache clearing works for both JSON and ImageCache"""
    print("🧪 Testing Cache Clearing Functionality")
    print("=" * 50)
    
    # Create test cache structure
    cache_dir = "ScrapedDataCache"
    cache_file = os.path.join(cache_dir, "landsearch_scrape_cache.json")
    progress_file = os.path.join(cache_dir, "landsearch_progress.json")
    image_cache_dir = os.path.join(cache_dir, "ImageCache")
    
    print("1️⃣ Creating test cache structure...")
    
    # Create directories
    os.makedirs(cache_dir, exist_ok=True)
    os.makedirs(image_cache_dir, exist_ok=True)
    
    # Create test JSON cache
    test_data = [
        {"temp_ID": 1, "site": "landsearch", "address": "Test Property 1", "price": "$100,000"},
        {"temp_ID": 2, "site": "landsearch", "address": "Test Property 2", "price": "$200,000"}
    ]
    with open(cache_file, 'w') as f:
        json.dump(test_data, f, indent=2)
    print(f"✅ Created test cache file: {cache_file}")
    
    # Create test progress file
    with open(progress_file, 'w') as f:
        json.dump({"current_page": 3}, f)
    print(f"✅ Created test progress file: {progress_file}")
    
    # Create test image directories and files
    for i in range(1, 4):
        prop_dir = os.path.join(image_cache_dir, str(i))
        os.makedirs(prop_dir, exist_ok=True)
        
        # Create dummy image files
        for j in range(1, 3):
            img_file = os.path.join(prop_dir, f"{i}_{j}.jpg")
            with open(img_file, 'w') as f:
                f.write("dummy image data")
        print(f"✅ Created test images in: {prop_dir}")
    
    print(f"\n📁 Test structure created:")
    print(f"   - Cache file: {os.path.exists(cache_file)}")
    print(f"   - Progress file: {os.path.exists(progress_file)}")
    print(f"   - Image cache dir: {os.path.exists(image_cache_dir)}")
    print(f"   - Image subdirs: {len([d for d in os.listdir(image_cache_dir) if os.path.isdir(os.path.join(image_cache_dir, d))])}")
    
    # Test the clear function
    print("\n2️⃣ Testing clear_landsearch_cache() function...")
    
    try:
        from SiteScrapers.landsearch_scraper import clear_landsearch_cache
        clear_landsearch_cache()
        
        # Check if everything was cleared
        print("\n3️⃣ Verifying cache was cleared...")
        
        cache_cleared = not os.path.exists(cache_file)
        progress_cleared = not os.path.exists(progress_file)
        image_cache_cleared = not os.path.exists(image_cache_dir)
        
        print(f"   - Cache file cleared: {'✅' if cache_cleared else '❌'}")
        print(f"   - Progress file cleared: {'✅' if progress_cleared else '❌'}")
        print(f"   - Image cache cleared: {'✅' if image_cache_cleared else '❌'}")
        
        if cache_cleared and progress_cleared and image_cache_cleared:
            print("\n🎉 Cache clearing test PASSED!")
            return True
        else:
            print("\n❌ Cache clearing test FAILED!")
            return False
            
    except Exception as e:
        print(f"❌ Error testing cache clearing: {e}")
        return False

def test_scraper_fresh_start():
    """Test that scraper starts fresh after clearing"""
    print("\n🧪 Testing Fresh Start Functionality")
    print("=" * 40)
    
    try:
        from SiteScrapers.landsearch_scraper import load_landsearch_cache, load_progress
        
        # Test loading cache after clearing
        cache_data = load_landsearch_cache()
        progress = load_progress()
        
        print(f"📊 Cache data after clearing: {len(cache_data)} properties")
        print(f"📊 Progress after clearing: page {progress}")
        
        if len(cache_data) == 0 and progress == 1:
            print("✅ Fresh start test PASSED!")
            return True
        else:
            print("❌ Fresh start test FAILED!")
            return False
            
    except Exception as e:
        print(f"❌ Error testing fresh start: {e}")
        return False

def main():
    """Main test function"""
    print("🚀 Cache Clearing Test Suite")
    print("=" * 50)
    
    # Change to project root
    project_root = Path(__file__).parent.parent.parent
    os.chdir(project_root)
    print(f"📁 Working directory: {os.getcwd()}")
    
    # Run tests
    clearing_ok = test_cache_clearing()
    fresh_start_ok = test_scraper_fresh_start()
    
    print("\n" + "=" * 50)
    print("📊 Test Results Summary:")
    print(f"   Cache Clearing: {'✅' if clearing_ok else '❌'}")
    print(f"   Fresh Start: {'✅' if fresh_start_ok else '❌'}")
    
    if clearing_ok and fresh_start_ok:
        print("\n🎉 All cache clearing tests PASSED!")
        print("✅ Scraper will now clear both JSON and ImageCache on each new session")
    else:
        print("\n❌ Some tests failed!")
        print("💡 Check the cache clearing implementation")

if __name__ == "__main__":
    main()
