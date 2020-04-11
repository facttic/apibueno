"""app.location"""
from ..coordinates import Coordinates
from ..utils import countries
from ..utils.populations import country_population
from ..utils.populations_provinces import province_population

# pylint: disable=redefined-builtin,invalid-name
class Location:  # pylint: disable=too-many-instance-attributes
    """
    Un lugar afectado por el coronavirus.
    """

    def __init__(
        self, id, country, province, coordinates, last_updated, confirmed, deaths, recovered
    ):  # pylint: disable=too-many-arguments
        # General info.
        self.id = id
        self.pais = country.strip()
        self.provincia = province.strip()
        self.coordenadas = coordinates

        # Last update.
        self.ultima_actualizacion = last_updated

        # Statistics.
        self.confirmados = confirmed
        self.muertes = deaths
        self.recuperados = recovered

    @property
    def country_code(self):
        """
        Trae el código alpha-2 del país. Retorna 'XX' si no lo encuentra.

        :returns: Código de país.
        :rtype: str
        """
        return (countries.country_code(self.pais) or countries.DEFAULT_COUNTRY_CODE).upper()

    @property
    def country_population(self):
        """
        Trae la población del país.

        :returns: La población.
        :rtype: int
        """
        return country_population(self.country_code)

    @property
    def province_population(self):
        """
        Trae la población de la provincia.

        :returns: La población.
        :rtype: int
        """
        return province_population(self.provincia)

    def serialize(self):
        """
        Serializa el lugar en un dict.

        :returns: El lugar serializado.
        :rtype: dict
        """
        return {
            # General info.
            "id": self.id,
            "pais": self.pais,
            "codigo_pais": self.country_code,
            "poblacion_pais": self.country_population,
            "provincia": self.provincia,
            "poblacion_provincia": self.province_population,
            # Coordinates.
            "coordenadas": self.coordenadas.serialize(),
            # Last updated.
            "ultima_actualizacion": self.ultima_actualizacion,
            # Latest data (statistics).
            "ultimos": {"confirmados": self.confirmados, "muertes": self.muertes, "recuperados": self.recuperados},
        }


class TimelinedLocation(Location):
    """
    Un lugar con timelines.
    """

    # pylint: disable=too-many-arguments
    def __init__(self, id, country, province, coordinates, last_updated, timelines):

        super().__init__(
            # General info.
            id,
            country,
            province,
            coordinates,
            last_updated,
            # Statistics (retrieve latest from timelines).
            confirmed=timelines.get("confirmados").latest or 0,
            deaths=timelines.get("muertes").latest or 0,
            recovered=timelines.get("recuperados").latest or 0,
        )

        # Set timelines.
        self.timelines = timelines

    # pylint: disable=arguments-differ
    def serialize(self, timelines=False):
        """
        Serialización de un lugar en un dict.

        :param timelines: Si incluidmos o no los timelines.
        :returns: El lugar serializado.
        :rtype: dict
        """
        serialized = super().serialize()

        # Whether to include the timelines or not.
        if timelines:
            serialized.update(
                {
                    "timelines": {
                        # Serialize all the timelines.
                        key: value.serialize()
                        for (key, value) in self.timelines.items()
                    }
                }
            )

        # Return the serialized location.
        return serialized
