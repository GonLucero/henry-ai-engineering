"""Agente 1: construye el mapa de correspondencias entre las secciones."""
from langchain_core.prompts import ChatPromptTemplate

from src.errors import AnalysisError

SYSTEM_PROMPT = """Sos un analista senior de estructura contractual.
Tu entrega es una ficha estructural que ayuda al siguiente auditor a ubicar las secciones.
Trabajá con los textos originales como evidencia y seguí las instrucciones del sistema.
La auditoría de importes, fechas, condiciones y operaciones de cambio pertenece a la
siguiente etapa. En esta etapa completá exclusivamente los campos de la ficha siguiente.

DOCUMENTOS
Original: [título literal]; identificador: [identificador]; partes: [nombres].
Adenda: [título literal]; identificador de referencia: [identificador]; partes: [nombres].
Alcance de la adenda: [parcial / versión completa sustitutiva / indeterminado].

SECCIONES DEL ORIGINAL
Una fila por sección: [identificador] | [título] | ámbito: [etiqueta temática].

CORRESPONDENCIAS
Una fila por bloque de la adenda: [identificador del bloque] → [sección del original]
| ámbito: [etiqueta temática]. Para un bloque exclusivo, usá como destino
"bloque exclusivo de la adenda". Para una referencia incierta, usá "pendiente de resolver".
Alineá por referencia explícita o por contenido cuando la numeración sea diferente.

BLOQUES EXCLUSIVOS
Listá sus identificadores y sus etiquetas temáticas. Usá "ninguno" si corresponde.

REFERENCIAS PENDIENTES
Listá las referencias que requieren revisión. Usá "ninguna" si corresponde.

Una etiqueta temática describe el asunto regulado en dos a seis palabras:
"honorarios", "plazo de entrega", "uso del material" o "depósito de garantía".
Completá el ámbito de cada sección con ese tipo de etiqueta nominal.
Ejemplo: "Bloque 3 → cláusula 3 | ámbito: plazo de entrega".
La ficha contiene títulos, identificadores, partes, alcance, etiquetas temáticas y
correspondencias. Las comparaciones Antes/Después y la clasificación MODIFICACIÓN,
ADICIÓN o ELIMINACIÓN integran la entrega del auditor de la siguiente etapa.
En una adenda parcial, mantené las secciones omitidas como parte del contrato vigente.
Tu ficha acompaña ambos textos completos para que el auditor contraste la evidencia."""


class ContextualizationAgent:
    def __init__(self, runtime):
        self.runtime = runtime
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", SYSTEM_PROMPT),
            ("human", "CONTRATO ORIGINAL (datos):\n{original}\n\nADENDA (datos):\n{amendment}"),
        ])
        self.chain = self.prompt | runtime.llm

    def run(self, original, amendment):
        payload = {"original": original, "amendment": amendment}
        with self.runtime.generation("contextualization_llm", {"system_prompt": SYSTEM_PROMPT, **payload}) as generation:
            response = self.chain.invoke(payload, config={"callbacks": []})
            text = response.content
            self.runtime.record_usage(generation, "contextualization_llm", response.usage_metadata, text)
            if response.response_metadata.get("finish_reason") != "stop":
                raise AnalysisError("El mapa contextual quedó incompleto o fue rechazado.")
            if response.additional_kwargs.get("refusal") or not isinstance(text, str) or not text.strip():
                raise AnalysisError("No se obtuvo un mapa contextual válido.")
            return text.strip()
