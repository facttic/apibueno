from typing import Dict

from pydantic import BaseModel


class Timeline(BaseModel):
    """
    Timeline model.
    """

    ultimos: int
    timeline: Dict[str, int] = {}


class Timelines(BaseModel):
    """
    Timelines model.
    """

    confirmados: Timeline
    muertes: Timeline
    recuperados: Timeline
