# M2 — Embeddings y RAG

Estado: material de estudio en desarrollo. No hay un pipeline RAG propio implementado ni resultados verificados.

## Objetivo del proyecto

Construir un chatbot de FAQs basado en un documento de al menos 1000 palabras. Generar al menos 20 fragmentos significativos, crear sus embeddings y recuperar los relevantes para responder con un LLM.

## Conceptos

- Chunking divide documentos en fragmentos. El tamaño y el solapamiento afectan qué información puede recuperarse.
- Un embedding representa texto mediante un vector numérico.
- La búsqueda vectorial recupera fragmentos cercanos al vector de la pregunta. La similitud no demuestra que el fragmento responda la consulta.
- RAG combina recuperación de información y generación de una respuesta con ese contexto.
- Debe usarse un modelo de embeddings compatible para documentos y preguntas; cambiarlo requiere revisar y normalmente reconstruir el índice.
- Si los fragmentos no aportan evidencia suficiente, el sistema debería reconocer la limitación.

## Dos recorridos

Indexación: documento → chunks → embeddings → almacenamiento.

Consulta: pregunta → embedding → búsqueda → contexto recuperado → LLM → JSON.

La salida solicitada incluye `user_question`, `system_answer` y `chunks_related`.

## Pendientes

- [ ] Preparar el documento de FAQs.
- [ ] Implementar fragmentación e indexación.
- [ ] Implementar recuperación y generación.
- [ ] Verificar al menos tres consultas y guardar sus resultados.
- [ ] Documentar decisiones de chunking y búsqueda.

## Relación con M4

La consigna de comparación de contratos no exige RAG ni una base vectorial. Trabaja con los dos documentos suministrados en cada ejecución.

## Referencias

Consigna M2PI de Henry provista en el campus.
Material docente: https://github.com/Ivan-Cepeda/ai-engineer-lab
