from fastapi import APIRouter, HTTPException, Depends
from co.edu.uco.retnova.app.dto.reto_dto import RetoDTO
from co.edu.uco.retnova.app.use_cases.registrar_reto_use_case import RegistrarRetoUseCase
from co.edu.uco.retnova.app.use_cases.consultar_retos_use_case import ConsultarRetosUseCase
from co.edu.uco.retnova.app.use_cases.actualizar_eliminar_reto_use_case import ActualizarEliminarRetoUseCase
from co.edu.uco.retnova.app.use_cases.asignar_responsable_use_case import AsignarResponsableUseCase
from co.edu.uco.retnova.app.use_cases.cambiar_estado_reto_use_case import CambiarEstadoRetoUseCase
from co.edu.uco.retnova.infrastructure.security.auth_dependencies import auth_required

router = APIRouter(prefix="/retos", tags=["Retos"])


# ============================
# REGISTRAR RETO
# ============================
@router.post("/registrar")
def registrar_reto(reto_dto: RetoDTO, user=Depends(auth_required(["Solicitante"]))):
    usuario_actual = int(user["sub"])
    reto_dto.solicitante_id = usuario_actual
    use_case = RegistrarRetoUseCase()
    resultado = use_case.ejecutar(reto_dto)
    return {"mensaje": "Reto registrado correctamente", "data": resultado}


# ============================
# LISTAR RETOS
# ============================
@router.get("/listar")
def listar_retos(user=Depends(auth_required(["Administrador", "Lider", "Miembro", "Solicitante"]))):
    use_case = ConsultarRetosUseCase()
    return use_case.listar_todos()


# ============================
# OBTENER RETO POR ID
# ============================
@router.get("/{reto_id}")
def obtener_reto(reto_id: int, user=Depends(auth_required(["Administrador", "Lider", "Miembro", "Solicitante"]))):
    use_case = ConsultarRetosUseCase()
    return use_case.obtener_por_id(reto_id)


# ============================
# FILTRAR POR ESTADO
# ============================
@router.get("/estado/{estado}")
def listar_por_estado(estado: str, user=Depends(auth_required(["Administrador", "Lider", "Miembro", "Solicitante"]))):
    use_case = ConsultarRetosUseCase()
    return use_case.filtrar_por_estado(estado)


# ============================
# ACTUALIZAR
# ============================
@router.put("/actualizar/{reto_id}")
def actualizar_reto(reto_id: int, reto: RetoDTO, user=Depends(auth_required(["Lider", "Miembro"]))):
    reto.id = reto_id
    use_case = ActualizarEliminarRetoUseCase()
    return use_case.actualizar(reto)


# ============================
# ELIMINAR
# ============================
@router.delete("/eliminar/{reto_id}")
def eliminar_reto(reto_id: int, user=Depends(auth_required(["Administrador", "Lider"]))):
    usuario_id = int(user["sub"])
    use_case = ActualizarEliminarRetoUseCase()
    return use_case.eliminar(reto_id, usuario_id)



# ============================
# ASIGNAR RESPONSABLE (LÍDER)
# ============================
@router.put("/asignar-responsable/{reto_id}/{responsable_id}")
def asignar_responsable(reto_id: int, responsable_id: int, user=Depends(auth_required(["Lider"]))):
    lider_id = int(user["sub"])
    use_case = AsignarResponsableUseCase()
    return use_case.ejecutar(reto_id, responsable_id, lider_id)


# ============================
# CAMBIAR ESTADO (LÍDER / MIEMBRO )
# ============================
@router.put("/cambiar-estado/{reto_id}/{nuevo_estado}")
def cambiar_estado(reto_id: int, nuevo_estado: str, user=Depends(auth_required(["Lider", "Miembro"]))):
    usuario_id = int(user["sub"])
    use_case = CambiarEstadoRetoUseCase()
    return use_case.ejecutar(reto_id, nuevo_estado, usuario_id)
