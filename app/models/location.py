from typing import Dict, List

from pydantic import BaseModel

from .latest import Latest
from .timeline import Timelines


class Location(BaseModel):
    """
    Location model.
    """

    id: int
    pais: str
    codigo_pais: str
    poblacion_pais: int = None
    provincia: str = ""
    poblacion_provincia: int = None
    municipio: str = ""
    ultima_actualizacion: str  # TODO use datetime.datetime type.
    coordenadas: Dict
    ultimos: Latest
    timelines: Timelines = {}


class LocationResponse(BaseModel):
    """
    Response for location.
    """

    lugar: Location


class LocationsResponse(BaseModel):
    """
    Response for locations.
    """

    ultimos: Latest
    lugares: List[Location] = []
