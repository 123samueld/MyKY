from typing import List, Dict
import json
import os
from pathlib import Path
from playwright.sync_api import Page, TimeoutError as PlaywrightTimeout  # FIXED: Proper import for timeout exception
from datetime import datetime
import random
from time import sleep
import re
import requests  # FIXED: Import for download_images
from requests.adapters import HTTPAdapter  # FIXED: For retries
from urllib3.util.retry import Retry  # FIXED: For retries

LANDSEARCH_KY_URL = "https://www.landsearch.com/properties/kentucky/filter/format=sales%2Bauctions,hoa=0,pending=0,sort=-newest,structure=0"

# Get the correct cache directory from FilePathCompendium
def get_cache_directory():
    """Get the correct cache directory from FilePathCompendium.json"""
    try:
        # Get the project root directory
        script_dir = Path(__file__).parent.parent.parent
        project_root = script_dir
        
        # Load FilePathCompendium.json
        config_file = project_root / "Utilities" / "FilePathCompendium.json"
        with open(config_file, 'r') as f:
            config = json.load(f)
        
        # Get the scraper cache directory
        cache_dir = config.get('scraperCacheDirectory', './ScrapeSystem/ScrapedDataCache/')
        
        # Convert relative path to absolute path
        if cache_dir.startswith('./'):
            cache_dir = str(project_root / cache_dir[2:])
        elif not cache_dir.startswith('/'):
            cache_dir = str(project_root / cache_dir)
        
        return cache_dir
    except Exception as e:
        print(f"⚠️ Could not load config, using default path: {e}")
        return "ScrapedDataCache"

LANDSEARCH_CACHE_DIR = get_cache_directory()
LANDSEARCH_CACHE_FILE = os.path.join(LANDSEARCH_CACHE_DIR, "landsearch_scrape_cache.json")
PROGRESS_FILE = os.path.join(LANDSEARCH_CACHE_DIR, "landsearch_progress.json")

def clear_landsearch_cache():
    """Clear all cache files and directories for a fresh start"""
    import shutil
    
    # Remove JSON cache files
    if os.path.exists(LANDSEARCH_CACHE_FILE):
        os.remove(LANDSEARCH_CACHE_FILE)
        print("🗑️  Removed landsearch_scrape_cache.json")
    
    if os.path.exists(PROGRESS_FILE):
        os.remove(PROGRESS_FILE)
        print("🗑️  Removed landsearch_progress.json")
    
    # Remove entire ImageCache directory
    image_cache_dir = os.path.join(LANDSEARCH_CACHE_DIR, "ImageCache")
    if os.path.exists(image_cache_dir):
        shutil.rmtree(image_cache_dir)
        print("🗑️  Removed ImageCache directory and all images")
    
    print("✅ Cache completely cleared - ready for fresh scraping session")

def load_landsearch_cache() -> List[Dict]:
    os.makedirs(LANDSEARCH_CACHE_DIR, exist_ok=True)
    if os.path.exists(LANDSEARCH_CACHE_FILE):
        with open(LANDSEARCH_CACHE_FILE, 'r') as f:
            return json.load(f)
    return []

def save_landsearch_cache(data: List[Dict]):
    with open(LANDSEARCH_CACHE_FILE, 'w') as f:
        json.dump(data, f, indent=2)
    print(f"💾 Saved {len(data)} properties to {LANDSEARCH_CACHE_FILE}")

def load_progress() -> int:
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE, 'r') as f:
            data = json.load(f)
            return data.get('current_page', 1)
    return 1

def save_progress(current_page: int):
    with open(PROGRESS_FILE, 'w') as f:
        json.dump({'current_page': current_page}, f)
    print(f"📊 Updated progress to page {current_page}")

