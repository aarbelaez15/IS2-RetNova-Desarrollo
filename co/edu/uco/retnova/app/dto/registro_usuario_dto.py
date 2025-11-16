from pydantic import BaseModel, EmailStr, field_validator
from co.edu.uco.retnova.infrastructure.helpers.email_helper import es_correo_corporativo

class RegistroRequest(BaseModel):
    nombre_usuario: str
    email: EmailStr
    contrasena: str
    rol: str


