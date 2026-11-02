"""Configuración local y carga de credenciales desde el entorno."""
import os
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[1]


def load_settings():
    load_dotenv(ROOT / ".env", override=False)
    required = ("OPENAI_API_KEY", "LANGFUSE_PUBLIC_KEY", "LANGFUSE_SECRET_KEY")
    missing = [name for name in required if not os.getenv(name, "").strip()]
    if missing:
        raise ValueError("Faltan variables en .env: " + ", ".join(missing))
    base_url = os.getenv("LANGFUSE_BASE_URL") or os.getenv("LANGFUSE_HOST")
    if not base_url:
        raise ValueError("Falta LANGFUSE_BASE_URL en .env")
    return {
        "openai_key": os.environ["OPENAI_API_KEY"],
        "model": os.getenv("OPENAI_MODEL", "gpt-4o"),
        "langfuse_public_key": os.environ["LANGFUSE_PUBLIC_KEY"],
        "langfuse_secret_key": os.environ["LANGFUSE_SECRET_KEY"],
        "langfuse_base_url": base_url,
    }
