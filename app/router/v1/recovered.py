"""app.router.v1.recovered.py"""
from ...services.location.local import get_category
from ...models.location import LugaresPorCategoria
from . import V1


@V1.get("/recuperados", response_model=LugaresPorCategoria)
async def recuperados():
    """Casos recuperados."""
    recovered_data = await get_category("recovered")

    return recovered_data
