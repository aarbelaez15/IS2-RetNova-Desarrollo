from co.edu.uco.retnova.infrastructure.config.database import db_config
from datetime import datetime

class AuditoriaRepositoryPostgres:
    """Repositorio para registrar eventos de auditoría en PostgreSQL."""

    def registrar_evento(self, usuario_id: int, accion: str, descripcion: str):
        connection = db_config.get_connection()
        cursor = connection.cursor()
        try:
            query = """
                INSERT INTO auditoria (id_usuario, accion, descripcion, fecha_evento)
                VALUES (%s, %s, %s, %s)
            """
            valores = (usuario_id, accion, descripcion, datetime.now())
            cursor.execute(query, valores)

            # 🔐 Confirmar la transacción explícitamente
            connection.commit()

            print(f"✅ Auditoría guardada: {accion} -> {descripcion}")

        except Exception as e:
            connection.rollback()  # ← Evita que quede bloqueado el pool
            print(f"[ERROR] No se pudo registrar el evento de auditoría: {e}")
            raise
        finally:
            cursor.close()
            db_config.release_connection(connection)

    def listar_eventos(self):
        connection = db_config.get_connection()
        cursor = connection.cursor()
        try:
            cursor.execute("SELECT * FROM auditoria ORDER BY fecha_evento DESC;")
            rows = cursor.fetchall()
            columnas = [desc[0] for desc in cursor.description]
            return [dict(zip(columnas, r)) for r in rows]
        finally:
            cursor.close()
            db_config.release_connection(connection)
