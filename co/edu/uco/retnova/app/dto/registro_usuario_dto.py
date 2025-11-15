from pydantic import BaseModel, EmailStr, field_validator
from co.edu.uco.retnova.infrastructure.helpers.email_helper import es_correo_corporativo

class RegistroRequest(BaseModel):
    nombre_usuario: str
    email: EmailStr
    contrasena: str
    rol: str

    @field_validator("email")
    def validar_correo_empresa(cls, v):
        # DEBUG opcional (puedes quitarlo después)
        print("VALIDANDO EMAIL DESDE DTO:", v)

        if not es_correo_corporativo(v):
            raise ValueError(
                "El correo no cumple los requisitos corporativos: "
                "mínimo 3 caracteres antes del @ y dominio autorizado."
            )

        return v
