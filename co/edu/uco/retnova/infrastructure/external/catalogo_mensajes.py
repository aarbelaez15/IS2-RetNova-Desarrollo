class CatalogoMensajes:
    """Gestor centralizado de mensajes del sistema RetNova."""

    _mensajes = {
        # 🟢 General
        "OPERACION_EXITOSA": "Operación realizada exitosamente.",
        "ERROR_INTERNO": "Ocurrió un error interno en el sistema.",

        # 🟩 Retos
        "CREAR_RETO_OK": "El reto fue registrado correctamente.",
        "CREAR_RETO_ERROR": "Error al registrar el reto.",
        "ACTUALIZAR_RETO_OK": "El reto fue actualizado correctamente.",
        "ACTUALIZAR_RETO_ERROR": "Error al actualizar el reto.",
        "ELIMINAR_RETO_OK": "El reto fue eliminado correctamente.",
        "ELIMINAR_RETO_ERROR": "Error al eliminar el reto.",
        "CONSULTA_RETO_OK": "Consulta ejecutada exitosamente.",
        "CONSULTA_RETO_ERROR": "Error al realizar la consulta.",

        # 🔐 Autenticación y seguridad
        "TOKEN_INVALIDO": "Token de autenticación inválido.",
        "TOKEN_EXPIRADO": "El token ha expirado. Por favor inicie sesión nuevamente.",
        "ACCESO_DENEGADO": "Acceso denegado: no tiene los permisos requeridos.",
        "USUARIO_NO_AUTORIZADO": "El usuario no está autorizado para esta acción.",

        # 🧩 Auditoría
        "AUDITORIA_OK": "Evento registrado en el log de auditoría.",
        "AUDITORIA_ERROR": "Error al registrar el evento de auditoría.",

        # 🧠 Catálogos
        "PARAMETRO_INVALIDO": "El valor proporcionado no corresponde a los parámetros definidos.",

        "EMAIL_INVALIDO": "El correo ingresado no tiene un formato válido.",
        "EMAIL_DOMINIO_NO_PERMITIDO": "El dominio del correo no está permitido.",
        "EMAIL_DUPLICADO": "Este correo ya está registrado en el sistema.",
        "CONTRASENA_DEBIL": "La contraseña debe tener al menos 8 caracteres, incluir mayúsculas, números y un símbolo.",
        "USUARIO_DUPLICADO": "El nombre de usuario ya se encuentra registrado.",
        "VALIDACION_INTERNA": "La información enviada no cumple los requisitos del sistema.",
        "ERROR_DESCONOCIDO": "Ha ocurrido un error inesperado. Intenta nuevamente."
    }

    @classmethod
    def obtener(cls, clave: str) -> str:
        """Obtiene un mensaje por clave."""
        return cls._mensajes.get(clave, f"[MENSAJE_NO_DEFINIDO:{clave}]")

    @classmethod
    def agregar(cls, clave: str, mensaje: str):
        """Agrega un nuevo mensaje o reemplaza uno existente."""
        cls._mensajes[clave] = mensaje

    @classmethod
    def listar_todos(cls):
        """Devuelve todos los mensajes registrados."""
        return cls._mensajes
