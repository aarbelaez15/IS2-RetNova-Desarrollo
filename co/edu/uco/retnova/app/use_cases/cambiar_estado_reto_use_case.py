from fastapi import HTTPException
from co.edu.uco.retnova.infrastructure.persistence.reto_repository_postgres import RetoRepositoryPostgres
from co.edu.uco.retnova.infrastructure.external.catalogo_mensajes import CatalogoMensajes
from co.edu.uco.retnova.infrastructure.external.catalogo_parametros import CatalogoParametros

class CambiarEstadoRetoUseCase:

    def __init__(self):
        self.repo = RetoRepositoryPostgres()

    def ejecutar(self, reto_id: int, nuevo_estado: str, usuario_id: int):

        # ------------------------------
        # 1. Normalizar estado recibido
        # ------------------------------
        nuevo_estado = nuevo_estado.strip().capitalize()

        # ------------------------------
        # 2. Obtener estados permitidos del catálogo
        # ------------------------------
        estados_validos = CatalogoParametros.obtener("ESTADOS_RETO")

        # ------------------------------
        # 3. Validar estado permitido
        # ------------------------------
        if nuevo_estado not in estados_validos:
            raise HTTPException(
                status_code=400,
                detail=(
                    CatalogoMensajes.obtener("ESTADO_INVALIDO") +
                    f" Estados permitidos: {', '.join(estados_validos)}"
                )
            )

        # ------------------------------
        # 4. Validar que el reto existe
        # ------------------------------
        reto = self.repo.obtener_por_id(reto_id)
        if not reto:
            raise HTTPException(
                status_code=404,
                detail=CatalogoMensajes.obtener("NO_ENCONTRADO_RETO") + f" (ID: {reto_id})"
            )

        # ------------------------------
        # 5. Actualizar estado
        # ------------------------------
        self.repo.actualizar_estado(reto_id, nuevo_estado)

        # ------------------------------
        # 6. Registrar auditoría
        # ------------------------------
        self.repo.registrar_auditoria(
            accion="Cambio de estado",
            descripcion=f"El usuario {usuario_id} cambió el estado del reto {reto_id} a '{nuevo_estado}'",
            usuario_id=usuario_id
        )

        # ------------------------------
        # 7. Respuesta final
        # ------------------------------
        return {
            "mensaje": CatalogoMensajes.obtener("CAMBIAR_ESTADO_OK"),
            "reto_id": reto_id,
            "nuevo_estado": nuevo_estado
        }
