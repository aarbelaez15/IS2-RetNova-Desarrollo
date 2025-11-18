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
        "NO_ENCONTRADO_RETO": "No se encontraron retos que coincidan con los criterios proporcionados.",
        # 🟦 Estados de reto
        "ESTADO_INVALIDO": "El estado proporcionado no es válido para un reto.",
        "CAMBIAR_ESTADO_OK": "El estado del reto fue actualizado correctamente.",
        "CAMBIAR_ESTADO_ERROR": "Error al intentar actualizar el estado del reto.",

        "RETO_TITULO_DESCRIPCION_OBLIGATORIO": "El reto debe tener título y descripción.",
        "RETO_FECHA_ENTREGA_FUTURA": "La fecha de entrega debe ser futura.",
        "RETO_FINALIZAR_SIN_FECHA": "No se puede finalizar un reto sin fecha de entrega.",


        # 🟩 Usuario
        "CREAR_USUARIO_OK": "El usuario fue registrado correctamente.",
        "CREAR_USUARIO_ERROR": "Error al registrar el usuario.",
        "ACTUALIZAR_USUARIO_OK": "El usuario fue actualizado correctamente.",
        "ACTUALIZAR_USUARIO_ERROR": "Error al actualizar el usuario.",
        "NO_ENCONTRADO_USUARIO": "No se encontraron usuarios que coincidan con los criterios proporcionados.",
        "PROPIO_USUARIO_NO_ELIMINABLE": "No se puede eliminar el propio usuario.",

        # 🟩 Asignación de responsable
        "ASIGNAR_RESPONSABLE_OK": "El responsable del reto fue asignado correctamente.",
        "ASIGNAR_RESPONSABLE_ERROR": "Ocurrió un error al asignar el responsable del reto.",


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
        "ERROR_DESCONOCIDO": "Ha ocurrido un error inesperado. Intenta nuevamente.",

        "LOGIN_USUARIO_NO_ENCONTRADO": "Usuario no encontrado.",
        "LOGIN_USUARIO_INACTIVO": "El usuario está inactivo.",
        "LOGIN_CONTRASENA_INCORRECTA": "La contraseña ingresada es incorrecta.",
        "USUARIO_EMAIL_DUPLICADO": "El correo ya se encuentra registrado.",
        "USUARIO_REGISTRADO_OK": "Usuario registrado correctamente",
        "USUARIO_ELIMINADO_OK": "Usuario eliminado correctamente.",
        "USUARIO_NO_ENCONTRADO": "No se encontró el usuario especificado.",
        "ERROR_INTERNO": "Ha ocurrido un error inesperado en el sistema.",

        "USUARIO_NOMBRE_OBLIGATORIO": "El nombre de usuario es obligatorio.",
        "USUARIO_EMAIL_OBLIGATORIO": "El email es obligatorio.",
        "USUARIO_CONTRASENA_OBLIGATORIA": "La contraseña es obligatoria.",
        "ASIGNAR_RESPONSABLE_ROL_INVALIDO": "Solo se puede asignar un reto a un usuario con rol Miembro.",
        "USUARIO_DESACTIVADO_OK": "El usuario ha sido desactivado correctamente.",
        "USUARIO_YA_INACTIVO": "El usuario ya se encuentra inactivo.",
        "USUARIO_NO_SE_PUEDE_DESACTIVAR_ADMIN": "No está permitido desactivar al usuario Administrador principal.",


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
