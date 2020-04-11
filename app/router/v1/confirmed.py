"""app.router.v1.confirmed.py"""
from ...services.location.local import get_category
from ...models.location import LugaresPorCategoria
from . import V1


@V1.get("/confirmados", response_model=LugaresPorCategoria)
async def confirmados():
    """Casos confirmados."""
    confirmed_data = await get_category("confirmed")

    return confirmed_data
