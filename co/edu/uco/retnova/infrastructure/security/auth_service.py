from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthService:
    """Servicio para gestionar contraseñas y autenticación segura."""

    @staticmethod
    def hash_password(password: str) -> str:
        """Genera un hash seguro de la contraseña."""
        return pwd_context.hash(password)

    @staticmethod
    def verify_password(password: str, hashed_password: str) -> bool:
        """Verifica una contraseña contra su hash almacenado."""
        return pwd_context.verify(password, hashed_password)
