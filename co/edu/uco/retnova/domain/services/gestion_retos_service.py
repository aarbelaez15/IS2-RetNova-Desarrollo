from datetime import datetime
from co.edu.uco.retnova.domain.models.reto import Reto
from co.edu.uco.retnova.infrastructure.external.catalogo_parametros import CatalogoParametros
from co.edu.uco.retnova.infrastructure.external.catalogo_mensajes import CatalogoMensajes

class GestionRetosService:

    def validar_creacion(self, reto: Reto):

        if not reto.titulo or not reto.descripcion:
            raise ValueError(
                CatalogoMensajes.obtener("RETO_TITULO_DESCRIPCION_OBLIGATORIO")
            )

        if reto.fecha_entrega <= datetime.now():
            raise ValueError(
                CatalogoMensajes.obtener("RETO_FECHA_ENTREGA_FUTURA")
            )

        CatalogoParametros.validar("ESTADOS_RETO", reto.estado)

        reto.fecha_creacion = datetime.now()
        reto.estado = "Pendiente"

    def cambiar_estado(self, reto: Reto, nuevo_estado: str):

        CatalogoParametros.validar("ESTADOS_RETO", nuevo_estado)

        if nuevo_estado == "Finalizado" and reto.fecha_entrega is None:
            raise ValueError(
                CatalogoMensajes.obtener("RETO_FINALIZAR_SIN_FECHA")
            )

        reto.estado = nuevo_estado
        return reto
