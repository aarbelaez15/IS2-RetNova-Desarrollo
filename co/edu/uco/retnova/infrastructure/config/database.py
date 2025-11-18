import os
from psycopg2 import pool, OperationalError

class DatabaseConfig:
    """Configura y gestiona el pool de conexiones a PostgreSQL."""

    def __init__(self):
        # No crear el pool aquí
        self.connection_pool = None

    def _create_pool(self):
        """Crea el pool dependiendo del entorno."""
        is_railway = os.getenv("RAILWAY_ENVIRONMENT") is not None

        try:
            if is_railway:
                # Configuración para Railway
                return pool.SimpleConnectionPool(
                    1, 10,
                    user=os.getenv("PGUSER"),
                    password=os.getenv("PGPASSWORD"),
                    host=os.getenv("PGHOST"),
                    port=os.getenv("PGPORT"),
                    database=os.getenv("PGDATABASE")
                )
            else:
                # Configuración LOCAL (tu máquina)
                return pool.SimpleConnectionPool(
                    1, 10,
                    user="postgres",
                    password="1234",
                    host="localhost",
                    port="5432",
                    database="retnova_db"
                )

        except OperationalError:
            # Dejar que el middleware capture este error cuando ocurra en un request
            raise

    def get_connection(self):
        # Crear pool solo cuando se necesite
        if self.connection_pool is None:
            self.connection_pool = self._create_pool()

        return self.connection_pool.getconn()

    def release_connection(self, connection):
        if self.connection_pool:
            self.connection_pool.putconn(connection)


# Instancia global reutilizable (segura ahora)
db_config = DatabaseConfig()
