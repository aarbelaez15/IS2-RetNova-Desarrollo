from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordRequestForm
from datetime import datetime, timedelta
import jwt
from co.edu.uco.retnova.domain.services.gestion_usuarios_service import GestionUsuariosService
from co.edu.uco.retnova.infrastructure.config.database import db_config
from co.edu.uco.retnova.infrastructure.security.auth_service import AuthService
from co.edu.uco.retnova.infrastructure.security.auth_dependencies import auth_required
from co.edu.uco.retnova.infrastructure.external.catalogo_parametros import CatalogoParametros
from co.edu.uco.retnova.infrastructure.external.catalogo_mensajes import CatalogoMensajes
from co.edu.uco.retnova.infrastructure.persistence.auditoria_repository_postgres import AuditoriaRepositoryPostgres
from co.edu.uco.retnova.app.dto.registro_usuario_dto import RegistroRequest

router = APIRouter(prefix="/auth", tags=["Autenticación"])

servicio_usuarios = GestionUsuariosService()
@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    connection = db_config.get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("""
            SELECT id, nombre_usuario, contrasena, rol, activo 
            FROM usuarios 
            WHERE nombre_usuario = %s
        """, (form_data.username,))
        usuario = cursor.fetchone()

        if not usuario:
            raise HTTPException(401, CatalogoMensajes.obtener("LOGIN_USUARIO_NO_ENCONTRADO"))

        user_id, nombre_usuario, contrasena_hash, rol, activo = usuario

        if not activo:
            raise HTTPException(403, CatalogoMensajes.obtener("LOGIN_USUARIO_INACTIVO"))

        if not AuthService.verify_password(form_data.password, contrasena_hash):
            raise HTTPException(401, CatalogoMensajes.obtener("LOGIN_CONTRASENA_INCORRECTA"))

        payload = {
            "sub": str(user_id),
            "rol": rol,
            "exp": datetime.utcnow() + timedelta(hours=2),
            "iat": datetime.utcnow(),
        }

        token = jwt.encode(payload, "SuperClaveSecreta", algorithm="HS256")

        return {
            "access_token": token,
            "token_type": "bearer",
            "usuario": {
                "id": user_id,
                "nombre_usuario": nombre_usuario,
                "rol": rol,
            },
        }

    finally:
        cursor.close()
        db_config.release_connection(connection)



@router.post("/registrar")
def registrar_usuario(datos: RegistroRequest, user=Depends(auth_required(["Administrador"]))):
    connection = db_config.get_connection()
    cursor = connection.cursor()

    try:
        servicio_usuarios.validar_creacion(datos)
        CatalogoParametros.validar("ROLES", datos.rol)

        contrasena_hash = AuthService.hash_password(datos.contrasena)

        cursor.execute("SELECT id FROM usuarios WHERE email = %s;", (datos.email,))
        if cursor.fetchone():
            raise HTTPException(400, CatalogoMensajes.obtener("USUARIO_EMAIL_DUPLICADO"))

        cursor.execute("""
            INSERT INTO usuarios (nombre_usuario, email, contrasena, rol, activo, fecha_creacion)
            VALUES (%s, %s, %s, %s, TRUE, NOW())
            RETURNING id;
        """, (datos.nombre_usuario, datos.email, contrasena_hash, datos.rol))

        usuario_id = cursor.fetchone()[0]
        connection.commit()

        auditor = AuditoriaRepositoryPostgres()
        auditor.registrar_evento(
            user["sub"],
            "CREAR_USUARIO",
            f"Usuario '{datos.nombre_usuario}' creado por el administrador {user['sub']}"
        )

        return {"mensaje": CatalogoMensajes.obtener("USUARIO_REGISTRADO_OK"), "usuario_id": usuario_id}

    except HTTPException:
        connection.rollback()
        raise

    except ValueError as e:
        connection.rollback()
        raise HTTPException(400, str(e))

    except Exception:
        connection.rollback()
        raise HTTPException(500, CatalogoMensajes.obtener("ERROR_INTERNO"))

    finally:
        cursor.close()
        db_config.release_connection(connection)


