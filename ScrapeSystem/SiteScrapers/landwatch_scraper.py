from typing import List, Dict

LANDWATCH_KY_URL = "https://www.landwatch.com/"


def scrape_site(driver) -> List[Dict]:
    """Navigate to the LandWatch site (KY context TBD) and open it.

    Returns an empty list for now; orchestration expects a list.
    """
    driver.get(LANDWATCH_KY_URL)
    return []

# https://www.landwatch.com/kentucky-land-for-sale