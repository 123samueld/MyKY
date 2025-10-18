#!/usr/bin/env python3
"""
Quick test to verify scraper progress tracking works
"""
import os
import sys
import json
from pathlib import Path

# Add ScrapeSystem to path
sys.path.append(str(Path(__file__).parent.parent.parent / "ScrapeSystem"))

def test_progress_files():
    """Test that progress files are created and updated correctly"""
    print("🧪 Testing Scraper Progress Files")
    print("=" * 40)
    
    progress_file = "ScrapedDataCache/landsearch_progress.json"
    cache_file = "ScrapedDataCache/landsearch_scrape_cache.json"
    
    # Check if files exist
    print(f"📁 Progress file exists: {os.path.exists(progress_file)}")
    print(f"📁 Cache file exists: {os.path.exists(cache_file)}")
    
    if os.path.exists(progress_file):
        with open(progress_file, 'r') as f:
            progress = json.load(f)
        print(f"📊 Current progress: {progress}")
    
    if os.path.exists(cache_file):
        with open(cache_file, 'r') as f:
            cache = json.load(f)
        print(f"💾 Cache has {len(cache)} properties")
        
        if cache:
            print("📋 Sample properties:")
            for i, prop in enumerate(cache[:3]):  # Show first 3
                print(f"   {i+1}. {prop.get('price', 'N/A')} - {prop.get('full_address', 'N/A')}")
    
    # Check image cache
    image_cache = "ScrapedDataCache/ImageCache"
    if os.path.exists(image_cache):
        image_dirs = [d for d in os.listdir(image_cache) if os.path.isdir(os.path.join(image_cache, d))]
        print(f"📸 Image cache has {len(image_dirs)} property folders")
        
        for img_dir in image_dirs[:3]:  # Show first 3
            img_path = os.path.join(image_cache, img_dir)
            images = [f for f in os.listdir(img_path) if f.endswith('.jpg')]
            print(f"   📸 Property {img_dir}: {len(images)} images")

def test_scraper_import():
    """Test that scraper can be imported and functions work"""
    print("\n🧪 Testing Scraper Import")
    print("=" * 40)
    
    try:
        from SiteScrapers.landsearch_scraper import (
            load_landsearch_cache,
            save_landsearch_cache,
            load_progress,
            save_progress,
            clear_landsearch_cache
        )
        print("✅ Scraper functions imported successfully")
        
        # Test basic functions
        cache = load_landsearch_cache()
        print(f"✅ Loaded cache: {len(cache)} properties")
        
        progress = load_progress()
        print(f"✅ Loaded progress: page {progress}")
        
        # Test saving
        save_progress(10)
        new_progress = load_progress()
        print(f"✅ Progress save/load: {new_progress}")
        
        print("🎯 All import tests passed!")
        
    except Exception as e:
        print(f"❌ Import test failed: {e}")
        import traceback
        traceback.print_exc()

def main():
    """Main test function"""
    print("🚀 Quick Scraper Progress Test")
    print("=" * 50)
    
    # Change to project root
    project_root = Path(__file__).parent.parent.parent
    os.chdir(project_root)
    print(f"📁 Working directory: {os.getcwd()}")
    
    test_progress_files()
    test_scraper_import()
    
    print("\n✅ Quick test complete!")
    print("\n💡 To test the actual scraper:")
    print("   python3 Utilities/Tests/test_scraper_run.py")
    print("   (Choose option 2 for full scraper test)")

if __name__ == "__main__":
    main()
