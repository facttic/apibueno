"""app.router.v2.locations.py"""
from fastapi import HTTPException, Request

from ...enums.sources import Sources
from ...models.location import LocationResponse as Location
from ...models.location import LocationsResponse as Locations
from . import V2


# pylint: disable=unused-argument,too-many-arguments,redefined-builtin
@V2.get("/lugares", response_model=Locations, response_model_exclude_unset=True)
async def get_locations(
    request: Request,
    fuente: Sources = "local",
    codigo_pais: str = None,
    provincia: str = None,
    municipio: str = None,
    timelines: bool = False,
):
    """
    Ir a buscar casos de un lugar
    """
    # All query paramameters.
    params = dict(request.query_params)

    # Remove reserved params.
    params.pop("fuente", None)
    params.pop("timelines", None)

    # Retrieve all the locations.
    locations = await request.state.source.get_all()

    # Attempt to filter out locations with properties matching the provided query params.
    for key, value in params.items():
        # Clean keys for security purposes.
        key = key.lower()
        value = value.lower().strip("__")

        # Do filtering.
        try:
            locations = [location for location in locations if str(getattr(location, key)).lower() == str(value)]
        except AttributeError:
            pass
        if not locations:
            raise HTTPException(404, detail=f"Source `{fuente}` does not have the desired location data.")

    # Return final serialized data.
    return {
        "ultimos": {
            "confirmados": sum(map(lambda location: location.confirmados, locations)),
            "muertes": sum(map(lambda location: location.muertes, locations)),
            "recuperados": sum(map(lambda location: location.recuperados, locations)),
        },
        "lugares": [location.serialize(timelines) for location in locations],
    }


# pylint: disable=invalid-name
@V2.get("/lugares/{id}", response_model=Location)
async def get_location_by_id(request: Request, id: int, fuente: Sources = "local", timelines: bool = True):
    """
    Ir a buscar un lugar por Id.
    """
    location = await request.state.source.get(id)
    return {"lugar": location.serialize(timelines)}
