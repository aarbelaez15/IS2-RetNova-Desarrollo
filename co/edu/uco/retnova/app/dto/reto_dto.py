from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class RetoDTO(BaseModel):
    """DTO para transferencia de datos del Reto entre capas."""
    id: Optional[int] = None
    titulo: str
    descripcion: str
    categoria: str
    estado: Optional[str] = "Pendiente"
    fecha_creacion: Optional[datetime] = None
    fecha_entrega: datetime
    solicitante_id: int
    responsable_id: Optional[int] = None
    observaciones: Optional[str] = None
