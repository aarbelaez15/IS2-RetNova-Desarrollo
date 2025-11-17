from co.edu.uco.retnova.infrastructure.security.auth_service import AuthService

def test_password_hashing_and_verification():
    password_original = "1234"

    # Generar hash
    hashed = AuthService.hash_password(password_original)

    # Verificar contraseña correcta
    assert AuthService.verify_password("1234", hashed) is True

    # Verificar contraseña incorrecta
    assert AuthService.verify_password("9999", hashed) is False
