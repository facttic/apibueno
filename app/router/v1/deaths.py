"""app.router.v1.deaths.py"""
from ...services.location.local import get_category
from . import V1


@V1.get("/muertes")
async def muertes():
    """Total de muertes."""
    deaths_data = await get_category("deaths")

    return deaths_data
