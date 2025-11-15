from fastapi import APIRouter
from co.edu.uco.retnova.infrastructure.external.catalogo_parametros import CatalogoParametros

catalogo_router = APIRouter(prefix="/catalogo", tags=["Catálogo"])

@catalogo_router.get("/{tipo}")
def obtener_catalogo(tipo: str):
    valores = CatalogoParametros.obtener(tipo.upper())
    return valores
