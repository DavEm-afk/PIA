## Propósito del uso de IA

La Inteligencia Artificial se utilizará en el proyecto con el propósito de generar un reporte final más claro, organizado y personalizado, basado en los resultados obtenidos por los módulos de análisis.
Su función es:

- Redactar un reporte entendible a partir de los datos procesados.
- Resaltar anomalías encontradas.
- Proporcionar recomendaciones simples basadas únicamente en los datos entregados.

Atribuye una facilidad en cuanto a la interpretación del analisis final.

## Punto del flujo donde se integra la IA

La IA se usa al final del pipeline, cuando ya se han completado los procesos técnicos:
- Adquisición de datos mediante un script de PowerShell.
- Análisis de hashes y procesos mediante scripts en Python.
- Detección de anomalías y marcado de archivos o procesos sospechosos.
- Generación del reporte con IA → (punto donde interviene la IA).

El uso en esta etapa garantiza que la IA reciba únicamente los datos filtrados, limpios y relevantes. Esto evita saturación a causa de un exceso de datos compartidos.

## Modelo/API utilizados

Se utilizará la API de OpenAI, empleando un modelo de generación de texto (GPT-3.5 en este caso).

## Ejemplo de prompt a utilizar:
Con los datos que se comparten a continuación:

{data}

genera un reporte personalizado enfocado en:
- detectar y explicar posibles anomalías (si las hay)
- describir riesgos potenciales asociados a procesos o archivos
- proporcionar recomendaciones básicas para mitigar problemas

El reporte debe ser conciso y basado únicamente en los datos proporcionados. No es necesario agregar ningun tipo de información adicional.
