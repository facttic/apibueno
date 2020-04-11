"""app.router.v1.all.py"""
from ...services.location.local import get_category
from ...models.all import Todos
from . import V1


@V1.get("/todos", response_model=Todos)
async def todos():  # pylint: disable=redefined-builtin
    """Trae todas las categorias."""
    confirmed = await get_category("confirmed")
    deaths = await get_category("deaths")
    recovered = await get_category("recovered")

    return {
        # Data.
        "confirmados": confirmed,
        "muertes": deaths,
        "recuperados": recovered,
        # Latest.
        "ultimos": {"confirmados": confirmed["ultimos"], "muertes": deaths["ultimos"], "recuperados": recovered["ultimos"],},
    }
