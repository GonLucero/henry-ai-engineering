"""Contrato público de salida, independiente de los prompts."""
from typing import List

from pydantic import BaseModel, ConfigDict, Field, field_validator


class ContractChangeOutput(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)

    sections_changed: List[str] = Field(
        description="Identificadores de las secciones modificadas, agregadas o eliminadas; lista vacía cuando las condiciones contractuales se mantienen."
    )
    topics_touched: List[str] = Field(
        description="Temas contractuales afectados por los cambios, en español."
    )
    summary_of_the_change: str = Field(
        description="Resumen en español de cada modificación, adición o eliminación, con condiciones anteriores y nuevas cuando estén disponibles."
    )

    @field_validator("summary_of_the_change")
    @classmethod
    def require_summary(cls, value):
        if not value.strip():
            raise ValueError("El resumen no puede estar vacío")
        return value.strip()

    @field_validator("sections_changed", "topics_touched")
    @classmethod
    def require_meaningful_items(cls, items):
        if any(not item.strip() for item in items):
            raise ValueError("Las listas no pueden contener textos vacíos")
        if len(set(items)) != len(items):
            raise ValueError("Las listas no pueden contener duplicados")
        return items
