#!/usr/bin/env python3

"""
Test script to verify ScrapeSystem configuration is working correctly
"""

from config import config
import os

def test_config():
    print("=== ScrapeSystem Configuration Test ===")
    print()
    
    print(f"Root Path: {config.root_path}")
    print(f"Project Root: {config.project_root}")
    print(f"Utilities Dir: {config.utilities_dir}")
    print(f"Scraped Data Cache: {config.scraped_data_cache}")
    print(f"ChromeDriver Path: {config.chromedriver_path}")
    print()
    
    # Test if key directories exist
    print("Testing key paths:")
    
    # Test project root
    if os.path.exists(config.project_root):
        print(f"✅ Project root exists: {config.project_root}")
    else:
        print(f"❌ Project root missing: {config.project_root}")
    
    # Test utilities directory
    if os.path.exists(config.utilities_dir):
        print(f"✅ Utilities directory exists: {config.utilities_dir}")
    else:
        print(f"❌ Utilities directory missing: {config.utilities_dir}")
    
    # Test ChromeDriver
    if os.path.exists(config.chromedriver_path):
        print(f"✅ ChromeDriver exists: {config.chromedriver_path}")
        if os.access(config.chromedriver_path, os.X_OK):
            print(f"✅ ChromeDriver is executable")
        else:
            print(f"⚠️  (Expected) ChromeDriver exists but is not executable")
    else:
        print(f"❌ ChromeDriver missing: {config.chromedriver_path}")
    
    # Test scraped data cache directory
    if os.path.exists(config.scraped_data_cache):
        print(f"✅ Scraped data cache exists: {config.scraped_data_cache}")
    else:
        print(f"⚠️  (Expected) Scraped data cache directory missing (will be created when needed): {config.scraped_data_cache}")
    
    print()
    print("=== Test Complete ===")

if __name__ == "__main__":
    test_config()
