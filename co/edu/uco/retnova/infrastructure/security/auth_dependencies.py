from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
import jwt

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def auth_required(roles_permitidos: list):
    def wrapper(token: str = Depends(oauth2_scheme)):
        try:
            payload = jwt.decode(token, "SuperClaveSecreta", algorithms=["HS256"])
            if payload["rol"] not in roles_permitidos:
                raise HTTPException(status_code=403, detail="No tiene permisos para acceder a este recurso")
            return payload
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token expirado")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail="Token inválido")
    return wrapper
