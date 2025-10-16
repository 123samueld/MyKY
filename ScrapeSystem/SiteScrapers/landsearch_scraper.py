from typing import List, Dict

LANDSEARCH_KY_URL = "https://www.landsearch.com/"


def scrape_site(driver) -> List[Dict]:
    """Navigate to the LandSearch site (KY context TBD) and open it.

    Returns an empty list for now; orchestration expects a list.
    """
    driver.get(LANDSEARCH_KY_URL)
    return []

# https://www.landsearch.com/properties/kentucky