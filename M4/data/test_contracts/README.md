# Documentos de prueba — producción musical y alquiler de sonido

Documentos ficticios creados para probar el pipeline. Los nombres, importes y condiciones forman parte de los casos de evaluación académica.

| Caso | Original | Adenda | Resultado esperado |
| --- | --- | --- | --- |
| Simple | `simple/original.png` | `simple/adenda.png` | Solo cambia la cláusula 2: ARS 300.000 → ARS 360.000 |
| Complejo | `complejo/original.png` | `complejo/adenda.png` | Cambian las cláusulas 3, 4 y 5; se elimina la 6; se agrega la 7 |
| Alquiler de sonido | `alquiler_sonido/original.png` | `alquiler_sonido/adenda.png` | Cambia la devolución en la cláusula 3 y se agrega el depósito de la cláusula 6; el precio no cambia |

Los dos casos musicales parten del mismo contrato MUS-001. Cada adenda es independiente: el caso complejo se compara con el original, no con el resultado del caso simple.

Los `.txt` son las fuentes usadas para generar las imágenes y permiten revisar la fidelidad de la transcripción. El pipeline de análisis no los lee: recibe las imágenes y las transcribe con GPT-4o.

`expected_changes.json` contiene criterios de revisión preparados antes de ejecutar el modelo. La numeración puede aparecer en el reporte como `3` o `Cláusula 3`; se revisa el significado, no una redacción exacta.

El caso de alquiler ALQ-001 se preparó después de ajustar los prompts musicales. Sus cambios esperados se definieron antes de ejecutarlo y los prompts se mantuvieron intactos. `alquiler_sonido/prompts_before_run.json` registra las huellas de los tres archivos de prompts anteriores a esa primera prueba. Esa evidencia es histórica; la reformulación posterior con instrucciones afirmativas se documenta en `../../docs/verificacion.md`. No es un conjunto de evaluación independiente a gran escala, sino un caso adicional de otro tipo de contrato.

Para regenerar las seis imágenes:

```bash
python scripts/generate_contracts.py
```

Para regenerar se necesita una fuente Arial o DejaVu Sans disponible en el sistema. Las imágenes ya incluidas no requieren instalar fuentes.

Son páginas digitales nítidas que simulan documentos escaneados. No demuestran rendimiento en fotos borrosas, manuscritos o documentos extensos.
