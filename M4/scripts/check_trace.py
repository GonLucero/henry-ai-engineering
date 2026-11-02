"""Verifica en Langfuse la jerarquía y las cuatro generaciones de una ejecución."""
import argparse
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from langfuse import Langfuse
from src.config import load_settings


EXPECTED_STAGES = {
    "validate_images", "parse_original_contract", "parse_amendment_contract",
    "contextualization_agent", "extraction_agent", "output_validation",
}
EXPECTED_GENERATIONS = {
    "parse_original_contract": "vision_transcription",
    "parse_amendment_contract": "vision_transcription",
    "contextualization_agent": "contextualization_llm",
    "extraction_agent": "extraction_llm",
}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("run_folder", type=Path, help="Carpeta de outputs que contiene run.json")
    args = parser.parse_args()
    try:
        info = json.loads((args.run_folder / "run.json").read_text())
        settings = load_settings()
        client = Langfuse(
            public_key=settings["langfuse_public_key"], secret_key=settings["langfuse_secret_key"],
            base_url=settings["langfuse_base_url"], timeout=15,
        )
        response = client.api.observations.get_many(
            trace_id=info["trace_id"], fields="core,basic,io,model,usage,metrics", limit=100,
        )
        observations = [item.model_dump(by_alias=True, mode="json") for item in response.data]
        roots = [item for item in observations if item.get("name") == "contract-analysis" and not item.get("parentObservationId")]
        if len(roots) != 1:
            raise ValueError("No se encontró exactamente una raíz contract-analysis")
        root = roots[0]
        stages = {item["name"]: item for item in observations if item.get("parentObservationId") == root["id"]}
        if not EXPECTED_STAGES.issubset(stages):
            raise ValueError("Faltan etapas en la traza remota")
        generations = [item for item in observations if item.get("type") == "GENERATION"]
        if len(generations) != 4:
            raise ValueError("Se esperaban cuatro generaciones del modelo")
        for stage, name in EXPECTED_GENERATIONS.items():
            found = [g for g in generations if g.get("parentObservationId") == stages[stage]["id"] and g.get("name") == name]
            if len(found) != 1:
                raise ValueError("Una generación no está bajo la etapa esperada: " + stage)
        for item in observations:
            if item.get("level") == "ERROR" or item.get("endTime") is None:
                raise ValueError("Hay observaciones incompletas o con error")
            if not item.get("input") or not item.get("output"):
                raise ValueError("Faltan entradas o salidas en una observación")
        for item in generations:
            usage = item.get("usageDetails") or {}
            if usage.get("input", 0) <= 0 or usage.get("output", 0) <= 0 or not item.get("model"):
                raise ValueError("Faltan métricas de uso o modelo")
        audit = {
            "trace_id": info["trace_id"], "verified": True,
            "observations": len(observations), "model_generations": len(generations),
            "stages": sorted(stages),
            "generations": [{"name": g["name"], "model": g["model"], "usage": g["usageDetails"], "latency_seconds": g.get("latency")} for g in generations],
        }
        (args.run_folder / "trace_audit.json").write_text(json.dumps(audit, ensure_ascii=False, indent=2) + "\n")
        print("Traza remota verificada: raíz, seis etapas, cuatro generaciones, entradas/salidas y tokens.")
        return 0
    except Exception as error:
        message = str(error) if isinstance(error, (ValueError, FileNotFoundError)) else type(error).__name__
        print("No se pudo verificar la traza: " + message, file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
