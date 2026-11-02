# M1 — Integración de modelos y prompting

Estado: material de estudio en desarrollo. La implementación propia y su verificación están pendientes.

## Objetivo del proyecto

Construir una utilidad de texto que reciba una pregunta, consulte la API de OpenAI y devuelva JSON. Registrar tokens de entrada/salida, latencia y costo estimado. Documentar una técnica de prompting e incluir al menos un test automatizado.

## Conceptos

- Un system prompt define instrucciones; el mensaje del usuario contiene la consulta.
- Few-shot consiste en proporcionar ejemplos de entrada y salida para orientar la respuesta.
- JSON válido no garantiza que estén todos los campos esperados ni que el contenido sea correcto.
- Los tokens son unidades de procesamiento; el costo depende del modelo y del consumo de entrada y salida.
- La latencia mide cuánto tarda una operación. Puede medirse con un reloj monotónico.
- Las claves se leen del entorno y no se versionan.

## Recorrido previsto

Pregunta → armado de mensajes → llamada al modelo → validación → respuesta JSON y métricas.

## Pendientes

- [ ] Implementar el script de consulta y el esquema de salida.
- [ ] Preparar un prompt con ejemplos few-shot.
- [ ] Registrar una ejecución real con métricas.
- [ ] Agregar un test de validación y el informe breve.

## Aplicación en M4

Llamadas a la API, prompts especializados, manejo de errores y métricas. M4 agrega validación con Pydantic y entradas de imagen.

## Referencias

Consigna M1PI de Henry provista en el campus.
Material docente: https://github.com/Ivan-Cepeda/primeros_pasos_ai_engineer
Caso alternativo: https://github.com/Ivan-Cepeda/IA-Engineer-M1-Orbitair-case
