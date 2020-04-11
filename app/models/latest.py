from pydantic import BaseModel


class Ultimos(BaseModel):
    """
    Latest model.
    """

    confirmados: int
    muertes: int
    recuperados: int


class RespuestaDeUltimos(BaseModel):
    """
    Response for latest.
    """

    ultimos: Ultimos
