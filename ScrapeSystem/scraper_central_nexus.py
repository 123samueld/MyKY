import os
import json
import importlib
from playwright.sync_api import sync_playwright
from config import config

headlessScraping = False
SITE_SCRAPERS = ["landsearch_scraper"]
#SITE_SCRAPERS = ["zillow_scraper", "landsearch_scraper", "landwatch_scraper"]


class PlaywrightDriver:
    def __init__(self, page):
        self.page = page
    
    def get(self, url):
        self.page.goto(url, wait_until="networkidle")
    
    def find_element(self, by, value):
        if by == "css selector":
            return PlaywrightElement(self.page.locator(value))
        elif by == "xpath":
            return PlaywrightElement(self.page.locator(f"xpath={value}"))
        raise ValueError(f"Unsupported selector: {by}")
    
    def find_elements(self, by, value):
        if by == "css selector":
            return [PlaywrightElement(self.page.locator(value).nth(i)) 
                   for i in range(self.page.locator(value).count())]
        elif by == "xpath":
            return [PlaywrightElement(self.page.locator(f"xpath={value}").nth(i)) 
                   for i in range(self.page.locator(f"xpath={value}").count())]
        raise ValueError(f"Unsupported selector: {by}")
    
    def quit(self):
        pass

class PlaywrightElement:
    def __init__(self, locator):
        self.locator = locator
    
    def click(self):
        self.locator.click()
    
    def send_keys(self, text):
        self.locator.fill(text)
    
    def text(self):
        return self.locator.inner_text()
    
    def get_attribute(self, name):
        return self.locator.get_attribute(name)

def setup_playwright():
    playwright = sync_playwright().start()
    browser = playwright.chromium.launch(
        headless=headlessScraping, 
        args=["--no-sandbox", "--disable-dev-shm-usage"]
    )
    context = browser.new_context(viewport={"width": 1920, "height": 1080})
    page = context.new_page()
    page.set_viewport_size({"width": 1920, "height": 1080})
    driver = PlaywrightDriver(page)
    print("✅ Playwright ready! (Visible browser)")
    return playwright, browser, context, driver

def load_scraper_module(scraper_name):
    try:
        module = importlib.import_module(f"SiteScrapers.{scraper_name}")
        return module
    except ImportError as e:
        print(f"Error importing {scraper_name}: {e}")
        return None

def save_to_json(data, file_path=config.scraped_data_cache):
    try:
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                existing_data = json.load(f)
        else:
            existing_data = []
        existing_data.extend(data)
        with open(file_path, 'w') as f:
            json.dump(existing_data, f, indent=2)
        print(f"Saved {len(data)} records to {file_path}")
    except Exception as e:
        print(f"Error saving to JSON: {e}")

def scrapeSelectedSites(playwright, browser, context, driver):
    print("Scraping sites")
    print(f"Using Playwright (auto-managed browser)")
    
    cache_dir = os.path.dirname(config.scraped_data_cache)
    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir)
    
    all_data = []
    for scraper_name in SITE_SCRAPERS:
        print(f"Running scraper: {scraper_name}")
        scraper_module = load_scraper_module(scraper_name)
        if scraper_module:
            try:
                # ← FIXED: Pass Page directly
                site_data = scraper_module.scrape_site(driver.page)
                if site_data:
                    all_data.extend(site_data)
                    print(f"Scraped {len(site_data)} records from {scraper_name}")
            except Exception as e:
                print(f"Error in {scraper_name}: {e}")
    
    if all_data:
        save_to_json(all_data)
    
    return all_data

def main():
    print("🎯 Scraper Central Nexus (Playwright Edition)")
    print(f"Project root: {config.project_root}")
    print(f"Data cache: {config.scraped_data_cache}")
    print("🚀 No more ChromeDriver paths needed!")
    print("-" * 50)
    
    playwright, browser, context, driver = setup_playwright()
    
    try:
        scrapeSelectedSites(playwright, browser, context, driver)
    finally:
        context.close()
        browser.close()
        playwright.stop()
        print("✅ Browser closed cleanly")

if __name__ == "__main__":
    main()