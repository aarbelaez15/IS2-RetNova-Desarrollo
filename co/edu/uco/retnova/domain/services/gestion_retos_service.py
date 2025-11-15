from datetime import datetime
from co.edu.uco.retnova.domain.models.reto import Reto
from co.edu.uco.retnova.infrastructure.external.catalogo_parametros import CatalogoParametros

class GestionRetosService:
    """Reglas de negocio puras del dominio de retos."""

    def validar_creacion(self, reto: Reto):
        if not reto.titulo or not reto.descripcion:
            raise ValueError("El reto debe tener título y descripción.")

        if reto.fecha_entrega <= datetime.now():
            raise ValueError("La fecha de entrega debe ser futura.")

        # Validar que el estado inicial sea válido
        CatalogoParametros.validar("ESTADOS_RETO", reto.estado)
        reto.fecha_creacion = datetime.now()
        reto.estado = "Pendiente"

    def cambiar_estado(self, reto: Reto, nuevo_estado: str):
        CatalogoParametros.validar("ESTADOS_RETO", nuevo_estado)

        if nuevo_estado == "Finalizado" and reto.fecha_entrega is None:
            raise ValueError("No puede finalizar un reto sin fecha de entrega.")

        reto.estado = nuevo_estado
        return reto
