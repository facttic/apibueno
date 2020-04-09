"""app.data"""
from ..services.location.local import LocalLocationService

# Mapping of services to data-sources.
DATA_SOURCES = {"local": LocalLocationService()}


def data_source(source):
    """
    Retrieves the provided data-source service.

    :returns: The service.
    :rtype: LocationService
    """
    return DATA_SOURCES.get(source.lower())
