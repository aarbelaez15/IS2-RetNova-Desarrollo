# string_helper.py

def normalizar_texto(texto: str) -> str:
    return texto.strip().lower()

def es_vacio(texto: str) -> bool:
    return texto.strip() == ""
