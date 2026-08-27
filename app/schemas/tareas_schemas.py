from pydantic import BaseModel, Field
from typing import Literal

class TareaBase(BaseModel):
    titulo: str = Field(min_length=1)
    prioridad: Literal["alta", "media", "baja"]
    completada: bool = False
    horas_estimadas: float = Field(ge=0)

class Tarea(TareaBase):
    id: int
