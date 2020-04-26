"""app.services.location.local.py"""
import csv
from datetime import datetime

from asyncache import cached
from cachetools import TTLCache

from ...coordinates import Coordinates
from ...location import TimelinedLocation
from ...timeline import Timeline
from ...utils import countries
from ...utils import date as date_util
from . import LocationService


def map_totals(totals):
    accum = 0
    accum_totals = []
    for date, amount in totals:
        accum += int(amount or 0)
        accum_totals.append((date, accum))
    return accum_totals

class LocalLocationService(LocationService):
    """
    Servicio para traer lugares desde el repositorio local repository(https://github.com/facttic/apibueno).
    """

    async def get_all(self):
        # Get the locations.
        locations = await get_locations()
        return locations

    async def get(self, loc_id):  # pylint: disable=arguments-differ
        # Get location at the index equal to provided id.
        locations = await self.get_all()
        return locations[loc_id]


# ---------------------------------------------------------------


# Base DIR for fetching category.
BASE_DIR = (
    "app/data/"
)

def latlong(province):
    latlongs = {
        "Provincia de Buenos Aires": (-34.603722,-58.381592),
        "Catamarca": (-27.1910825,-67.105374),
        "Chaco": (-26.3829647,-60.8816092),
        "Chubut": (-43.7128356,-68.7461817),
        "Córdoba": (-31.4173391,-64.183319),
        "Corrientes": (-28.5912315,-57.9394658),
        "Formosa": (-24.5955306,-60.4289718),
        "Jujuy": (-23.3161458,-65.7595288),
        "Mendoza": (-34.7871961,-68.4380712),
        "Misiones": (-26.737224,-54.4315257),
        "Neuquén": (-38.3695057,-69.832275),
        "Salta": (-25.1076701,-64.3494964),
        "Tucumán": (-26.5643582,-64.882397),
        "Entre Ríos": (-31.6252842,-59.3539578),
        "La Pampa": (-36.6148,-64.2849),
        "La Rioja": (-29.9729781,-67.0487944),
        "Río Negro": (-40.4811973,-67.6145911),
        "San Juan": (-30.7054363,-69.1988222),
        "San Luis": (-33.2762202,-65.9515546),
        "Santa Cruz": (-48.5693327,-70.1606767),
        "Santa Fe": (-30.3154739,-61.1645076),
        "Santiago del Estero": (-27.6431016,-63.5408542),
        "Tierra del Fuego, Antártida e Islas del Atlántico Sur": (-54.4071064,-67.8974895),
        "Ciudad Autónoma de Buenos Aires": (-34.6131516,-58.3772316)
    }
    return latlongs[province]


def group_by_province(rows, category, totals=False):
    provinces = {}
    categories = {
        "deaths": "Muertes",
        "recovered": "Recuperados",
        "confirmed": "Confirmados"
    }
    val_to_use = categories[category]
    if totals:
        val_to_use = "Total " + categories[category]
    for row in rows:
        province = row['Provincia']
        province_vals = provinces.get(province, {})
        province_vals[row['Dia']] = row[val_to_use]
        provinces[province] = province_vals
    return provinces


@cached(cache=TTLCache(maxsize=1024, ttl=3600))
async def get_category(category, totales = False):
    """
    Trae los datos por medio de la categoria. Los datos se cachean por 1 hora.
    Si se pasa totales=True, los datos son los acumulados hasta esa fecha
    Por defecto los datos se muestran como los valores nuevos para cada fecha

    :returns: Los datos de la categoria.
    :rtype: dict
    """

    # Adhere to category naming standard.
    category = category.lower()

    # DIR to get data from.
    dir = BASE_DIR + "time_series_export.csv"

    # Open the file
    with open(dir, mode='r') as csv_file:
        # Parse the CSV.
        rows = list(csv.DictReader(csv_file))

    data = group_by_province(rows, category, totales)

    # The normalized locations.
    locations = []

    for name, dates in data.items():
        # Make location history from dates.
        history = {date: int(amount or 0) for date, amount in dates.items()}

        # Country for this location.
        country = "Argentina"

        # Latest data insert value.
        latest = list(history.values())[-1]

        (lat, long) = latlong(name)

        # Normalize the item and append to locations.
        locations.append(
            {
                # General info.
                "pais": country,
                "codigo_pais": countries.country_code(country),
                "provincia": name,
                # Coordinates.
                "coordenadas": {"latitude": lat, "longitude": long},
                # History.
                "historico": history,
                # Latest statistic.
                "ultimos": int(latest or 0),
            }
        )

    # Latest total.
    latest = sum(map(lambda location: location["ultimos"], locations))

    # Return the final data.
    return {
        "lugares": locations,
        "ultimos": latest,
        "ultimo_actualizacion": datetime.utcnow().isoformat() + "Z",
        "fuente": "https://github.com/facttic/apibueno",
    }


@cached(cache=TTLCache(maxsize=1024, ttl=3600))
async def get_locations():
    """
    Trae los lugares de las categorias. Los lugares se cachean por 1 hora

    :returns: Los lugares.
    :rtype: List[Location]
    """
    # Get all of the data categories locations.
    confirmed = await get_category("confirmed")
    deaths = await get_category("deaths")
    recovered = await get_category("recovered")

    locations_confirmed = confirmed["lugares"]
    locations_deaths = deaths["lugares"]
    locations_recovered = recovered["lugares"]

    # Final locations to return.
    locations = []

    # Go through locations.
    for index, location in enumerate(locations_confirmed):
        # Get the timelines.
        timelines = {
            "confirmed": locations_confirmed[index]["historico"],
            "deaths": locations_deaths[index]["historico"],
            "recovered" : locations_recovered[index]["historico"],
        }

        # Grab coordinates.
        coordinates = location["coordenadas"]

        # Create location (supporting timelines) and append.
        locations.append(
            TimelinedLocation(
                # General info.
                index,
                location["pais"],
                location["provincia"],
                # Coordinates.
                Coordinates(coordinates["latitude"], coordinates["longitude"]),
                # Last update.
                datetime.utcnow().isoformat() + "Z",
                # Timelines (parse dates as ISO).
                {
                    "confirmados": Timeline(
                        {
                            datetime.strptime(date, "%m/%d/%y").isoformat() + "Z": amount
                            for date, amount in timelines["confirmed"].items()
                        }
                    ),
                    "muertes": Timeline(
                        {
                            datetime.strptime(date, "%m/%d/%y").isoformat() + "Z": amount
                            for date, amount in timelines["deaths"].items()
                        }
                    ),
                    "recuperados": Timeline(
                        {
                            datetime.strptime(date, "%m/%d/%y").isoformat() + "Z": amount
                            for date, amount in timelines["recovered"].items()
                        }
                    ),
                },
            )
        )

    # Finally, return the locations.
    return locations
