from config import config

def main():
    print("Scraper Central Nexus called")
    print(f"Project root: {config.project_root}")
    print(f"ChromeDriver path: {config.chromedriver_path}")
    print(f"Data cache: {config.scraped_data_cache}")
    
def scrapeSelectedSites():
    print("Scraping sites")
    print(f"Using ChromeDriver at: {config.chromedriver_path}")

if __name__ == "__main__":
    main()