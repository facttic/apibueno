"""app.timeline.py"""
from collections import OrderedDict


class Timeline:
    """
    Timeline con los datos históricos.
    """

    def __init__(self, history=None):
        self.__timeline = history if history else {}

    @property
    def timeline(self):
        """
        Trae el histórico ordenado por fecha (key).
        """
        return OrderedDict(sorted(self.__timeline.items()))

    @property
    def latest(self):
        """
        Trae el último valor disponible del histórico.
        """
        # Get values in a list.
        values = list(self.timeline.values())

        # Last item is the latest.
        if values:
            return values[-1] or 0

        # Fallback value of 0.
        return 0

    def serialize(self):
        """
        Serializa el timeline en un dict.

        :returns: El timeline serializado.
        :rtype: dict
        """
        return {"ultimos": self.latest, "timeline": self.timeline}
