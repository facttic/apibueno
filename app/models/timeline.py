from typing import Dict

from pydantic import BaseModel


class Historial(BaseModel):
    """
    Historial de una categoria en particular.
    """

    ultimos: int
    timeline: Dict[str, int] = {}


class Historiales(BaseModel):
    """
    Historial para cada categoria.
    """

    confirmados: Historial
    muertes: Historial
    recuperados: Historial
