# Plan de uso de IA en el proyecto

La IA se utilizará al final del proceso de analisis, sería el punto donde se tienen los datos filtrados, logrando asi una mayor precision y no saturando a la inteligencia artificial con demasiados datos innecesarios. La idea es que la IA ayude a escribir un reporte más claro, personalizado y con recomendaciones basadas en lo que realmente encontró el sistema.

## ¿Para qué usamos la IA?
Para convertir los datos crudos del análisis en un reporte entendible y con sugerencias útiles. No investiga nada por su cuenta, solo mejora y organiza lo que ya generaron los scripts.

## ¿En qué parte del flujo entra la IA?
Al final, después de:

1.⁠ ⁠Adquisición de datos (PowerShell)

2.⁠ ⁠Análisis y comparación (Python)

3.⁠ ⁠`IA para generar el reporte final`

El objetivo es: datos → filtrado → IA → reporte listo para entregar.

## ¿Qué API/modelo usaremos?
La API de OpenAI, usando un modelo de texto (en este caso se buscaría hacer uso de la version 3.5).  

## Prompt base que usaremos
Este es un ejemplo simple del prompt inicial que vamos a utilizar ⁠:
