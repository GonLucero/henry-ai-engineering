# Ejemplos de ejecuciones reales

Resultados de los tres pares de imágenes y del control con documentos idénticos, obtenidos con los prompts afirmativos actuales y GPT-4o para visión y ambos agentes.

| Carpeta | Qué comprueba |
| --- | --- |
| `simple/` | Cambio de honorarios en una cláusula |
| `complejo/` | Modificaciones, eliminación y adición en varias cláusulas |
| `alquiler_sonido/` | Cambio de devolución y nuevo depósito reembolsable, conservando el precio |
| `sin_cambios/` | Listas vacías cuando se compara el mismo documento consigo mismo |

Cada carpeta conserva el reporte validado, las transcripciones, la ficha de correspondencias, las métricas y la comprobación remota de Langfuse. En los textos versionados se quitaron espacios finales para facilitar la lectura de cambios; las salidas originales se conservan en `outputs/`.

`prompts_version.json` registra las huellas de los archivos que contienen los prompts y las ejecuciones asociadas. Los criterios esperados se encuentran en `data/test_contracts/expected_changes.json`.

El caso de alquiler se probó por primera vez antes de esta reformulación; su evidencia histórica permanece en Git. Los ejemplos actuales corresponden a la nueva revisión de los tres pares, con la misma redacción afirmativa de los prompts para todos ellos.

Las trazas requieren acceso al proyecto de Langfuse. Los resultados de nuevas llamadas pueden variar. El informe de comprobación está en `docs/verificacion.md`.
