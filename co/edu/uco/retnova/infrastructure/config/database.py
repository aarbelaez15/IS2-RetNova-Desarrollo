import os
import psycopg2
from psycopg2 import pool

class DatabaseConfig:
    """Configura y gestiona el pool de conexiones a PostgreSQL."""

    def __init__(self):

        # ============================
        #  CONFIGURACIÓN HÍBRIDA
        # ============================
        # Railway -> usa variables de entorno
        # Local   -> usa valores por defecto

        db_user = os.getenv("PGUSER", "postgres")
        db_password = os.getenv("PGPASSWORD", "1234")
        db_host = os.getenv("PGHOST", "localhost")
        db_port = os.getenv("PGPORT", "5432")
        db_name = os.getenv("PGDATABASE", "retnova_db")

        # Crear pool de conexiones
        self.connection_pool = pool.SimpleConnectionPool(
            1, 10,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port,
            database=db_name
        )

    def get_connection(self):
        return self.connection_pool.getconn()

    def release_connection(self, connection):
        self.connection_pool.putconn(connection)

# Instancia global reutilizable
db_config = DatabaseConfig()