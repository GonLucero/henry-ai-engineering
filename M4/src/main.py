"""CLI: dos imágenes → JSON validado y resumen en stderr."""
import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import sys
from uuid import uuid4

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from pydantic import ValidationError
from src.config import ROOT, load_settings
from src.errors import AnalysisError
from src.pipeline import analyze_contracts
from src.runtime import Runtime


def main(argv=None):
    parser = argparse.ArgumentParser(description="Compara las imágenes de un contrato original y su adenda.")
    parser.add_argument("original", type=Path, help="Contrato original PNG/JPEG")
    parser.add_argument("amendment", type=Path, help="Adenda PNG/JPEG")
    parser.add_argument("--json-only", action="store_true", help="Omite el resumen humano en stderr")
    parser.add_argument("--output-dir", type=Path, default=ROOT / "outputs", help="Carpeta para guardar cada ejecución")
    args = parser.parse_args(argv)
    runtime = None
    try:
        settings = load_settings()
        runtime = Runtime(settings)
        runtime.check_observability()
        result, evidence = analyze_contracts(args.original, args.amendment, runtime)
        # Una carpeta nueva por ejecución evita pisar resultados anteriores.
        run_name = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ") + "_" + uuid4().hex[:8]
        folder = args.output_dir / run_name
        folder.mkdir(parents=True, exist_ok=False)
        report_json = result.model_dump_json(indent=2)
        (folder / "report.json").write_text(report_json + "\n", encoding="utf-8")
        for name in ("original_text", "amendment_text", "context_map"):
            (folder / (name + ".txt")).write_text(evidence[name] + "\n", encoding="utf-8")
        trace_url = runtime.langfuse.get_trace_url(trace_id=evidence["trace_id"])
        run_info = {"trace_id": evidence["trace_id"], "trace_url": trace_url, **evidence["metrics"]}
        (folder / "run.json").write_text(json.dumps(run_info, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        runtime.langfuse.flush()
        # stdout conserva SOLO el contrato JSON para permitir redirecciones.
        print(report_json)
        if not args.json_only:
            print("\nLegalMove — análisis completado", file=sys.stderr)
            print("Secciones afectadas: " + (", ".join(result.sections_changed) or "ninguna"), file=sys.stderr)
            print("Temas: " + (", ".join(result.topics_touched) or "ninguno"), file=sys.stderr)
            print(result.summary_of_the_change, file=sys.stderr)
            print(f"Tokens: {run_info['total_tokens']} | Duración: {run_info['latency_ms'] / 1000:.1f} s", file=sys.stderr)
            cost = run_info["estimated_cost_usd"]
            if cost is not None:
                print(f"Costo estimado: USD {cost:.4f} (sin descuentos ni reintentos fallidos)", file=sys.stderr)
            print("Archivos: " + str(folder), file=sys.stderr)
            print("Langfuse: " + str(trace_url or evidence["trace_id"]), file=sys.stderr)
        return 0
    except (AnalysisError, ValueError) as error:
        if isinstance(error, ValidationError):
            message = "La salida no pasó la validación Pydantic. Revisá la traza."
        else:
            message = str(error)
        print("Error: " + message, file=sys.stderr)
        return 1
    except OSError:
        print("Error: no se pudieron leer o guardar los archivos. Revisá rutas y permisos.", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print("Análisis interrumpido.", file=sys.stderr)
        return 130
    except Exception as error:
        print("Error inesperado: " + type(error).__name__ + ". Revisá la configuración y la traza.", file=sys.stderr)
        return 1
    finally:
        if runtime is not None:
            runtime.langfuse.flush()


if __name__ == "__main__":
    raise SystemExit(main())
