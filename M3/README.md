# M3 — Orquestación y observabilidad

Estado: material de estudio en desarrollo. El sistema multiagente por departamentos y sus trazas están pendientes.

## Objetivo del proyecto

Clasificar consultas y dirigirlas mediante LangChain a un agente RAG especializado. Implementar al menos tres dominios, un mínimo de 50 chunks por dominio y diez consultas con intención esperada. Registrar el workflow con Langfuse.

## Conceptos

- Un orquestador controla el recorrido de una consulta.
- El routing condicional selecciona una rama según la intención identificada.
- La especialización de un agente depende de sus instrucciones, contexto, herramientas y responsabilidad; no exige un modelo distinto por agente.
- LangChain proporciona componentes para organizar las llamadas y el flujo de datos.
- Una traza agrupa una ejecución; los spans representan operaciones dentro de ella.
- La observabilidad permite inspeccionar entradas, salidas, tiempos y errores. Tener una traza no demuestra que la respuesta sea correcta.
- La evaluación contrasta resultados con criterios y ejemplos preparados previamente.

## Recorrido previsto

Pregunta → clasificación → agente de HR / tecnología / finanzas → recuperación → respuesta.

Langfuse debe permitir seguir el recorrido completo y localizar fallos de clasificación, recuperación o generación.

## Pendientes

- [ ] Preparar documentos para tres dominios.
- [ ] Implementar los agentes RAG y el routing con LangChain.
- [ ] Preparar diez consultas con categorías esperadas y casos borde.
- [ ] Instrumentar el flujo con Langfuse y revisar trazas reales.
- [ ] Documentar instalación, uso y limitaciones.

## Aplicación en M4

M4 usa dos agentes en secuencia: contextualización y extracción. Reutiliza orquestación y trazabilidad, pero no requiere el routing por departamentos de este proyecto.

## Referencias

Consigna M3PI de Henry provista en el campus.
Material de observabilidad: https://github.com/Ivan-Cepeda/AI-Observability
