# API de tareas

API básica para crear, consultar, actualizar y eliminar tareas usando FastAPI.

## Instalación

Crea y activa un entorno virtual, y luego instala las dependencias:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Ejecución

Desde la raíz del proyecto, ejecuta:

```bash
uvicorn app.main:app --reload
```

La API estará disponible en `http://127.0.0.1:8000`.

Documentación interactiva: `http://127.0.0.1:8000/docs`
