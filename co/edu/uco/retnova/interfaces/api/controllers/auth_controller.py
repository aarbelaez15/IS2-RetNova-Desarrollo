from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordRequestForm
from datetime import datetime, timedelta
import jwt

from co.edu.uco.retnova.infrastructure.config.database import db_config
from co.edu.uco.retnova.infrastructure.security.auth_service import AuthService
from co.edu.uco.retnova.infrastructure.security.auth_dependencies import auth_required
from co.edu.uco.retnova.infrastructure.external.catalogo_parametros import CatalogoParametros
from co.edu.uco.retnova.infrastructure.persistence.auditoria_repository_postgres import AuditoriaRepositoryPostgres
from co.edu.uco.retnova.app.dto.registro_usuario_dto import RegistroRequest

router = APIRouter(prefix="/auth", tags=["Autenticación"])



# ============================
# LOGIN
# ============================
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
            raise HTTPException(status_code=401, detail="Usuario no encontrado")

        user_id, nombre_usuario, contrasena_hash, rol, activo = usuario

        if not activo:
            raise HTTPException(status_code=403, detail="Usuario inactivo")

        if not AuthService.verify_password(form_data.password, contrasena_hash):
            raise HTTPException(status_code=401, detail="Contraseña incorrecta")

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


# ============================
# REGISTRAR USUARIO
# ============================
@router.post("/registrar")
def registrar_usuario(
    datos: RegistroRequest,
    user=Depends(auth_required(["Administrador"]))
):
    connection = db_config.get_connection()
    cursor = connection.cursor()

    try:
        CatalogoParametros.validar("ROLES", datos.rol)
        contrasena_hash = AuthService.hash_password(datos.contrasena)

        cursor.execute("SELECT id FROM usuarios WHERE email = %s;", (datos.email,))
        if cursor.fetchone():
            raise HTTPException(
                status_code=400,
                detail=f"El correo '{datos.email}' ya está registrado en el sistema."
            )
        
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

        return {"mensaje": "Usuario registrado correctamente", "usuario_id": usuario_id}

    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=500, detail=f"Error: {e}")

    finally:
        cursor.close()
        db_config.release_connection(connection)


# ============================
# ELIMINAR USUARIO
# ============================
@router.delete("/eliminar/{usuario_id}")
def eliminar_usuario(
    usuario_id: int,
    user=Depends(auth_required(["Administrador"]))
):
    connection = db_config.get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("SELECT id, nombre_usuario FROM usuarios WHERE id = %s;", (usuario_id,))
        usuario = cursor.fetchone()

        if not usuario:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")

        cursor.execute("DELETE FROM usuarios WHERE id = %s;", (usuario_id,))
        connection.commit()

        auditor = AuditoriaRepositoryPostgres()
        auditor.registrar_evento(
            user["sub"],
            "ELIMINAR_USUARIO",
            f"Administrador {user['sub']} eliminó al usuario ID {usuario_id}"
        )

        return {"mensaje": "Usuario eliminado correctamente"}

    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        cursor.close()
        db_config.release_connection(connection)


# ============================
# LISTAR USUARIOS (ADMIN)
# ============================
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

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        cursor.close()
        db_config.release_connection(connection)
