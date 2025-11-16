from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from datetime import datetime

class Reto:
    def __init__(self, id=None, titulo=None, descripcion=None, categoria=None, estado=None,
                 fecha_creacion=None, fecha_entrega=None, solicitante_id=None,
                 responsable_id=None, observaciones=None):
        self.id = id
        self.titulo = titulo
        self.descripcion = descripcion
        self.categoria = categoria
        self.estado = estado or "Pendiente"  
        self.fecha_creacion = fecha_creacion or datetime.now()
        self.fecha_entrega = fecha_entrega
        self.solicitante_id = solicitante_id
        self.responsable_id = responsable_id
        self.observaciones = observaciones