def scrape_site(page: Page) -> List[Dict]:
    print("🚀 Starting LandSearch scrape... (TEST MODE: 3 properties + full details)")
    
    # Record scrape start time
    scrape_start_time = datetime.now()
    scrape_timestamp = scrape_start_time.strftime("%Y-%m-%d %H:%M:%S")
    print(f"📅 Scrape session started at: {scrape_timestamp}")
    
    # Clear all cache for fresh start
    clear_landsearch_cache()
    
    scraped_data = []
    existing_urls = set()
    temp_id_counter = 1
    total_properties = 0
    
    page_num = 1  # Start from page 1 for fresh session
    
    page.goto(LANDSEARCH_KY_URL, wait_until="networkidle")  # Initial goto to handle consent
    print("⏳ Waiting 8 seconds for SLOW MAP + POPUP...")
    sleep(8)
    
    # Consent popup (already working!)
    cookie_button = page.locator('button.fc-cta-consent')
    try:
        cookie_button.wait_for(timeout=10000)
        cookie_button.click()
        print("✅ Clicked 'Consent' button!")
        sleep(3)
    except:
        print("ℹ️ No consent popup found")
    
    while total_properties < 3:
        url = LANDSEARCH_KY_URL if page_num == 1 else f"{LANDSEARCH_KY_URL}/p{page_num}"
        print(f"\n📋 Page {page_num} ({url})...")
        
        page.goto(url, wait_until="networkidle")
        sleep(2)  # Short wait after load
        
        # Re-check consent if needed (though cookies should persist)
        try:
            cookie_button.wait_for(timeout=5000)
            cookie_button.click()
            sleep(1)
        except:
            pass
        
        cards = page.locator('article.preview')
        card_elements = cards.all()
        print(f"🔍 Found {len(card_elements)} properties")
        
        if len(card_elements) == 0:
            break
        
        for i, card in enumerate(card_elements):
            if total_properties >= 3:
                break
                
            sleep(random.uniform(0.5, 1))
            
            try:
                # ✅ YOUR EXACT LINK: a.preview__link
                link_elem = card.locator('a.preview__link').first
                detail_url = link_elem.get_attribute('href')
                if detail_url and not detail_url.startswith('http'):
                    detail_url = f"https://www.landsearch.com{detail_url}"
                
                if detail_url in existing_urls:
                    print(f"  ⏭️ Skipping already scraped: {detail_url[-50:]}")
                    continue
                
                # ✅ YOUR EXACT TITLE: div.preview__title
                title_elem = card.locator('div.preview__title').first
                full_text = title_elem.inner_text().strip()
                
                price_match = re.search(r'\$(\d{1,3}(?:,\d{3})*)', full_text)
                acres_match = re.search(r'(\d+(?:\.\d+)?)\s*acres?', full_text)
                
                price = f"${price_match.group(1)}" if price_match else "N/A"
                acres = f"{acres_match.group(1)} acres" if acres_match else "N/A"
                clean_text = re.sub(r'\$(\d{1,3}(?:,\d{3})*)|(\d+(?:\.\d+)?)\s*acres?', '', full_text)
                address = clean_text.strip()
                
                # ✅ YOUR EXACT LOCATION: div.preview__location
                location_elem = card.locator('div.preview__location').first
                full_address = location_elem.inner_text().strip()
                
                print(f"  🔗 Opening: {detail_url[-50:]}")
        
                with page.context.new_page() as detail_page:
                    # FIXED: Navigation - higher timeout, looser wait_until for slow site
                    detail_page.goto(detail_url, timeout=60000, wait_until="domcontentloaded")
                    detail_page.wait_for_load_state('networkidle', timeout=30000)  # Extra wait post-load
                    sleep(5)  # Buffer for maps/images to settle
                    
                    # FIXED: Correct param order - detail_page first, then temp_id last
                    full_details = scrape_detail_page(detail_page, address, full_address, price, acres, detail_url, temp_id_counter, scrape_timestamp)
                    property_data = full_details
                
                scraped_data.append(property_data)
                save_landsearch_cache(scraped_data)
                existing_urls.add(detail_url)
                temp_id_counter += 1
                total_properties += 1
                print(f"  ✅ {total_properties}/3: {price} | {acres} | {full_address}")
                
            except Exception as e:
                print(f"  ❌ Card {i+1} error: {e}")
                continue
        
        if total_properties < 3:
            next_button = page.locator('a[rel="next"]').first
            if next_button.is_visible():
                page_num += 1
                save_progress(page_num)
            else:
                break
    
    # Clean up progress if completed
    if os.path.exists(PROGRESS_FILE):
        os.remove(PROGRESS_FILE)
        print("🗑️  Removed progress file as scrape is complete")
    
    print(f"\n🎉 LandSearch TEST COMPLETE! {len(scraped_data)} properties")
    return scraped_data

