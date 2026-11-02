# Verificación — revisión con prompts afirmativos

Fecha: 2 de noviembre de 2026. Entorno: Python 3.12.16, con las dependencias fijadas en `requirements.txt`.

## Qué se modificó

Se reformularon las instrucciones de visión y ambos agentes para definir de forma afirmativa la tarea, las fuentes y el formato de salida. El contexto se organiza como una ficha de documentos, secciones, correspondencias, bloques exclusivos y referencias pendientes. La extracción conserva la comparación Antes/Después y los tres campos públicos.

Las condiciones de los contratos permanecen intactas, incluidas sus negaciones. Los identificadores de los campos públicos también se conservan. Se simplificaron la descripción del generador y la explicación de Langfuse en el README.

## Pruebas de código

La revisión final completó 22 tests offline. Cubren validación, archivos corruptos o incompatibles, transcripciones incompletas, traspaso de mapa y textos, salida JSON y manejo de fallos. La comprobación de contenido de las respuestas requiere la revisión adicional descrita abajo.

## Resultados con el modelo

Cada ejecución incluye dos transcripciones, contextualización y extracción. Las cuatro ejecuciones finales conservaron los resultados esperados.

| Caso | Secciones reportadas | Tokens | Duración | Costo estimado |
| --- | --- | --- | --- | --- |
| simple | 2 | 5663 | 11.9 s | USD 0.0200 |
| complejo | 3, 4, 5, 6, 7 | 6573 | 12.5 s | USD 0.0259 |
| alquiler_sonido | 3, 6 | 5927 | 12.2 s | USD 0.0219 |
| sin_cambios | ninguna | 6260 | 10.5 s | USD 0.0228 |

### Revisión de contenido

- Simple: cláusula 2, ARS 300.000 → ARS 360.000; conserva el pago 50%/50%.
- Complejo: cláusulas 3, 4 y 5 modificadas; cláusula 6 eliminada; cláusula 7 agregada. Preserva los valores anteriores/nuevos y las condiciones de uso del material, cancelación y confidencialidad.
- Alquiler: cláusula 3, devolución del 10 al 11 de noviembre de 2026 a las 18:00; cláusula 6, depósito de ARS 40.000 con reintegro dentro de 48 horas si se cumplen las condiciones indicadas. Conserva retiro y lugar. Distingue depósito y precio de alquiler.
- Control con documentos idénticos: listas vacías y resumen que indica equivalencia contractual.

También se revisaron las fichas de los tres pares: contienen identidad, inventario, correspondencias y etiquetas temáticas. La descripción de cambios queda a cargo del segundo agente.

## Fidelidad de visión

Se contrastaron las transcripciones finales con las fuentes del generador. El pipeline recibe las imágenes; las fuentes `.txt` sirven como referencia de revisión.

| Documento | Resultado |
| --- | --- |
| simple / original | Variación léxica: portfolio → portafolio |
| simple / adenda | Coincide al ignorar espacios y saltos de línea |
| complejo / original | Variación léxica: portfolio → portafolio |
| complejo / adenda | Coincide al ignorar espacios y saltos de línea |
| alquiler_sonido / original | Coincide al ignorar espacios y saltos de línea |
| alquiler_sonido / adenda | Coincide al ignorar espacios y saltos de línea |

En las transcripciones de los originales musicales persiste la variante “portafolio” para el texto fuente “portfolio”. Los importes, fechas y condiciones revisados se mantienen. En esta revisión final las adendas se transcribieron sin las marcas Markdown observadas en una ejecución anterior. Estas observaciones describen los casos preparados y requieren evaluación adicional para generalizar a otros documentos.

## Langfuse

Se verificaron remotamente las cuatro ejecuciones finales:

- Una raíz `contract-analysis` y seis etapas hijas.
- Cuatro generaciones bajo sus etapas correspondientes.
- Entradas, salidas, modelo, tokens y cierre de observaciones.
- Estado de las observaciones compatible con una ejecución exitosa.

La verificación usa un margen de espera acotado para que aparezcan los registros enviados en segundo plano. Los archivos `trace_audit.json` de cada ejemplo conservan las comprobaciones.

## Iteración y costo

La primera formulación afirmativa conservó los reportes esperados, pero algunas salidas del primer agente incluían cambios. Se precisó la ficha estructural y se repitieron los cuatro casos. Las comprobaciones finales respaldan la separación de responsabilidades en estos ejemplos.

El costo local estimado de las cuatro ejecuciones finales fue USD 0.0906. Incluyendo la primera iteración de esta reformulación, fue USD 0.1920. Son estimaciones de tokens a tarifa de referencia; la facturación definitiva depende del proveedor.

## Evidencia histórica y alcance

El archivo `data/test_contracts/alquiler_sonido/prompts_before_run.json` corresponde a la primera prueba de alquiler, realizada antes de reformular los prompts. Los hashes de la versión actual y sus ejemplos se encuentran en `examples/prompts_version.json`. Las versiones previas de resultados y documentación permanecen en el historial Git.

El alcance verificado comprende tres pares ficticios nítidos, de una imagen por documento, y un control con imágenes idénticas. Quedan pendientes evaluaciones de documentos reales, fotos degradadas, manuscritos, entradas adversariales y contratos extensos. Pydantic comprueba estructura; el contenido exige revisión humana.
