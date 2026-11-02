"""Orden explícito del pipeline y traza raíz."""
from time import perf_counter

from src.agents.contextualization_agent import ContextualizationAgent
from src.agents.extraction_agent import ExtractionAgent
from src.errors import AnalysisError
from src.image_parser import parse_contract_image, validate_image
from src.models import ContractChangeOutput


def analyze_contracts(original_path, amendment_path, runtime):
    started = perf_counter()
    with runtime.stage("contract-analysis", {"original": original_path.name, "amendment": amendment_path.name}) as root:
        with runtime.stage("validate_images", {"original": original_path.name, "amendment": amendment_path.name}) as span:
            # Ambas se validan antes de consumir la primera llamada a OpenAI.
            original_info = validate_image(original_path)
            amendment_info = validate_image(amendment_path)
            span.update(output={"original": original_info, "amendment": amendment_info})
        with runtime.stage("parse_original_contract", original_info) as span:
            original = parse_contract_image(original_path, runtime)
            span.update(output=original)
        with runtime.stage("parse_amendment_contract", amendment_info) as span:
            amendment = parse_contract_image(amendment_path, runtime)
            span.update(output=amendment)
        if len(original) + len(amendment) > 50_000:
            raise AnalysisError("Los textos exceden el límite local de 50.000 caracteres.")
        with runtime.stage("contextualization_agent", {"original": original, "amendment": amendment}) as span:
            context = ContextualizationAgent(runtime).run(original, amendment)
            span.update(output=context)
        with runtime.stage("extraction_agent", {"original": original, "amendment": amendment, "context": context}) as span:
            extracted = ExtractionAgent(runtime).run(original, amendment, context)
            span.update(output=extracted)
        with runtime.stage("output_validation", extracted) as span:
            result = ContractChangeOutput.model_validate(extracted)
            span.update(output=result.model_dump())
        root.update(output=result.model_dump())
        trace_id = runtime.langfuse.get_current_trace_id()
        metrics = runtime.metrics()
        metrics["latency_ms"] = round((perf_counter() - started) * 1000)
        return result, {
            "original_text": original, "amendment_text": amendment,
            "context_map": context, "metrics": metrics, "trace_id": trace_id,
        }
