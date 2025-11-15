# validators.py

def validar_min_length(value: str, min_len=3):
    if len(value) < min_len:
        raise ValueError(f"El valor debe tener al menos {min_len} caracteres.")
    return True

def validar_no_espacios(value: str):
    if " " in value:
        raise ValueError("El valor no puede contener espacios.")
    return True
