from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from co.edu.uco.retnova.infrastructure.external.catalogo_mensajes import CatalogoMensajes
from fastapi import Request, Response
from fastapi.responses import JSONResponse
import psycopg2

# ---- Errores de validación (Pydantic) ----
async def validation_exception_handler(request: Request, exc: RequestValidationError):

    errors = exc.errors()

    for err in errors:
        field = err["loc"][-1]               # nombre del campo
        input_value = err.get("input")       # valor enviado
        error_type = err["type"]             # tipo de error

        # 🟣 1. Campo vacío (“”)
        if input_value == "":
            clave = f"USUARIO_{field.upper()}_OBLIGATORIO"
            return JSONResponse(
                status_code=400,
                content={ "error": CatalogoMensajes.obtener(clave) }
            )

        # 🟣 2. Campo faltante en el JSON
        if error_type == "value_error.missing":
            clave = f"USUARIO_{field.upper()}_OBLIGATORIO"
            return JSONResponse(
                status_code=400,
                content={ "error": CatalogoMensajes.obtener(clave) }
            )

        # 🟣 3. Email con formato inválido
        if field == "email" and error_type == "value_error":
            return JSONResponse(
                status_code=400,
                content={ "error": CatalogoMensajes.obtener("EMAIL_FORMATO_INVALIDO") }
            )

    # Si no se identifica el tipo exacto, usar mensaje genérico
    return JSONResponse(
        status_code=400,
        content={ "error": CatalogoMensajes.obtener("VALIDACION_INTERNA") }
    )

    # Si no es un caso capturable, usar mensaje genérico
    return JSONResponse(
        status_code=400,
        content={ "error": CatalogoMensajes.obtener("VALIDACION_INTERNA") }
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

def mostrar_error_api(response_json):
    """
    Recibe la respuesta del backend y muestra mensajes amigables en Streamlit.
    """

    # Caso 1: Mensaje directo del backend
    if "error" in response_json and response_json["error"]:
        return response_json["error"]

    # Caso 2: Errores de validación (detalle)
    if "detalle" in response_json and isinstance(response_json["detalle"], list):
        # Mostrar solo el primer error
        err = response_json["detalle"][0]
        msg = err.get("msg", "Datos inválidos.")
        return f"Error: {msg}"

    # Caso inesperado
    return "Ocurrió un error inesperado. Intenta nuevamente."




from psycopg2 import OperationalError
from psycopg2.errors import UniqueViolation


async def error_handler(request, call_next):
    try:
        return await call_next(request)

    except OperationalError:
        # Error de base de datos
        mensaje = CatalogoMensajes.obtener("ERROR_DB_CONEXION")
        return JSONResponse(status_code=500, content={"error": mensaje})

    except UniqueViolation:
        # Usuario duplicado (email o nombre ya existe)
        mensaje = CatalogoMensajes.obtener("USUARIO_YA_EXISTE")
        return JSONResponse(status_code=400, content={"error": mensaje})

    except ValueError as e:
        # Errores de validación definidos por tu dominio
        return JSONResponse(status_code=400, content={"error": str(e)})

    except Exception:
        # Error inesperado
        mensaje = CatalogoMensajes.obtener("ERROR_DESCONOCIDO")
        return JSONResponse(status_code=500, content={"error": mensaje})


        