def scrape_detail_page(detail_page: Page, address: str, full_address: str, price: str, acres: str, detail_url: str, temp_id: int, scrape_timestamp: str = None) -> dict:
    """Build COMPLETE FLAT JSON + DOWNLOAD IMAGES to ImageCache/temp_ID/"""
    if scrape_timestamp is None:
        scrape_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    property_data = {
        "temp_ID": temp_id,
        "site": "landsearch",
        "address": address,
        "full_address": full_address,
        "street_address": "",
        "price": price,
        "acres": acres,
        "listed_date": datetime.now().strftime("%Y-%m-%d"),
        "county": "",
        "elevation": "",
        "coordinates": "",
        "detail_url": detail_url,
        "scrape_timestamp": scrape_timestamp
    }
    
    try:
        detail_page.wait_for_selector('article.property', timeout=30000)  # Increased timeout
        detail_page.wait_for_load_state('networkidle', timeout=30000)  # Ensure everything loaded
        sleep(5)  # Extra buffer for maps/images
        
        # Fill 5 fields (use inner_text with timeout)
        property_data["street_address"] = detail_page.locator('dt:has-text("Street address") + dd').inner_text(timeout=10000).strip()
        property_data["county"] = detail_page.locator('dt:has-text("County") + dd a').inner_text(timeout=10000).strip()
        property_data["elevation"] = detail_page.locator('dt:has-text("Elevation") + dd').inner_text(timeout=10000).strip()
        property_data["coordinates"] = detail_page.locator('dt:has-text("Coordinates") + dd span').inner_text(timeout=10000).strip()
        
        # DOWNLOAD IMAGES
        print(f"     📸 Downloading {temp_id} images...")
        download_images(detail_page, temp_id)
        
        print(f"     ✅ FILLED: {property_data['street_address'][:20]} | {property_data['county']}")
        
    except PlaywrightTimeout as timeout_error:  # FIXED: Proper exception name
        print(f"     ❌ Timeout waiting for elements on {detail_url}: {timeout_error}")
        # Optional debug screenshot
        detail_page.screenshot(path=f"debug_timeout_{temp_id}.png")
    except Exception as e:
        print(f"     ❌ Error: {e}")
        detail_page.screenshot(path=f"debug_error_{temp_id}.png")
    
    return property_data


def download_images(detail_page: Page, temp_id: int):
    """Download LARGE images to ImageCache/temp_ID/ using requests with retries"""
    IMAGE_DIR = os.path.join("ScrapedDataCache", "ImageCache", str(temp_id))
    os.makedirs(IMAGE_DIR, exist_ok=True)
    
    # Wait for gallery to load
    try:
        detail_page.wait_for_selector('.property-gallery img[src*="large"]', timeout=20000)
    except PlaywrightTimeout:
        print("     ❌ Gallery images not found even after wait")
        return
    
    images = detail_page.locator('.property-gallery img[src*="large"]').all()
    print(f"     Found {len(images)} images to download")
    
    # Session with retries for flaky network
    session = requests.Session()
    retry = Retry(total=3, backoff_factor=1, status_forcelist=[500, 502, 503, 504])
    session.mount('https://', HTTPAdapter(max_retries=retry))
    
    base_url = "https://www.landsearch.com"  # For relative URLs
    
    for i, img in enumerate(images):
        try:
            img_url = img.get_attribute('src')
            if img_url:
                if img_url.startswith('/'):
                    img_url = base_url + img_url
                elif not img_url.startswith('http'):
                    continue  # Skip invalid
                
                print(f"     Downloading {img_url}")
                response = session.get(img_url, timeout=15)
                if response.status_code == 200:
                    filename = f"{temp_id}_{i+1}.jpg"
                    filepath = os.path.join(IMAGE_DIR, filename)
                    with open(filepath, 'wb') as f:
                        f.write(response.content)
                    print(f"     💾 Saved: {filename}")
                else:
                    print(f"     ❌ HTTP {response.status_code} for image {i+1}")
        except Exception as e:
            print(f"     ❌ Image {i+1} error: {e}")