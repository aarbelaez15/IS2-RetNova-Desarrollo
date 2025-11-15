from co.edu.uco.retnova.infrastructure.persistence.reto_repository_postgres import RetoRepositoryPostgres

class AsignarResponsableUseCase:

    def __init__(self):
        self.repo = RetoRepositoryPostgres()

    def ejecutar(self, reto_id: int, responsable_id: int, lider_id: int):

        # 1. Verificar si el reto existe
        reto = self.repo.obtener_por_id(reto_id)
        if not reto:
            raise ValueError(f"❌ El reto {reto_id} no existe.")

        # 2. Verificar si el usuario existe
        if not self.repo.usuario_existe(responsable_id):
            raise ValueError(f"❌ El usuario {responsable_id} no existe.")

        # 3. Actualizar responsable del reto
        self.repo.asignar_responsable(reto_id, responsable_id)

        # 4. Registrar auditoría
        self.repo.registrar_auditoria(
            accion="Asignación de responsable",
            descripcion=f"El líder {lider_id} asignó al usuario {responsable_id} como responsable del reto {reto_id}",
            usuario_id=lider_id
        )

        return {"reto_id": reto_id, "nuevo_responsable": responsable_id}
