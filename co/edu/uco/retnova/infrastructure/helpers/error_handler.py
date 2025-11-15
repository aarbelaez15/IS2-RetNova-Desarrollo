from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from co.edu.uco.retnova.infrastructure.external.catalogo_mensajes import CatalogoMensajes

# ---- Errores de validación (Pydantic) ----
async def validation_exception_handler(request: Request, exc: RequestValidationError):

    return JSONResponse(
        status_code=400,
        content={
            "error": CatalogoMensajes.obtener("VALIDACION_INTERNA")
        }
    )

# ---- Errores HTTP lanzados explícitamente ----
async def http_exception_handler(request: Request, exc: StarletteHTTPException):

    detalle = exc.detail

    # Caso: el detalle ES una clave del catálogo
    if isinstance(detalle, str) and CatalogoMensajes.obtener(detalle) != f"[MENSAJE_NO_DEFINIDO:{detalle}]":
        detalle = CatalogoMensajes.obtener(detalle)

    return JSONResponse(
        status_code=exc.status_code,
        content={ "error": detalle }
    )

# ---- Errores inesperados ----
async def generic_exception_handler(request: Request, exc: Exception):

    return JSONResponse(
        status_code=500,
        content={
            "error": CatalogoMensajes.obtener("ERROR_DESCONOCIDO")
        }
    )
