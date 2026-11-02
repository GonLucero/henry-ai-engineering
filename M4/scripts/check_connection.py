"""Prueba mínima de OpenAI y Langfuse. Consume una llamada corta a la API."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from langfuse import Langfuse
from openai import OpenAI
from src.config import load_settings


def main():
    try:
        settings = load_settings()
    except ValueError as error:
        print(error, file=sys.stderr)
        return 1
    lf = Langfuse(
        public_key=settings["langfuse_public_key"],
        secret_key=settings["langfuse_secret_key"],
        base_url=settings["langfuse_base_url"],
        timeout=15,
    )
    try:
        if not lf.auth_check():
            print("Langfuse: no se pudo autenticar. Revisá claves y región.", file=sys.stderr)
            return 1
        print("Langfuse: autenticación correcta.")
        client = OpenAI(api_key=settings["openai_key"], timeout=30, max_retries=0)
        with lf.start_as_current_observation(name="connection-check", input="Prueba de conexión") as root:
            with lf.start_as_current_observation(
                name="openai-check", as_type="generation", model=settings["model"],
                input="Respondé únicamente OK.",
            ) as generation:
                response = client.chat.completions.create(
                    model=settings["model"],
                    messages=[{"role": "user", "content": "Respondé únicamente OK."}],
                    max_tokens=12,
                    temperature=0,
                )
                usage = response.usage
                generation.update(
                    output=response.choices[0].message.content,
                    usage_details={"input": usage.prompt_tokens, "output": usage.completion_tokens},
                )
            root.update(output="Conexión correcta")
            trace_id = lf.get_current_trace_id()
        lf.flush()
        print("OpenAI: llamada correcta con " + settings["model"] + ".")
        print("Tokens: " + str(usage.total_tokens))
        print("Traza enviada: " + str(trace_id))
        print("Buscá connection-check en Tracing de Langfuse para confirmar su recepción.")
        return 0
    except Exception as error:
        # No imprimimos excepciones completas porque pueden contener datos sensibles.
        status = getattr(error, "status_code", None)
        print("Falló la conexión: " + type(error).__name__ + (" (HTTP " + str(status) + ")" if status else ""), file=sys.stderr)
        return 1
    finally:
        lf.flush()


if __name__ == "__main__":
    raise SystemExit(main())
