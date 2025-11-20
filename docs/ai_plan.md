# Plan de uso de inteligencia artificial
## Este documento forma parte del tercer entregable del proyecto. Explica cómo se integrará IA en el flujo del proyecto, con fines éticos y funcionales.
---
## Propósito del uso de IA
La Inteligencia Artificial se utilizará en el proyecto con el propósito de generar un reporte final más claro, organizado y personalizado, basado en los resultados obtenidos por los módulos de análisis.
Su función es:

- Redactar un reporte entendible a partir de los datos procesados.
- Resaltar anomalías encontradas.
- Proporcionar recomendaciones simples basadas únicamente en los datos entregados.

Atribuye una facilidad en cuanto a la interpretación del analisis final.
---
## Punto del flujo donde se integra la IA

La IA se usa al final del pipeline, cuando ya se han completado los procesos técnicos:
- Adquisición de datos mediante un script de PowerShell.
- Análisis de hashes y procesos mediante scripts en Python.
- Detección de anomalías y marcado de archivos o procesos sospechosos.
- Generación del reporte con IA → (punto donde interviene la IA).

El uso en esta etapa garantiza que la IA reciba únicamente los datos filtrados y mas relevantes. Esto evita saturación a causa de un exceso de datos compartidos.

## Modelo/API utilizados

Nombre del modelo/API: OpenAI GPT-3.5 Turbo.

Tipo de acceso: Uso de API publica proporcionada.

Dependencias técnicas:

openai

JSON que se usará como formato de entrada para el prompt

Scripts en Python para leer archivos y enviar el prompt

Archivo de configuración del prompt:

`/prompts/prompt_v1.json`

## Diseño inicial del prompt
El prompt se utilizará para:

- Entregar al modelo los datos filtrados del sistema.
- Solicitar un reporte claro, donde lo primordial sería: buscar recomendaciones.
- Mantener control sobre el tono, formato y alcance de la respuesta.

Campos incluidos en /prompts/prompt_v1.json
"version": "1.0",
"tarea": "generacion_reporte",
"template": "Con los datos proporcionados a continuación:\n{data}\nGenera un reporte claro, organizado y con recomendaciones basadas únicamente en los datos.",
"instrucciones": "No es necesario inventar o agregar información externa. Analiza solamente los datos entregados."

## Consideraciones éticas
Para garantizar uso responsable:
- No se envía información personal, solo datos técnicos.
- Toda salida generada por IA se revisará en la integracion de reportes.
- El modelo no toma decisiones, solo redacta y organiza información existente.
- Se documenta cada ejecución por medio de logs.

## Observaciones
Se necesita de una correcta definición del prompt.

Se debe de buscar hacer un análisis de datos lo suficientemente compactos.
