# Documentos de prueba — producción musical

Los documentos son ficticios y se generaron específicamente para este proyecto. No provienen de contratos reales ni de entregas de otros estudiantes. No constituyen modelos jurídicos para firmar.

| Caso | Original | Adenda | Resultado esperado |
| --- | --- | --- | --- |
| Simple | `simple/original.png` | `simple/adenda.png` | Solo cambia la cláusula 2: ARS 300.000 → ARS 360.000 |
| Complejo | `complejo/original.png` | `complejo/adenda.png` | Cambian las cláusulas 3, 4 y 5; se elimina la 6; se agrega la 7 |

Ambos casos parten del mismo contrato MUS-001. Cada adenda es independiente: el caso complejo se compara con el original, no con el resultado del caso simple.

Los `.txt` son las fuentes usadas para generar las imágenes y permiten revisar la fidelidad de la transcripción. El pipeline de análisis no los lee: recibe las imágenes y las transcribe con GPT-4o.

`expected_changes.json` contiene criterios de revisión preparados antes de ejecutar el modelo. La numeración puede aparecer en el reporte como `3` o `Cláusula 3`; se revisa el significado, no una redacción exacta.

Para regenerar las cuatro imágenes:

```bash
python scripts/generate_contracts.py
```

Para regenerar se necesita una fuente Arial o DejaVu Sans disponible en el sistema. Las imágenes ya incluidas no requieren instalar fuentes.

Son páginas digitales nítidas que simulan documentos escaneados. No demuestran rendimiento en fotos borrosas, manuscritos o documentos extensos.
