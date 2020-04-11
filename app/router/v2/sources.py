"""app.router.v2.sources.py"""
from ...data import DATA_SOURCES
from . import V2


@V2.get("/fuentes")
async def sources():
    """
    Trae la lista de fuentes de datos disponibles para usar.
    """
    return {"fuentes": list(DATA_SOURCES.keys())}
