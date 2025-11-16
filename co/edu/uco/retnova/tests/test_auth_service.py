from co.edu.uco.retnova.infrastructure.security.auth_service import AuthService

# 1️⃣ Contraseña original
password_original = "1234"

# 2️⃣ Encriptar la contraseña
hashed = AuthService.hash_password(password_original)
print(f"🔐 Hash generado: {hashed}")

# 3️⃣ Verificar contraseñas correctas e incorrectas
print("\n✅ Verificando con la contraseña correcta...")
print(AuthService.verify_password("1234", hashed))  # Debe imprimir True

print("\n❌ Verificando con contraseña incorrecta...")
print(AuthService.verify_password("9999", hashed))  # Debe imprimir False
