from co.edu.uco.retnova.infrastructure.persistence.reto_repository_postgres import RetoRepositoryPostgres

ESTADOS_VALIDOS = {"Pendiente", "En progreso", "Finalizado", "Rechazado", "Impedimento"}

class CambiarEstadoRetoUseCase:

    def __init__(self):
        self.repo = RetoRepositoryPostgres()

    def ejecutar(self, reto_id: int, nuevo_estado: str, usuario_id: int):

        # Normalizar estado
        nuevo_estado = nuevo_estado.strip().capitalize()

        # Validar estado
        if nuevo_estado not in ESTADOS_VALIDOS:
            raise ValueError(f"❌ Estado inválido. Estados permitidos: {ESTADOS_VALIDOS}")

        # Verificar si el reto existe
        reto = self.repo.obtener_por_id(reto_id)
        if not reto:
            raise ValueError(f"❌ El reto {reto_id} no existe.")

        # Actualizar estado
        self.repo.actualizar_estado(reto_id, nuevo_estado)

        # Registrar auditoría
        self.repo.registrar_auditoria(
            accion="Cambio de estado",
            descripcion=f"El usuario {usuario_id} cambió el estado del reto {reto_id} a '{nuevo_estado}'",
            usuario_id=usuario_id
        )

        return {"reto_id": reto_id, "nuevo_estado": nuevo_estado}
