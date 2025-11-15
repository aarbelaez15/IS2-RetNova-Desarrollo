from co.edu.uco.retnova.app.dto.reto_dto import RetoDTO
from co.edu.uco.retnova.domain.models.reto import Reto

class RetoMapper:
    """Convierte entre Reto (dominio) y RetoDTO (aplicación)."""

    @staticmethod
    def to_domain(dto: RetoDTO):
        return Reto(
            id=dto.id,
            titulo=dto.titulo,
            descripcion=dto.descripcion,
            categoria=dto.categoria,
            estado=dto.estado,
            fecha_creacion=dto.fecha_creacion,
            fecha_entrega=dto.fecha_entrega,
            solicitante_id=dto.solicitante_id,
            responsable_id=dto.responsable_id,
            observaciones=dto.observaciones
        )


    @staticmethod
    def to_dto(reto: Reto) -> RetoDTO:
        return RetoDTO(
            id=reto.id,
            titulo=reto.titulo,
            descripcion=reto.descripcion,
            categoria=reto.categoria,
            estado=reto.estado,
            fecha_creacion=reto.fecha_creacion,
            fecha_entrega=reto.fecha_entrega,
            solicitante_id=reto.solicitante_id,
            responsable_id=reto.responsable_id,
            observaciones=reto.observaciones
        )
