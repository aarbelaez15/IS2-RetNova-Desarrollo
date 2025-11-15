import jwt
from datetime import datetime, timedelta
from fastapi import HTTPException, status

class IdentityProviderService:
    """Servicio simulado de autenticación con JWT."""

    SECRET_KEY = "SuperClaveSecreta"
    ALGORITHM = "HS256"
    EXPIRATION_MINUTES = 60

    @classmethod
    def generar_token(cls, usuario_id: int, rol: str):
        """Genera un token JWT con el ID de usuario y su rol."""
        payload = {
            "sub": str(usuario_id),  # importante: debe ser string
            "rol": rol,
            "exp": datetime.utcnow() + timedelta(minutes=cls.EXPIRATION_MINUTES),
            "iat": datetime.utcnow()
        }
        token = jwt.encode(payload, cls.SECRET_KEY, algorithm=cls.ALGORITHM)
        return token

    @classmethod
    def validar_token(cls, token: str):
        """Valida y decodifica el token JWT."""
        try:
            payload = jwt.decode(token, cls.SECRET_KEY, algorithms=[cls.ALGORITHM])
            return payload
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="El token ha expirado"
            )
        except jwt.InvalidTokenError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido"
            )

    # 👇 NUEVO: obtener usuario actual desde token
    @staticmethod
    def obtener_usuario_actual(token_data: dict) -> int:
        """
        Retorna el ID del usuario autenticado (campo 'sub' del token).
        """
        if not token_data or "sub" not in token_data:
            raise HTTPException(status_code=401, detail="Token inválido o faltante")

        try:
            return int(token_data["sub"])
        except ValueError:
            raise HTTPException(status_code=400, detail="ID de usuario no válido en token")
