from pydantic import BaseModel
from typing import List

class FuentesDeDatos(BaseModel):
    """
    Origenes de la informacion
    """
    fuentes: List[str]
