from co.edu.uco.retnova.domain.models.reto import Reto
from co.edu.uco.retnova.infrastructure.config.database import db_config

class RetoRepositoryPostgres:
    """Repositorio de retos usando PostgreSQL."""

    def guardar(self, reto: Reto):
        connection = db_config.get_connection()
        cursor = connection.cursor()
        try:
            query = """
                INSERT INTO retos (
                    titulo, descripcion, categoria, estado,
                    fecha_creacion, fecha_entrega,
                    solicitante_id, responsable_id, observaciones
                )
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
                RETURNING id;
            """
            cursor.execute(query, (
                reto.titulo, reto.descripcion, reto.categoria, reto.estado,
                reto.fecha_creacion, reto.fecha_entrega,
                reto.solicitante_id, reto.responsable_id, reto.observaciones
            ))
            reto.id = cursor.fetchone()[0]
            connection.commit()
        except Exception as e:
            connection.rollback()
            raise e
        finally:
            cursor.close()
            db_config.release_connection(connection)

    def listar_todos(self):
        connection = db_config.get_connection()
        cursor = connection.cursor()
        try:
            cursor.execute("""
            SELECT 
                r.id,
                r.titulo,
                r.descripcion,
                r.categoria,
                r.estado,
                r.fecha_creacion,
                r.fecha_entrega,

                r.solicitante_id,
                u1.nombre_usuario AS solicitante_nombre,

                r.responsable_id,
                u2.nombre_usuario AS responsable_nombre,

                r.observaciones
            FROM retos r
            LEFT JOIN usuarios u1 ON r.solicitante_id = u1.id
            LEFT JOIN usuarios u2 ON r.responsable_id = u2.id
            ORDER BY r.id DESC;
        """)

            rows = cursor.fetchall()
            columnas = [desc[0] for desc in cursor.description]
            return [dict(zip(columnas, row)) for row in rows]
        finally:
            cursor.close()
            db_config.release_connection(connection)

    def obtener_por_id(self, reto_id: int):
        connection = db_config.get_connection()
        cursor = connection.cursor()
        try:
            cursor.execute("SELECT * FROM retos WHERE id = %s;", (reto_id,))
            row = cursor.fetchone()
            if not row:
                return None
            columnas = [desc[0] for desc in cursor.description]
            return dict(zip(columnas, row))
        finally:
            cursor.close()
            db_config.release_connection(connection)

    def filtrar_por_estado(self, estado: str):
        connection = db_config.get_connection()
        cursor = connection.cursor()
        try:
            cursor.execute("SELECT * FROM retos WHERE estado = %s;", (estado,))
            rows = cursor.fetchall()
            columnas = [desc[0] for desc in cursor.description]
            return [dict(zip(columnas, row)) for row in rows]
        finally:
            cursor.close()
            db_config.release_connection(connection)

    # 👇 NUEVOS MÉTODOS: asegúrate que estén dentro de la clase (con la misma indentación)
    def actualizar(self, reto: Reto):
        connection = db_config.get_connection()
        cursor = connection.cursor()
        try:
            query = """
                UPDATE retos
                SET titulo = %s,
                    descripcion = %s,
                    categoria = %s,
                    estado = %s,
                    fecha_entrega = %s,
                    responsable_id = %s,
                    observaciones = %s
                WHERE id = %s;
            """
            cursor.execute(query, (
                reto.titulo,
                reto.descripcion,
                reto.categoria,
                reto.estado,
                reto.fecha_entrega,
                reto.responsable_id,
                reto.observaciones,
                reto.id
            ))
            connection.commit()
            return cursor.rowcount
        except Exception as e:
            connection.rollback()
            raise e
        finally:
            cursor.close()
            db_config.release_connection(connection)

    def eliminar(self, reto_id: int):
        connection = db_config.get_connection()
        cursor = connection.cursor()
        try:
            cursor.execute("DELETE FROM retos WHERE id = %s;", (reto_id,))
            connection.commit()
            return cursor.rowcount
        except Exception as e:
            connection.rollback()
            raise e
        finally:
            cursor.close()
            db_config.release_connection(connection)

    def asignar_responsable(self, reto_id: int, responsable_id: int):
        connection = db_config.get_connection()
        cursor = connection.cursor()
        try:
            query = """
                UPDATE retos
                SET responsable_id = %s
                WHERE id = %s;
            """
            cursor.execute(query, (responsable_id, reto_id))
            connection.commit()
            return cursor.rowcount
        except Exception as e:
            connection.rollback()
            raise e
        finally:
            cursor.close()
            db_config.release_connection(connection)

    def usuario_existe(self, usuario_id: int):
        connection = db_config.get_connection()
        cursor = connection.cursor()
        try:
            cursor.execute("SELECT 1 FROM usuarios WHERE id = %s;", (usuario_id,))
            return cursor.fetchone() is not None
        finally:
            cursor.close()
            db_config.release_connection(connection)
    def registrar_auditoria(self, accion: str, descripcion: str, usuario_id: int):
        connection = db_config.get_connection()
        cursor = connection.cursor()
        try:
            query = """
                INSERT INTO auditoria (accion, descripcion, id_usuario)
                VALUES (%s, %s, %s);
            """
            cursor.execute(query, (accion, descripcion, usuario_id))
            connection.commit()
        except Exception as e:
            connection.rollback()
            raise e
        finally:
            cursor.close()
            db_config.release_connection(connection)
            
    def actualizar_estado(self, reto_id: int, nuevo_estado: str):
        connection = db_config.get_connection()
        cursor = connection.cursor()
        try:
            query = """
                UPDATE retos
                SET estado = %s
                WHERE id = %s;
            """
            cursor.execute(query, (nuevo_estado, reto_id))
            connection.commit()
            return cursor.rowcount
        except Exception as e:
            connection.rollback()
            raise e
        finally:
            cursor.close()
            db_config.release_connection(connection)

    def obtener_rol_usuario(self, usuario_id: int):
        connection = db_config.get_connection()
        cursor = connection.cursor()
        try:
            cursor.execute("SELECT rol FROM usuarios WHERE id = %s;", (usuario_id,))
            row = cursor.fetchone()
            return row[0] if row else None
        finally:
            cursor.close()
            db_config.release_connection(connection)
