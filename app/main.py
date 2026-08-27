from fastapi import APIRouter, FastAPI, HTTPException, status, Query
from app.schemas.tareas_schemas import Tarea, TareaBase
from typing import Literal

app = FastAPI()
router = APIRouter(prefix="/tareas", tags=["Tareas"])

_tareas: dict[int, Tarea] = {} 

def obtener_tarea(tarea_id: int) -> Tarea:
    tarea = _tareas.get(tarea_id)
    if tarea is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tarea no encontrada",
        )
    return tarea

@router.post("/", response_model=Tarea, status_code=status.HTTP_201_CREATED)
def crear_tarea(tarea: TareaBase) -> Tarea:
    nuevo_id = max(_tareas.keys(), default=0) + 1

    nueva_tarea = {
        "id": nuevo_id,
        "titulo":  tarea.titulo,
        "prioridad": tarea.prioridad,
        "completada": tarea.completada,
        "horas_estimadas": tarea.horas_estimadas
    }

    _tareas[nuevo_id] = Tarea(**nueva_tarea)
    return _tareas[nuevo_id]

@router.get("/", response_model=list[Tarea])
def listar_tareas(prioridad: Literal["alta", "media", "baja"] | None = Query(default=None)) -> list[Tarea]:
    tareas = _tareas.values()
    if prioridad is not None:
        tareas = (tarea for tarea in tareas if tarea.prioridad == prioridad)
    return tareas 

@router.get("/{tarea_id}",  response_model=Tarea)
def buscar_tarea(tarea_id: int) -> Tarea:
    return obtener_tarea(tarea_id)

@router.put("/{tarea_id}", response_model=Tarea)
def actualizar_tarea(tarea_id: int, tarea: TareaBase) -> Tarea:
    obtener_tarea(tarea_id)
    tarea_actualizada = Tarea(
        id=tarea_id,
        titulo=tarea.titulo,
        prioridad=tarea.prioridad,
        completada=tarea.completada,
        horas_estimadas=tarea.horas_estimadas,
    )
    _tareas[tarea_id] = tarea_actualizada
    return tarea_actualizada

@router.delete("/{tarea_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_tarea(tarea_id: int) -> None:
    obtener_tarea(tarea_id)
    del _tareas[tarea_id]


app.include_router(router)
