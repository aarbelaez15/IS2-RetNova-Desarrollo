# co/edu/uco/retnova/infrastructure/external/catalogo_parametros.py

class CatalogoParametros:
    """
    Catálogo centralizado de parámetros del sistema.
    Usado para roles, estados y categorías.
    """

    PARAMETROS = {
        "ROLES": ["Administrador", "Solicitante", "Lider", "Miembro"],
        "ESTADOS_RETO": ["Pendiente", "En progreso", "Finalizado", "Rechazado"],
        "CATEGORIAS": ["Reproceso", "Solicitud Inventario", "Cambio de cifras", "Retos nuevos"]
    }

    @staticmethod
    def obtener(tipo: str):
        return CatalogoParametros.PARAMETROS.get(tipo, [])

    @staticmethod
    def validar(tipo: str, valor: str):
        valores = CatalogoParametros.obtener(tipo)
        if valor not in valores:
            raise ValueError(f"El valor '{valor}' no es válido para {tipo}.")
