from pydantic import BaseModel
from .latest import Ultimos
from .location import LugaresPorCategoria

class Todos(BaseModel):
    """
    Totales y ultimos valores
    """

    confirmados: LugaresPorCategoria
    muertes: LugaresPorCategoria
    recuperados: LugaresPorCategoria
    ultimos: Ultimos
