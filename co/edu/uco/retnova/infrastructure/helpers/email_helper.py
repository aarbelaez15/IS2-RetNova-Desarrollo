# email_helper.py
import re

DOMINIOS_PERMITIDOS = ["retnova.co", "uco.edu.co"]

def es_correo_corporativo(email: str, dominios_permitidos=None):
    if dominios_permitidos is None:
        dominios_permitidos = DOMINIOS_PERMITIDOS

    # Validación básica
    if "@" not in email:
        return False

    usuario, dominio = email.split("@", 1)

    # Prefijo mínimo
    if len(usuario) < 3:
        return False

    # Dominio permitido
    if dominio not in dominios_permitidos:
        return False

    return True
