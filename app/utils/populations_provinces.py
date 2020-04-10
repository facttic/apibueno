"""app.utils.populations_province.py"""
import logging

import requests
from bs4 import BeautifulSoup

LOGGER = logging.getLogger(__name__)

# Fetching of the populations.
def fetch_populations():
    """
    Returns a dictionary containing the population of each country fetched from the GeoNames.
    https://www.geonames.org/

    :returns: The mapping of populations.
    :rtype: dict
    """
    LOGGER.info("Fetching province populations...")

    # Mapping of populations
    mappings = {}

    # Fetch the province populations
    web = requests.get("https://es.wikipedia.org/wiki/Demografía_de_Argentina").text
    soup = BeautifulSoup(web, "html.parser")

    data = []
    table = soup.find('table', attrs={'class':'wikitable'})
    table_body = table.find('tbody')
    rows = table_body.find_all('tr')
    for row in rows:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        data = [ele for ele in cols if ele]
        if data:
            data[1] = data[1].replace('.','')
            mappings.update({data[0]: int(data[1]) or None})

    # Finally, return the mappings.
    return mappings


# Mapping of alpha-2 codes country codes to population.
POPULATIONS = fetch_populations()

# Retrieving.
def province_population(province_name, default=None):
    """
    Fetches the population of the country with the provided country code.

    :returns: The population.
    :rtype: int
    """
    return POPULATIONS.get(province_name, default)
