from fastapi import APIRouter, Depends, HTTPException
from co.edu.uco.retnova.infrastructure.security.auth_dependencies import auth_required
from co.edu.uco.retnova.infrastructure.persistence.auditoria_repository_postgres import AuditoriaRepositoryPostgres

router = APIRouter(prefix="/auditoria", tags=["Auditoria"])

@router.get("/")
def listar_auditoria(user=Depends(auth_required(["Administrador"]))):
    repo = AuditoriaRepositoryPostgres()
    try:
        return repo.listar_eventos()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al consultar auditoría: {e}")
