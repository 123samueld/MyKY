import os
import json
import importlib
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from config import config

# List of site scraper module names (strings) in SiteScrapers/
SITE_SCRAPERS = ["zillow_scraper"]  # Site scraper filenames (without .py extension)

def setup_selenium():
    """Set up Selenium WebDriver with ChromeDriver in visible (non-headless) mode."""
    chrome_options = Options()
    # Visible window per request; comment out headless
    # chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")  # Required for Ubuntu
    chrome_options.add_argument("--disable-dev-shm-usage")  # Avoid shared memory issues
    service = Service(config.chromedriver_path)  # Use ChromeDriver path from config
    driver = webdriver.Chrome(service=service, options=chrome_options)
    try:
        driver.maximize_window()
    except Exception:
        pass
    return driver

def load_scraper_module(scraper_name):
    """Dynamically import a site scraper module from SiteScrapers/."""
    try:
        module = importlib.import_module(f"SiteScrapers.{scraper_name}")
        return module
    except ImportError as e:
        print(f"Error importing {scraper_name}: {e}")
        return None

def save_to_json(data, file_path=config.scraped_data_cache):
    """Append scraped data to JSON file."""
    try:
        # Read existing data or initialize empty list
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                existing_data = json.load(f)
        else:
            existing_data = []
        
        # Append new data (list of dicts)
        existing_data.extend(data)
        
        # Write back to file
        with open(file_path, 'w') as f:
            json.dump(existing_data, f, indent=2)
        print(f"Saved {len(data)} records to {file_path}")
    except Exception as e:
        print(f"Error saving to JSON: {e}")

def scrapeSelectedSites():
    """Orchestrate scraping across all site scrapers."""
    print("Scraping sites")
    print(f"Using ChromeDriver at: {config.chromedriver_path}")
    
    # Set up Selenium WebDriver
    driver = setup_selenium()
    
    # Ensure cache directory exists
    cache_dir = os.path.dirname(config.scraped_data_cache)
    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir)
    
    # Iterate through site scrapers
    all_data = []
    for scraper_name in SITE_SCRAPERS:
        print(f"Running scraper: {scraper_name}")
        scraper_module = load_scraper_module(scraper_name)
        if scraper_module:
            try:
                # Assume each scraper has a scrape_site(driver) function returning list of dicts
                site_data = scraper_module.scrape_site(driver)
                if site_data:
                    all_data.extend(site_data)
                    print(f"Scraped {len(site_data)} records from {scraper_name}")
            except Exception as e:
                print(f"Error in {scraper_name}: {e}")
    
    # Save all scraped data to JSON
    if all_data:
        save_to_json(all_data)
    
    # Clean up
    driver.quit()

def main():
    print("Scraper Central Nexus called")
    print(f"Project root: {config.project_root}")
    print(f"ChromeDriver path: {config.chromedriver_path}")
    print(f"Data cache: {config.scraped_data_cache}")
    
    # Run the scraping process
    scrapeSelectedSites()

if __name__ == "__main__":
    main()