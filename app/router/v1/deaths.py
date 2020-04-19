"""app.router.v1.deaths.py"""
from ...services.location.local import get_category
from ...models.location import LugaresPorCategoria
from . import V1


@V1.get("/muertes", response_model=LugaresPorCategoria)
async def muertes(totales: bool = False):
    """**Muertes por dia**<br />
        - Por default trae los fallecidos nuevos por dia.<br />
        - Si se pasa `totales=true` trae las muertes acumuladas dia por dia"""
    deaths_data = await get_category("deaths", totales)

    return deaths_data
