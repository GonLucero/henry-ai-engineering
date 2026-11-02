"""Errores que la terminal puede mostrar sin exponer credenciales."""

class AnalysisError(Exception):
    pass


def explain_api_error(error):
    status = getattr(error, "status_code", None)
    name = type(error).__name__
    if status == 401:
        return "OpenAI rechazó la clave. Revisá OPENAI_API_KEY."
    if status == 429:
        return "OpenAI limitó la solicitud. Revisá saldo y límites de uso."
    if "Timeout" in name:
        return "La llamada al modelo superó el tiempo de espera."
    if "Connection" in name:
        return "No se pudo conectar con el servicio del modelo."
    if status == 404:
        return "El modelo solicitado no está disponible para esta cuenta."
    return f"Falló la llamada al modelo ({name}). Revisá la configuración y la traza."
