from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from co.edu.uco.retnova.interfaces.api.controllers import reto_controller, auth_controller
from co.edu.uco.retnova.interfaces.api.controllers.auditoria_controller import router as auditoria_router
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from co.edu.uco.retnova.infrastructure.helpers.error_helper import (
    validation_exception_handler,
    http_exception_handler,
    generic_exception_handler
)
from co.edu.uco.retnova.interfaces.api.controllers.catalogo_controller import catalogo_router

app = FastAPI(
    title="🎯 RetNova API",
    description="API para gestión de retos, roles y autenticación JWT.",
    version="1.0"
)

# Permitir Swagger con seguridad
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(auth_controller.router)
app.include_router(reto_controller.router)
app.include_router(auditoria_router)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)
app.include_router(catalogo_router)