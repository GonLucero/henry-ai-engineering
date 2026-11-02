# Ejemplos de ejecuciones reales

Estas carpetas conservan salidas de las dos ejecuciones finales, con GPT-4o para visión y ambos agentes. No son respuestas simuladas.

Cada carpeta contiene el reporte validado, las dos transcripciones, el mapa contextual y las métricas locales. Para facilitar la lectura de cambios en Git, se quitaron espacios al final de las líneas de los archivos de texto; las salidas originales se conservan en `outputs/`. `trace_audit.json` registra la comprobación de recepción remota y jerarquía realizada mediante la API de Langfuse. Los identificadores no hacen públicas las trazas: su consulta requiere acceso al proyecto.

Los criterios preparados antes de las ejecuciones están en `data/test_contracts/expected_changes.json`. Los resultados y las limitaciones observadas están en `docs/verificacion.md`.

Una nueva llamada al modelo puede producir otra redacción y otro consumo. Estos ejemplos no garantizan precisión sobre otros documentos.
