def mostrar_error_api(response_json):
    """
    Recibe la respuesta del backend y muestra mensajes amigables en Streamlit.
    """

    # Caso 1: Mensaje directo del backend
    if "error" in response_json and response_json["error"]:
        return response_json["error"]

    # Caso 2: Errores de validación (detalle)
    if "detalle" in response_json and isinstance(response_json["detalle"], list):
        # Mostrar solo el primer error
        err = response_json["detalle"][0]
        msg = err.get("msg", "Datos inválidos.")
        return f"Error: {msg}"

    # Caso inesperado
    return "Ocurrió un error inesperado. Intenta nuevamente."
