from fastapi import HTTPException
from co.edu.uco.retnova.infrastructure.external.catalogo_mensajes import CatalogoMensajes
from co.edu.uco.retnova.infrastructure.persistence.reto_repository_postgres import RetoRepositoryPostgres

class AsignarResponsableUseCase:

    def __init__(self):
        self.repo = RetoRepositoryPostgres()

    def ejecutar(self, reto_id: int, responsable_id: int, lider_id: int):

        reto = self.repo.obtener_por_id(reto_id)
        if not reto:
            raise HTTPException(
                status_code=404,
                detail=CatalogoMensajes.obtener("NO_ENCONTRADO_RETO") + f" (ID: {reto_id})"
            )

        if not self.repo.usuario_existe(responsable_id):
            raise HTTPException(
                status_code=404,
                detail=CatalogoMensajes.obtener("NO_ENCONTRADO_USUARIO") + f" (ID: {responsable_id})"
            )

        # 🔥 Validar rol del responsable
        rol_responsable = self.repo.obtener_rol_usuario(responsable_id)
        if rol_responsable != "Miembro":
            raise HTTPException(
                status_code=400,
                detail=CatalogoMensajes.obtener("ASIGNAR_RESPONSABLE_ROL_INVALIDO")
            )

        self.repo.asignar_responsable(reto_id, responsable_id)

        self.repo.registrar_auditoria(
            accion="Asignación de responsable",
            descripcion=f"El líder {lider_id} asignó al usuario {responsable_id} como responsable del reto {reto_id}",
            usuario_id=lider_id
        )

        return {
            "mensaje": CatalogoMensajes.obtener("ASIGNAR_RESPONSABLE_OK"),
            "reto_id": reto_id,
            "nuevo_responsable": responsable_id
        }
