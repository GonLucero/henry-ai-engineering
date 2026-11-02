# Recorrido del proyecto y preparación de la demo

## El problema, explicado sin código

Un contrato fija condiciones. Una adenda modifica algunas de ellas. LegalMove recibe una imagen de cada documento, los lee y presenta los cambios en datos que otro programa puede procesar.

El dominio de los ejemplos es producción musical. En el caso simple cambian los honorarios. En el complejo cambian plazos, revisiones y uso del material, se elimina cancelación y se agrega confidencialidad. Los casos son independientes. Un tercer par de alquiler de equipos de sonido comprueba cambio de devolución y adición de depósito, sin aumento del precio. Fue evaluado después de ajustar los prompts musicales, sin modificarlos para ese caso.

## Qué hace cada parte

1. `main.py` recibe dos rutas desde la terminal y carga la configuración.
2. `validate_image()` comprueba ambos archivos antes de consumir llamadas al modelo.
3. `parse_contract_image()` codifica una imagen en base64 y solicita a GPT-4o una transcripción. Base64 representa bytes como texto: no lee ni cifra el contrato.
4. `ContextualizationAgent` recibe los dos textos y construye un mapa: qué secciones hay y cómo se corresponden. Su entrega se concentra en el inventario, las correspondencias y el propósito de cada sección.
5. `ExtractionAgent` recibe ese mapa Y los dos textos. El mapa orienta; las fuentes respaldan la comparación. Devuelve los tres campos del esquema.
6. `ContractChangeOutput` verifica los datos con Pydantic. Esa validación comprueba estructura, no verdad jurídica.
7. El programa guarda evidencia local, imprime JSON y muestra un resumen breve por stderr.
8. Langfuse registra toda la ejecución. El dashboard permite inspeccionar las etapas ejecutadas por el programa de Python.

## Las herramientas

- Python conecta las piezas.
- OpenAI aporta el modelo que interpreta las imágenes y produce respuestas.
- LangChain es la biblioteca que arma los mensajes y las cadenas de los agentes.
- Pydantic es la biblioteca que define y valida los datos.
- Langfuse recibe registros del programa y permite investigar cómo se obtuvo la respuesta.

En este proyecto, agente significa un componente especializado con instrucciones y lógica propias. El orden de ejecución de los componentes es fijo y explícito.

## Demo sugerida

1. Mostrar las imágenes del caso simple y anticipar qué debería cambiar.
2. Ejecutar el comando del README y revisar sección 2, precio anterior y nuevo.
3. Mostrar el caso complejo y comprobar cláusulas 3, 4, 5, 6 y 7.
4. Abrir el enlace que muestra la terminal en Langfuse.
5. Expandir `contract-analysis`, una transcripción, contextualización, extracción y validación.
6. Mostrar que el extractor recibió el mapa y las dos fuentes; ubicar tokens y duración en una generación.
7. Mostrar qué ocurre con un path inexistente. No debe producir un reporte exitoso.

## Preguntas para practicar

**¿Por qué dos agentes?** La consigna lo exige y permite separar alineación y extracción para inspeccionarlas. No afirmamos que mejoren la precisión sin medirlo frente a un solo agente.

**¿Por qué GPT-4o?** Lo exige el parsing de la consigna y admite imágenes. Se mantiene el mismo modelo en los agentes para simplificar la configuración.

**¿Por qué no RAG?** Los dos documentos se reciben completos en la ejecución; no hace falta recuperar información de una colección externa para este alcance.

**¿Qué pasa si una cláusula no aparece en la adenda?** Si la adenda es parcial, la omisión no prueba eliminación. El agente tiene una regla explícita al respecto.

**¿Cómo sé que funciona?** Hay tests offline para el código y tres pares de imágenes con resultados esperados escritos previamente. Debemos revisar el contenido del reporte y la transcripción; no basta con que el JSON sea válido.

**¿Qué ocurre con una imagen ilegible?** Si la transcripción contiene `[ILEGIBLE]`, se detiene y se solicita una imagen más clara o revisión humana. El modelo puede no marcar todos los errores visuales: la regla no garantiza detectar toda ilegibilidad.

**¿Cómo manejo errores de API?** Timeout y un reintento de transporte, mensajes de error sin claves y salida con código distinto de cero. No se fabrica una respuesta correcta si algo falló.

**¿Qué límites tiene?** Documentos de una imagen, ejemplos ficticios nítidos, sin garantía de precisión jurídica ni resistencia absoluta a instrucciones maliciosas en documentos.
