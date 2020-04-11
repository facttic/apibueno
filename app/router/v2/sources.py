"""app.router.v2.sources.py"""
from ...data import DATA_SOURCES
from ...models.sources import FuentesDeDatos
from . import V2


@V2.get("/fuentes", response_model=FuentesDeDatos)
async def fuentes():
    """
    Trae la lista de fuentes de datos disponibles para usar.
    """
    return {"fuentes": list(DATA_SOURCES.keys())}
