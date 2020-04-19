"""app.router.v1.confirmed.py"""
from ...services.location.local import get_category
from ...models.location import LugaresPorCategoria
from . import V1


@V1.get("/confirmados", response_model=LugaresPorCategoria)
async def confirmados(totales: bool = False):
    """**Casos confirmados**<br />
    - Por default trae los casos nuevos por dia.<br />
    - Si se pasa `totales=true` trae los casos acumulados dia por dia"""
    confirmed_data = await get_category("confirmed", totales)

    return confirmed_data
