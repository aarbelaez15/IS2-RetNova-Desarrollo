import logging
import os
from datetime import datetime


class LoggerService:
    """
    Servicio de logging centralizado para RetNova.
    Registra eventos del sistema en archivos de log diarios.
    """

    _logger = None  # Instancia única (singleton)

    @classmethod
    def _inicializar_logger(cls):
        """Inicializa el logger si no existe."""
        if cls._logger is None:
            # Crear carpeta de logs si no existe
            os.makedirs("logs", exist_ok=True)

            # Nombre de archivo con fecha
            fecha_actual = datetime.now().strftime("%Y-%m-%d")
            archivo_log = os.path.join("logs", f"retnova_{fecha_actual}.log")

            # Configurar logger
            cls._logger = logging.getLogger("RetNovaLogger")
            cls._logger.setLevel(logging.INFO)

            # Evitar duplicados
            if not cls._logger.handlers:
                handler = logging.FileHandler(archivo_log, encoding="utf-8")
                formatter = logging.Formatter(
                    "%(asctime)s | %(levelname)s | %(message)s"
                )
                handler.setFormatter(formatter)
                cls._logger.addHandler(handler)

                # También imprimir en consola
                console_handler = logging.StreamHandler()
                console_handler.setFormatter(formatter)
                cls._logger.addHandler(console_handler)

        return cls._logger

    # ==========================================================
    # Métodos públicos
    # ==========================================================

    @classmethod
    def info(cls, mensaje: str):
        """Registra un mensaje informativo."""
        cls._inicializar_logger().info(mensaje)

    @classmethod
    def warning(cls, mensaje: str):
        """Registra una advertencia."""
        cls._inicializar_logger().warning(mensaje)

    @classmethod
    def error(cls, mensaje: str):
        """Registra un error."""
        cls._inicializar_logger().error(mensaje)

    @classmethod
    def critical(cls, mensaje: str):
        """Registra un error crítico."""
        cls._inicializar_logger().critical(mensaje)
