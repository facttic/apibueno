from typing import Dict, List

from pydantic import BaseModel

from .latest import Ultimos
from .timeline import Historiales

class Coordenadas(BaseModel):
    latitude: str
    longitude: str

class Lugar(BaseModel):
    """
    Ubicacion.
    """

    id: int
    pais: str
    codigo_pais: str
    poblacion_pais: int = None
    provincia: str = ""
    poblacion_provincia: int = None
    municipio: str = ""
    ultima_actualizacion: str  # TODO use datetime.datetime type.
    coordenadas: Coordenadas
    ultimos: Ultimos
    timelines: Historiales = {}

class LugarParaCategoria(BaseModel):
    """
    Datos de Ubicacion para una categoria en particular.
    """

    pais: str
    codigo_pais: str
    provincia: str = ""
    coordenadas: Coordenadas
    historico: Dict
    ultimos: int

class LugaresPorCategoria(BaseModel):
    """
    Datos de Ubicaciones para una categoria en particular.
    """
    lugares: List[LugarParaCategoria]


class RespuestaDeLugar(BaseModel):
    """
    Response for location.
    """

    lugar: Lugar


class RespuestaDeLugares(BaseModel):
    """
    Response for locations.
    """

    ultimos: Ultimos
    lugares: List[Lugar] = []
