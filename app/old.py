from typing import Annotated, Literal

from fastapi import FastAPI, HTTPException, Query, status
from pydantic import BaseModel, Field


Prioridad = Literal["alta", "media", "baja"]


class TareaBase(BaseModel):
    titulo: str = Field(min_length=1)
    prioridad: Prioridad
    completada: bool = False
    horas_estimadas: float = Field(ge=0)


class Tarea(TareaBase):
    id: int


class TareaCreate(TareaBase):
    pass


class TareaUpdate(TareaBase):
    pass


app = FastAPI(title="API de Control de Tareas")

_tareas: dict[int, Tarea] = {}
_siguiente_id = 1


def _obtener_tarea(tarea_id: int) -> Tarea:
    tarea = _tareas.get(tarea_id)
    if tarea is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tarea no encontrada",
        )
    return tarea


@app.post("/tareas/", response_model=Tarea, status_code=status.HTTP_201_CREATED)
def crear_tarea(tarea: TareaCreate) -> Tarea:
    global _siguiente_id

    nueva_tarea = Tarea(id=_siguiente_id, **tarea.model_dump())
    _tareas[_siguiente_id] = nueva_tarea
    _siguiente_id += 1
    return nueva_tarea


@app.get("/tareas/", response_model=list[Tarea])
def listar_tareas(
    prioridad: Annotated[Prioridad | None, Query()] = None,
) -> list[Tarea]:
    tareas = _tareas.values()
    if prioridad is not None:
        tareas = (tarea for tarea in tareas if tarea.prioridad == prioridad)
    return list(tareas)


@app.get("/tareas/{tarea_id}", response_model=Tarea)
def buscar_tarea(tarea_id: int) -> Tarea:
    return _obtener_tarea(tarea_id)


@app.put("/tareas/{tarea_id}", response_model=Tarea)
def actualizar_tarea(tarea_id: int, tarea: TareaUpdate) -> Tarea:
    _obtener_tarea(tarea_id)
    tarea_actualizada = Tarea(id=tarea_id, **tarea.model_dump())
    _tareas[tarea_id] = tarea_actualizada
    return tarea_actualizada


@app.delete("/tareas/{tarea_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_tarea(tarea_id: int) -> None:
    _obtener_tarea(tarea_id)
    del _tareas[tarea_id]
