"""app.router.v2.latest.py"""
from fastapi import Request

from ...enums.sources import Sources
from ...models.latest import RespuestaDeUltimos as Ultimos
from . import V2


@V2.get("/ultimos", response_model=Ultimos)
async def ultimos(request: Request, fuente: Sources = "local"):  # pylint: disable=unused-argument
    """
    Ir a buscar los últimos totales de casos confirmados, muertes y recuperados.
    """
    locations = await request.state.source.get_all()
    return {
        "ultimos": {
            "confirmados": sum(map(lambda location: location.confirmados, locations)),
            "muertes": sum(map(lambda location: location.muertes, locations)),
            "recuperados": sum(map(lambda location: location.recuperados, locations)),
        }
    }
