from co.edu.uco.retnova.app.dto.reto_dto import RetoDTO
from co.edu.uco.retnova.app.mapper.reto_mapper import RetoMapper
from co.edu.uco.retnova.domain.services.gestion_retos_service import GestionRetosService
from co.edu.uco.retnova.infrastructure.persistence.reto_repository_postgres import RetoRepositoryPostgres
from co.edu.uco.retnova.infrastructure.persistence.auditoria_repository_postgres import AuditoriaRepositoryPostgres
from co.edu.uco.retnova.infrastructure.external.catalogo_mensajes import CatalogoMensajes
from co.edu.uco.retnova.infrastructure.logging.logger_service import LoggerService


class RegistrarRetoUseCase:
    """Caso de uso para registrar un nuevo reto en el sistema."""

    def __init__(self):
        self.reto_repository = RetoRepositoryPostgres()
        self.servicio_dominio = GestionRetosService()
        self.auditor = AuditoriaRepositoryPostgres()

    def ejecutar(self, dto: RetoDTO):
        try:
            # =============================
            # 1️⃣ Transformar DTO → Dominio
            # =============================
            reto = RetoMapper.to_domain(dto)
            self.servicio_dominio.validar_creacion(reto)
            self.reto_repository.guardar(reto)

            # =============================
            # 2️⃣ Registrar auditoría
            # =============================
            self.auditor.registrar_evento(
                reto.solicitante_id,
                "CREAR_RETO",
                f"Reto '{reto.titulo}' creado por usuario {reto.solicitante_id}"
            )

            # =============================
            # 3️⃣ Logging
            # =============================
            LoggerService.info(
                f"✅ Reto creado exitosamente: '{reto.titulo}' | Solicitante ID: {reto.solicitante_id}"
            )

            mensaje = CatalogoMensajes.obtener("CREAR_RETO_OK")

            # ✅ Retornar datos DTO
            return {"mensaje": mensaje, "reto": RetoMapper.to_dto(reto)}

        except Exception as e:
            mensaje_error = CatalogoMensajes.obtener("CREAR_RETO_ERROR")
            LoggerService.error(f"❌ Error al registrar reto: {str(e)}")
            raise Exception(f"{mensaje_error} Detalle: {e}")
