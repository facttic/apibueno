from pydantic import BaseModel


class Latest(BaseModel):
    """
    Latest model.
    """

    confirmados: int
    muertes: int
    recuperados: int


class LatestResponse(BaseModel):
    """
    Response for latest.
    """

    ultimos: Latest
