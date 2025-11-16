from co.edu.uco.retnova.app.dto.reto_dto import RetoDTO
from co.edu.uco.retnova.app.mapper.reto_mapper import RetoMapper
from co.edu.uco.retnova.domain.services.gestion_retos_service import GestionRetosService
from co.edu.uco.retnova.infrastructure.persistence.reto_repository_postgres import RetoRepositoryPostgres
from co.edu.uco.retnova.infrastructure.persistence.auditoria_repository_postgres import AuditoriaRepositoryPostgres
from co.edu.uco.retnova.infrastructure.external.catalogo_mensajes import CatalogoMensajes


class ActualizarEliminarRetoUseCase:
    """Caso de uso para actualizar y eliminar retos."""

    def __init__(self):
        self.reto_repository = RetoRepositoryPostgres()
        self.servicio_dominio = GestionRetosService()
        self.auditor = AuditoriaRepositoryPostgres()

    # ======================================================
    # 🟢 ACTUALIZAR RETO
    # ======================================================
    def actualizar(self, dto: RetoDTO):
        """
        Actualiza los datos de un reto existente.
        """
        try:
            # Mapear DTO a modelo de dominio
            reto = RetoMapper.to_domain(dto)

            # Validar lógica de dominio
            self.servicio_dominio.validar_creacion(reto)

            # Ejecutar actualización en la BD
            filas = self.reto_repository.actualizar(reto)
            if filas == 0:
                raise Exception("Reto no encontrado para actualizar.")

            # Registrar auditoría
            self.auditor.registrar_evento(
                reto.solicitante_id,
                "ACTUALIZAR_RETO",
                f"Reto '{reto.titulo}' actualizado por usuario {reto.solicitante_id}."
            )

            # Retornar mensaje del catálogo
            mensaje = CatalogoMensajes.obtener("ACTUALIZAR_RETO_OK")
            return {"mensaje": mensaje, "reto": RetoMapper.to_dto(reto).__dict__}

        except Exception as e:
            mensaje_error = CatalogoMensajes.obtener("ACTUALIZAR_RETO_ERROR")
            raise Exception(f"{mensaje_error} Detalle: {e}")

    # ======================================================
    # 🔴 ELIMINAR RETO
    # ======================================================
    def eliminar(self, reto_id: int, usuario_id: int):
        """
        Elimina un reto existente por su ID.
        """
        try:
            # Ejecutar eliminación en la BD
            filas = self.reto_repository.eliminar(reto_id)
            if filas == 0:
                raise Exception("Reto no encontrado para eliminar.")

            # Registrar auditoría
            self.auditor.registrar_evento(
                usuario_id,
                "ELIMINAR_RETO",
                f"Reto con ID {reto_id} eliminado por usuario {usuario_id}."
            )

            # Retornar mensaje del catálogo
            mensaje = CatalogoMensajes.obtener("ELIMINAR_RETO_OK")
            return {"mensaje": mensaje, "reto_id": reto_id}

        except Exception as e:
            mensaje_error = CatalogoMensajes.obtener("ELIMINAR_RETO_ERROR")
            raise Exception(f"{mensaje_error} Detalle: {e}")
