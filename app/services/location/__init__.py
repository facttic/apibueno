"""app.services.location"""
from abc import ABC, abstractmethod


class LocationService(ABC):
    """
    Servicio para ir a buscar los lugares.
    """

    @abstractmethod
    async def get_all(self):
        """
        Buscar y retorna todas los lugares.

        :returns: Los lugares.
        :rtype: List[Location]
        """
        raise NotImplementedError

    @abstractmethod
    async def get(self, id):  # pylint: disable=redefined-builtin,invalid-name
        """
        Busca y retorna el lugar por id.

        :returns: El lugar.
        :rtype: Location
        """
        raise NotImplementedError
