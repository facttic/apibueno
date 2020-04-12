"""app.coordinates.py"""


class Coordinates:
    """
    Una posición en la tierra usando coordenadas decimales (latitud y longitud).
    """

    def __init__(self, latitude, longitude):
        self.latitude = latitude
        self.longitude = longitude

    def serialize(self):
        """
        Serializa las coordenadas en un dict.

        :returns: Las coordenadas serializadas.
        :rtype: dict
        """
        return {"latitude": self.latitude, "longitude": self.longitude}

    def __str__(self):
        return "lat: %s, long: %s" % (self.latitude, self.longitude)
