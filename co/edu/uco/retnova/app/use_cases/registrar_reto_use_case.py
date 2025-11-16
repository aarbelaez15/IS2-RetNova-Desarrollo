from fastapi import HTTPException

from co.edu.uco.retnova.app.dto.reto_dto import RetoDTO
from co.edu.uco.retnova.app.mapper.reto_mapper import RetoMapper
from co.edu.uco.retnova.domain.services.gestion_retos_service import GestionRetosService
from co.edu.uco.retnova.infrastructure.persistence.reto_repository_postgres import RetoRepositoryPostgres
from co.edu.uco.retnova.infrastructure.persistence.auditoria_repository_postgres import AuditoriaRepositoryPostgres
from co.edu.uco.retnova.infrastructure.external.catalogo_mensajes import CatalogoMensajes
from co.edu.uco.retnova.infrastructure.external.catalogo_parametros import CatalogoParametros
from co.edu.uco.retnova.infrastructure.logging.logger_service import LoggerService


class RegistrarRetoUseCase:

    def __init__(self):
        self.reto_repository = RetoRepositoryPostgres()
        self.servicio_dominio = GestionRetosService()
        self.auditor = AuditoriaRepositoryPostgres()

    def ejecutar(self, dto: RetoDTO):
        try:
            categorias_validas = CatalogoParametros.obtener("CATEGORIAS")
            if dto.categoria not in categorias_validas:
                raise ValueError(
                    CatalogoMensajes.obtener("PARAMETRO_INVALIDO")
                    + f" Categoría recibida: '{dto.categoria}'. "
                    + f"Permitidas: {', '.join(categorias_validas)}."
                )

            reto = RetoMapper.to_domain(dto)
            self.servicio_dominio.validar_creacion(reto)
            self.reto_repository.guardar(reto)

            self.auditor.registrar_evento(
                reto.solicitante_id,
                "CREAR_RETO",
                f"Reto '{reto.titulo}' creado por usuario {reto.solicitante_id}"
            )

            LoggerService.info(
                f"Reto creado exitosamente: '{reto.titulo}' | Solicitante ID: {reto.solicitante_id}"
            )

            mensaje = CatalogoMensajes.obtener("CREAR_RETO_OK")

            return {"mensaje": mensaje, "reto": RetoMapper.to_dto(reto)}

        except ValueError as e:
            LoggerService.error(str(e))
            raise HTTPException(
                status_code=400,
                detail=str(e)
            )

        except Exception as e:
            LoggerService.error(f"Error al registrar reto: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=CatalogoMensajes.obtener("CREAR_RETO_ERROR") + f" Detalle: {str(e)}"
            )
