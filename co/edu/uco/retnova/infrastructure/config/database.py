import os
from psycopg2 import pool

class DatabaseConfig:
    """Configura y gestiona el pool de conexiones a PostgreSQL."""

    def __init__(self):

        # Detectar si estamos en Railway
        is_railway = os.getenv("RAILWAY_ENVIRONMENT") is not None

        if is_railway:
            # Configuración para Railway
            self.connection_pool = pool.SimpleConnectionPool(
                1, 10,
                user=os.getenv("PGUSER"),
                password=os.getenv("PGPASSWORD"),
                host=os.getenv("PGHOST"),
                port=os.getenv("PGPORT"),
                database=os.getenv("PGDATABASE")
            )
        else:
            # Configuración LOCAL (tu máquina)
            self.connection_pool = pool.SimpleConnectionPool(
                1, 10,
                user="postgres",
                password="1234",
                host="localhost",
                port="5432",
                database="retnova_db"
            )

    def get_connection(self):
        return self.connection_pool.getconn()

    def release_connection(self, connection):
        self.connection_pool.putconn(connection)

# Instancia global reutilizable.
db_config = DatabaseConfig()