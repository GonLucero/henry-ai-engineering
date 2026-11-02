# Ejemplos de ejecuciones reales

Estas carpetas conservan salidas de los casos musicales simple y complejo, del alquiler de sonido y de un control negativo con dos imágenes idénticas, con GPT-4o para visión y ambos agentes. No son respuestas simuladas.

Cada carpeta contiene el reporte validado, las dos transcripciones, el mapa contextual y las métricas locales. Para facilitar la lectura de cambios en Git, se quitaron espacios al final de las líneas de los archivos de texto; las salidas originales se conservan en `outputs/`. `trace_audit.json` registra la comprobación de recepción remota y jerarquía realizada mediante la API de Langfuse. Los identificadores no hacen públicas las trazas: su consulta requiere acceso al proyecto.

Los criterios preparados antes de las ejecuciones están en `data/test_contracts/expected_changes.json`. Los resultados y las limitaciones observadas están en `docs/verificacion.md`.

Una nueva llamada al modelo puede producir otra redacción y otro consumo. Estos ejemplos no garantizan precisión sobre otros documentos.

## Control sin cambios

`sin_cambios/` usa `data/test_contracts/simple/original.png` en ambos argumentos. No es una adenda real: permite comprobar que el sistema no fabrique diferencias ante documentos idénticos. Devolvió listas vacías y se verificó su traza remota.

## Alquiler de sonido

`alquiler_sonido/` conserva la primera ejecución de este nuevo par. Se definieron los cambios esperados y se registraron las huellas de los prompts antes de probarlo. Sin ajustarlos, el reporte identificó únicamente las secciones 3 y 6. No confundió el depósito reembolsable con un aumento de precio.