@router.delete("/eliminar/{usuario_id}")
def eliminar_usuario(usuario_id: int, user=Depends(auth_required(["Administrador"]))):
    connection = db_config.get_connection()
    cursor = connection.cursor()

    try:
        # 🚫 VALIDACIÓN: no permitir que el administrador se elimine a sí mismo
        if usuario_id == int(user["sub"]):
            raise HTTPException(404, CatalogoMensajes.obtener("PROPIO_USUARIO_NO_ELIMINABLE"))

        cursor.execute("SELECT id, nombre_usuario FROM usuarios WHERE id = %s;", (usuario_id,))
        usuario = cursor.fetchone()

        if not usuario:
            raise HTTPException(404, CatalogoMensajes.obtener("USUARIO_NO_ENCONTRADO"))

        cursor.execute("DELETE FROM usuarios WHERE id = %s;", (usuario_id,))
        connection.commit()

        auditor = AuditoriaRepositoryPostgres()
        auditor.registrar_evento(
            user["sub"],
            "ELIMINAR_USUARIO",
            f"Administrador {user['sub']} eliminó al usuario ID {usuario_id}"
        )

        return {"mensaje": CatalogoMensajes.obtener("USUARIO_ELIMINADO_OK")}

    except HTTPException as e:
        connection.rollback()
        raise e

    except Exception as e:
        connection.rollback()
        raise HTTPException(500, CatalogoMensajes.obtener("ERROR_INTERNO"))

    finally:
        cursor.close()
        db_config.release_connection(connection)


@router.put("/activar/{usuario_id}")
def activar_usuario(usuario_id: int, user=Depends(auth_required(["Administrador"]))):
    connection = db_config.get_connection()
    cursor = connection.cursor()

    try:
        # Verificar si existe
        cursor.execute("SELECT id, activo FROM usuarios WHERE id = %s;", (usuario_id,))
        usuario = cursor.fetchone()

        if not usuario:
            raise HTTPException(404, "Usuario no encontrado.")

        _, activo = usuario

        if activo:
            raise HTTPException(400, "El usuario ya está activo.")

        # Activar
        cursor.execute("""
            UPDATE usuarios SET activo = TRUE WHERE id = %s;
        """, (usuario_id,))
        connection.commit()

        # Registrar auditoría
        auditor = AuditoriaRepositoryPostgres()
        auditor.registrar_evento(
            user["sub"],
            "ACTIVAR_USUARIO",
            f"El administrador {user['sub']} activó al usuario {usuario_id}"
        )

        return {"mensaje": "Usuario activado correctamente."}

    except HTTPException:
        connection.rollback()
        raise

    except Exception:
        connection.rollback()
        raise HTTPException(500, "Error interno del servidor.")

    finally:
        cursor.close()
        db_config.release_connection(connection)


@router.put("/desactivar/{usuario_id}")
def desactivar_usuario(usuario_id: int, user=Depends(auth_required(["Administrador"]))):
    connection = db_config.get_connection()
    cursor = connection.cursor()

    try:
        # 1️⃣ Evitar que un usuario se desactive a sí mismo
        if usuario_id == user["sub"]:
            raise HTTPException(400, "No puedes desactivarte a ti mismo.")

        # 2️⃣ Verificar si el usuario es administrador (no desactivable)
        cursor.execute("SELECT id, rol, activo FROM usuarios WHERE id = %s;", (usuario_id,))
        usuario = cursor.fetchone()

        if not usuario:
            raise HTTPException(404, "Usuario no encontrado.")

        _, rol, activo = usuario

        if rol == "Administrador":
            raise HTTPException(400, "No se puede desactivar a un administrador.")

        if not activo:
            raise HTTPException(400, "El usuario ya está inactivo.")

        # 3️⃣ Desactivar usuario
        cursor.execute("UPDATE usuarios SET activo = FALSE WHERE id = %s;", (usuario_id,))
        connection.commit()

        # 4️⃣ Auditoría
        auditor = AuditoriaRepositoryPostgres()
        auditor.registrar_evento(
            user["sub"],
            "DESACTIVAR_USUARIO",
            f"El administrador {user['sub']} desactivó al usuario {usuario_id}"
        )

        return {"mensaje": "Usuario desactivado correctamente."}

    except HTTPException:
        connection.rollback()
        raise

    except Exception:
        connection.rollback()
        raise HTTPException(500, "Error interno del servidor.")

    finally:
        cursor.close()
        db_config.release_connection(connection)

@router.get("/usuarios")
def listar_usuarios(user=Depends(auth_required(["Administrador", "Lider"]))):
    connection = db_config.get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("""
            SELECT id, nombre_usuario, email, rol, activo, fecha_creacion
            FROM usuarios
            ORDER BY id ASC
        """)
        rows = cursor.fetchall()
        columnas = [desc[0] for desc in cursor.description]
        return [dict(zip(columnas, r)) for r in rows]

    except Exception:
        raise HTTPException(500, CatalogoMensajes.obtener("ERROR_INTERNO"))

    finally:
        cursor.close()
        db_config.release_connection(connection)
