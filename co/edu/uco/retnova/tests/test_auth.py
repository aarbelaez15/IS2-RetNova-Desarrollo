from co.edu.uco.retnova.infrastructure.external.identity_provider_service import IdentityProviderService

# Simula un usuario con rol "Solicitante"
token = IdentityProviderService.generar_token(usuario_id=1, rol="Solicitante")

print("\n🟢 Token generado:\n", token)

# Verificamos que sea válido
payload = IdentityProviderService.validar_token(token)
print("\n📦 Payload decodificado:", payload)
