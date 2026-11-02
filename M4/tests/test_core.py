"""Regresiones offline: no necesitan claves ni consumen saldo."""
from contextlib import contextmanager
import json
from pathlib import Path
from types import SimpleNamespace

from PIL import Image
from pydantic import ValidationError
import pytest

from src.errors import AnalysisError
from src.image_parser import parse_contract_image, validate_image
from src.models import ContractChangeOutput
import src.pipeline as pipeline
import src.main as cli


VALID = {
    "sections_changed": ["2"], "topics_touched": ["Honorarios"],
    "summary_of_the_change": "MODIFICACIÓN: honorarios de ARS 300.000 a ARS 360.000.",
}


class FakeSpan:
    def update(self, **kwargs):
        pass


class FakeRuntime:
    def __init__(self):
        self.model = "gpt-4o"
        self.events = []
        self.langfuse = SimpleNamespace(
            get_current_trace_id=lambda: "offline-trace",
            get_trace_url=lambda **kwargs: "https://example.test/trace/offline",
            flush=lambda: None,
        )

    @contextmanager
    def stage(self, name, inputs):
        self.events.append(name)
        yield FakeSpan()

    @contextmanager
    def generation(self, name, inputs):
        yield FakeSpan()

    def record_usage(self, *args):
        pass

    def metrics(self):
        return {"total_tokens": 0, "estimated_cost_usd": 0}

    def check_observability(self):
        pass


@pytest.fixture
def image_path(tmp_path):
    path = tmp_path / "contract.png"
    Image.new("RGB", (50, 80), "white").save(path)
    return path


def test_schema_accepts_empty_changes():
    result = ContractChangeOutput.model_validate({
        "sections_changed": [], "topics_touched": [],
        "summary_of_the_change": "No se identificaron cambios sustantivos.",
    })
    assert result.sections_changed == []


@pytest.mark.parametrize("bad", [
    {**VALID, "sections_changed": "2"},
    {**VALID, "topics_touched": [42]},
    {**VALID, "summary_of_the_change": "  "},
    {**VALID, "sections_changed": [""]},
    {**VALID, "sections_changed": ["2", "2"]},
    {**VALID, "extra": "no permitido"},
    {"sections_changed": ["2"]},
])
def test_schema_rejects_invalid_contract(bad):
    with pytest.raises(ValidationError):
        ContractChangeOutput.model_validate(bad)


def test_validate_image_reads_actual_format(image_path):
    info = validate_image(image_path)
    assert (info["format"], info["width"], info["height"]) == ("PNG", 50, 80)
    assert len(info["sha256"]) == 64


def test_corrupt_png_is_rejected(tmp_path):
    path = tmp_path / "bad.png"
    path.write_text("esto no es una imagen")
    with pytest.raises(AnalysisError, match="dañada"):
        validate_image(path)


def test_mismatched_extension_is_rejected(tmp_path):
    path = tmp_path / "fake.png"
    Image.new("RGB", (20, 20)).save(path, format="JPEG")
    with pytest.raises(AnalysisError, match="extensión"):
        validate_image(path)


def test_missing_file_is_rejected(tmp_path):
    with pytest.raises(AnalysisError, match="No existe"):
        validate_image(tmp_path / "missing.png")


def test_non_image_extension_is_rejected(tmp_path):
    path = tmp_path / "contract.pdf"
    path.write_text("pdf")
    with pytest.raises(AnalysisError, match="Formato"):
        validate_image(path)


def test_large_file_is_rejected_before_decoding(image_path, monkeypatch):
    monkeypatch.setattr("src.image_parser.MAX_IMAGE_BYTES", 1)
    with pytest.raises(AnalysisError, match="10 MB"):
        validate_image(image_path)


@pytest.mark.parametrize("text,finish,refusal", [
    ("texto parcial", "length", None),
    ("", "stop", None),
    ("Cláusula 2: [ILEGIBLE]", "stop", None),
    ("No", "stop", "refusal"),
])
def test_parser_rejects_unreliable_transcription(image_path, text, finish, refusal):
    runtime = FakeRuntime()
    response = SimpleNamespace(
        choices=[SimpleNamespace(finish_reason=finish, message=SimpleNamespace(content=text, refusal=refusal))],
        usage=None,
    )
    runtime.openai = SimpleNamespace(chat=SimpleNamespace(completions=SimpleNamespace(create=lambda **kwargs: response)))
    with pytest.raises(AnalysisError):
        parse_contract_image(image_path, runtime)


def test_invalid_second_image_stops_before_model_calls(image_path, tmp_path, monkeypatch):
    def forbidden(*args):
        pytest.fail("No debe llamarse al modelo si una imagen es inválida")
    monkeypatch.setattr(pipeline, "parse_contract_image", forbidden)
    with pytest.raises(AnalysisError):
        pipeline.analyze_contracts(image_path, tmp_path / "missing.png", FakeRuntime())


def test_pipeline_passes_map_and_both_sources_to_extractor(image_path, monkeypatch):
    texts = iter(["texto original", "texto adenda"])
    received = {}
    monkeypatch.setattr(pipeline, "parse_contract_image", lambda *args: next(texts))

    class Context:
        def __init__(self, runtime):
            pass
        def run(self, original, amendment):
            assert original == "texto original" and amendment == "texto adenda"
            return "mapa contextual"

    class Extract:
        def __init__(self, runtime):
            pass
        def run(self, original, amendment, context):
            received.update(original=original, amendment=amendment, context=context)
            return VALID

    monkeypatch.setattr(pipeline, "ContextualizationAgent", Context)
    monkeypatch.setattr(pipeline, "ExtractionAgent", Extract)
    runtime = FakeRuntime()
    result, evidence = pipeline.analyze_contracts(image_path, image_path, runtime)
    assert received == {"original": "texto original", "amendment": "texto adenda", "context": "mapa contextual"}
    assert result.model_dump() == VALID
    assert evidence["trace_id"] == "offline-trace"
    assert runtime.events[-1] == "output_validation"


def test_cli_keeps_stdout_machine_readable(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(cli, "load_settings", lambda: {})
    monkeypatch.setattr(cli, "Runtime", lambda settings: FakeRuntime())
    evidence = {
        "original_text": "original", "amendment_text": "adenda", "context_map": "mapa",
        "trace_id": "offline-trace", "metrics": {"total_tokens": 0, "latency_ms": 1, "estimated_cost_usd": 0},
    }
    monkeypatch.setattr(cli, "analyze_contracts", lambda *args: (ContractChangeOutput.model_validate(VALID), evidence))
    code = cli.main(["original.png", "adenda.png", "--output-dir", str(tmp_path)])
    output = capsys.readouterr()
    assert code == 0
    assert json.loads(output.out) == VALID
    assert "LegalMove" in output.err
    assert len(list(tmp_path.glob("*/report.json"))) == 1


def test_cli_failure_has_no_success_json_or_artifacts(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(cli, "load_settings", lambda: {})
    monkeypatch.setattr(cli, "Runtime", lambda settings: FakeRuntime())
    def fail(*args):
        raise AnalysisError("La imagen está dañada")
    monkeypatch.setattr(cli, "analyze_contracts", fail)
    code = cli.main(["original.png", "adenda.png", "--output-dir", str(tmp_path)])
    output = capsys.readouterr()
    assert code == 1
    assert output.out == ""
    assert "imagen está dañada" in output.err
    assert not list(tmp_path.iterdir())
