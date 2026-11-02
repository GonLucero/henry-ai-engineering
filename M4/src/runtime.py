"""Clientes, métricas y observabilidad de las etapas del análisis."""
from contextlib import contextmanager
from time import perf_counter
import os

from langfuse import Langfuse
from langchain_openai import ChatOpenAI
from openai import OpenAI

from src.errors import AnalysisError, explain_api_error


class Runtime:
    def __init__(self, settings):
        os.environ["LANGSMITH_TRACING"] = "false"
        os.environ["LANGCHAIN_TRACING_V2"] = "false"
        self.model = settings["model"]
        self.langfuse = Langfuse(
            public_key=settings["langfuse_public_key"],
            secret_key=settings["langfuse_secret_key"],
            base_url=settings["langfuse_base_url"],
            timeout=15,
        )
        self.openai = OpenAI(api_key=settings["openai_key"], timeout=60, max_retries=1)
        self.llm = ChatOpenAI(
            model=self.model, api_key=settings["openai_key"], temperature=0,
            timeout=60, max_retries=1, max_tokens=3000,
            # Desactiva el trazado independiente de LangSmith; usamos Langfuse.
        )
        self.calls = []

    def check_observability(self):
        try:
            valid = self.langfuse.auth_check()
        except Exception:
            raise AnalysisError("No se pudo conectar con Langfuse. Revisá conexión y región.") from None
        if not valid:
            raise AnalysisError("Langfuse rechazó las credenciales. Revisá claves y región.")

    @contextmanager
    def stage(self, name, inputs):
        started = perf_counter()
        with self.langfuse.start_as_current_observation(name=name, input=inputs) as span:
            try:
                yield span
            except Exception as error:
                message = str(error) if isinstance(error, AnalysisError) else "Error interno de la etapa"
                span.update(level="ERROR", status_message=message)
                raise
            finally:
                span.update(metadata={"latency_ms": round((perf_counter() - started) * 1000)})

    @contextmanager
    def generation(self, name, inputs):
        with self.langfuse.start_as_current_observation(
            name=name, as_type="generation", model=self.model,
            input=inputs, model_parameters={"temperature": 0, "max_retries": 1},
        ) as observation:
            try:
                yield observation
            except AnalysisError as error:
                observation.update(level="ERROR", status_message=str(error))
                raise
            except Exception as error:
                message = explain_api_error(error)
                observation.update(level="ERROR", status_message=message)
                raise AnalysisError(message) from None

    def record_usage(self, observation, name, usage, output):
        usage = usage or {}
        input_tokens = int(usage.get("input_tokens", usage.get("prompt_tokens", 0)))
        output_tokens = int(usage.get("output_tokens", usage.get("completion_tokens", 0)))
        details = {"input": input_tokens, "output": output_tokens}
        observation.update(output=output, usage_details=details)
        self.calls.append({"stage": name, "model": self.model, **details})

    def metrics(self):
        input_tokens = sum(call["input"] for call in self.calls)
        output_tokens = sum(call["output"] for call in self.calls)
        # Precio de referencia; no aplica descuentos de caché ni cuenta reintentos fallidos.
        cost = (input_tokens * 2.5 + output_tokens * 10) / 1_000_000 if self.model == "gpt-4o" else None
        return {
            "input_tokens": input_tokens, "output_tokens": output_tokens,
            "total_tokens": input_tokens + output_tokens,
            "estimated_cost_usd": cost, "calls": self.calls,
        }
