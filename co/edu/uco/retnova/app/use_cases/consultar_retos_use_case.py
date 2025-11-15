from co.edu.uco.retnova.infrastructure.persistence.reto_repository_postgres import RetoRepositoryPostgres

class ConsultarRetosUseCase:
    """Caso de uso para consultas de retos."""

    def __init__(self):
        self.reto_repository = RetoRepositoryPostgres()

    def listar_todos(self):
        return self.reto_repository.listar_todos()

    def obtener_por_id(self, reto_id: int):
        return self.reto_repository.obtener_por_id(reto_id)

    def filtrar_por_estado(self, estado: str):
        return self.reto_repository.filtrar_por_estado(estado)
