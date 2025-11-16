from co.edu.uco.retnova.infrastructure.helpers.email_helper import es_correo_corporativo
from co.edu.uco.retnova.infrastructure.external.catalogo_mensajes import CatalogoMensajes

class GestionUsuariosService:

    def validar_creacion(self, datos):

        if not datos.nombre_usuario or datos.nombre_usuario.strip() == "":
            raise ValueError(CatalogoMensajes.obtener("USUARIO_NOMBRE_OBLIGATORIO"))

        if not datos.email or datos.email.strip() == "":
            raise ValueError(CatalogoMensajes.obtener("USUARIO_EMAIL_OBLIGATORIO"))

        # 🔥 VALIDACIÓN DE EMAIL CORPORATIVO
        if not es_correo_corporativo(datos.email):
            raise ValueError(CatalogoMensajes.obtener("EMAIL_DOMINIO_NO_PERMITIDO"))

        if not datos.contrasena or datos.contrasena.strip() == "":
            raise ValueError(CatalogoMensajes.obtener("USUARIO_CONTRASENA_OBLIGATORIA"))
