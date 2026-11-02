# Verificación — 2 de noviembre de 2026

## Entorno y pruebas de código

Python 3.12.16. Dependencias directas fijadas en `requirements.txt`; se comprobó la compatibilidad de los paquetes instalados. La ejecución offline final completó 22 tests sin llamadas al modelo.

## Ejecuciones con imágenes

Se ejecutaron los dos pares completos usando GPT-4o en las cuatro llamadas por ejecución: dos transcripciones, contextualización y extracción. Los ejemplos conservados corresponden a los prompts finales.

| Caso | Secciones reportadas | Tokens totales | Duración del pipeline | Costo estimado |
| --- | --- | --- | --- | --- |
| Simple | 2 | 6002 | 10.7 s | USD 0.0226 |
| Complejo | 3, 4, 5, 6, 7 | 6935 | 13.9 s | USD 0.0286 |

Los valores de costo son estimaciones locales sin descuentos de caché ni reintentos fallidos; no son un comprobante de facturación.

### Revisión del caso simple

- Reporta únicamente la cláusula 2.
- Identifica precio anterior ARS 300.000 y nuevo ARS 360.000.
- Conserva la forma de pago 50% al inicio y 50% al entregar.
- No considera eliminadas las cláusulas no mencionadas.

### Revisión del caso complejo

- Identifica las cláusulas 3, 4, 5, 6 y 7.
- Compara 30 y 45 días corridos desde el mismo punto de inicio.
- Compara dos y tres rondas, y siete y diez días para pedir cada ronda.
- Conserva en el resumen la titularidad del artista y distingue el permiso anterior de la nueva prohibición de publicar fragmentos o usar grabaciones en portfolio.
- Reporta la eliminación explícita de cancelación, sin inventar una cláusula alternativa.
- Reporta la incorporación de confidencialidad por 12 meses desde la firma, sobre pistas y mezclas no publicadas.
- No atribuye cambios a las cláusulas 1 y 2. La ausencia de una mención a nuevas grabaciones en el resumen no implica que haya cambiado la exclusión original.

El campo de temas del caso complejo usa la categoría compuesta “titularidad y uso del material”. La titularidad en sí no cambia; el resumen sí lo distingue. Es una limitación de granularidad de la categorización, no una modificación de titularidad.

## Fidelidad de la transcripción

Se contrastaron las fuentes `.txt` del generador y los textos leídos de las imágenes. No se usaron las fuentes de texto como entrada del pipeline.

| Documento | Comparación |
| --- | --- |
| Simple / original | Presenta diferencias; ver nota de transcripción |
| Simple / adenda | Presenta diferencias; ver nota de transcripción |
| Complejo / original | Presenta diferencias; ver nota de transcripción |
| Complejo / adenda | Coincide al ignorar espacios y saltos de línea |

En los originales se observó la sustitución de “portfolio” por “portafolio”, aun con una instrucción de transcripción literal. No altera las condiciones del ejemplo, pero demuestra que no debe afirmarse una transcripción idéntica carácter por carácter. La adenda compleja coincide al ignorar espacios y saltos de línea. La transcripción de la adenda simple agregó marcas Markdown de apertura y cierre de un bloque de código, aunque el texto contractual dentro del bloque coincide al ignorar espacios. El parser conserva esas marcas en la evidencia; no alteraron los cambios detectados en este caso. Ningún resultado de estos dos casos mide precisión general en documentos reales.

## Trazas remotas

Se consultaron las dos trazas finales mediante la API de Langfuse y se comprobaron:

- Una raíz `contract-analysis`.
- Seis etapas hijas: validación de imágenes, ambas transcripciones, contextualización, extracción y validación de salida.
- Cuatro generaciones, cada una bajo la etapa correcta.
- Entradas, salidas, modelo, tokens y cierre de las observaciones, sin nivel ERROR.

Los mapas finales organizan correspondencias sin enumerar importes anteriores/nuevos ni redactar el reporte de cambios. La etapa de extracción recibe el mapa y los textos completos.

Los registros de comprobación se guardaron junto a los ejemplos como `trace_audit.json`. No se reemplaza la demostración del dashboard durante la defensa.

## Iteraciones de desarrollo

Se ajustaron los prompts después de observar temas demasiado amplios, un resumen que abreviaba una prohibición y correspondencias que describían operaciones de cambio. Se repitieron los casos afectados. También se reforzó la literalidad de visión; la variación léxica indicada arriba persiste.

En total quedaron registradas 9 ejecuciones completas de desarrollo, incluido el control adicional, con un costo local estimado acumulado de USD 0.2269, además de la prueba mínima de conexión.

## Control adicional sin cambios

Se pasó `data/test_contracts/simple/original.png` como ambos argumentos. El reporte devolvió listas vacías y señaló que no hay cambios sustantivos. Es un control negativo, no un tercer par de contrato/adenda distinto.

Consumo: 6683 tokens; duración: 14.9 segundos; costo local estimado: USD 0.0258. También se verificó su traza remota completa. La evidencia está en `examples/sin_cambios/`.

## Límites de la evidencia

Dos pares ficticios, nítidos y de una página. No se evaluaron fotos borrosas, manuscritos, PDFs, contratos extensos ni precisión jurídica. Los tests offline comprueban código y contratos de datos; no validan la veracidad de respuestas nuevas. Se requiere revisión humana del contenido.
