from co.edu.uco.retnova.infrastructure.security.auth_service import AuthService

def test_password_hash_and_verify():
    password = "mi_clave_segura"
    hash_pw = AuthService.hash_password(password)

    assert AuthService.verify_password(password, hash_pw) is True
    assert AuthService.verify_password("otra_clave", hash_pw) is False
