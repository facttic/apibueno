"""app.utils.populations_province.py"""
import logging

import requests
from wikipedia_table import parse_table

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
    #web = requests.get("https://es.wikipedia.org/wiki/Demografía_de_Argentina").text
    web = requests.get("https://es.wikipedia.org/wiki/Pandemia_de_enfermedad_por_coronavirus_de_2020_en_Argentina").text

    data = parse_table(web)
    for r in data:
        mappings.update({r[0]: int(r[2])})

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
