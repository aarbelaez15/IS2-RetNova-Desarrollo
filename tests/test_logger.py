from co.edu.uco.retnova.infrastructure.logging.logger_service import LoggerService

def test_logger_no_explota():
    # No validamos la salida, solo que no genere excepciones
    LoggerService.info("Mensaje info")
    LoggerService.warning("Mensaje warning")
    LoggerService.error("Mensaje error")
    LoggerService.critical("Mensaje critical")

    assert True  # Si llegó aquí, el logger funciona
