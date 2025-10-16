from typing import List, Dict

ZILLOW_KY_URL = "https://www.zillow.com/homes/24_rid/"


def scrape_site(driver) -> List[Dict]:
    """Navigate to the Zillow Kentucky URL and open it in a visible window.

    Returns an empty list for now; orchestration expects a list.
    """
    driver.get(ZILLOW_KY_URL)
    # Intentionally return no scraped data at this stage
    return []


