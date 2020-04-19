"""app.router.v1.recovered.py"""
from ...services.location.local import get_category
from ...models.location import LugaresPorCategoria
from . import V1


@V1.get("/recuperados", response_model=LugaresPorCategoria)
async def recuperados(totales: bool = False):
    """**Casos recuperados**<br />
        - Por default trae los recuperados nuevos por dia.<br />
        - Si se pasa `totales=true` trae los recuperados acumulados dia por dia"""
    recovered_data = await get_category("recovered", totales)

    return recovered_data
