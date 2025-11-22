# Sistema de Análisis Forense Automatizado en Windows

---

## Objetivo del proyecto
Este proyecto implementa un flujo automatizado para la adquisición, análisis y documentación de elementos relevantes en Windows. Se combinan tres componentes principales:

Scripts de PowerShell: obtienen datos de procesos y archivos.

Módulos en Python: procesan, filtran y correlacionan la información.

Integración con OpenAI API: redacta un informe a partir de los hallazgos.

El flujo completo es: Adquisición → Análisis → Implementacion de IA → Evidencia documentada

---

## Requisitos previos
- Python 3.10+

- Librerías: pandas, openai, piexif, PIL

- PowerShell habilitado en Windows

- Variable de entorno OPENAI_API_KEY definida con tu clave de OpenAI

---

## Ejecución del pipeline
Clonar el repositorio.

Es importante asegurarse de que se incluyen las carpetas principales:

- /src → contiene el código fuente del pipeline.
- /scripts → incluye el script de orquestación (run_pipeline.ps1) que ejecuta todo el flujo.
- /prompts → almacena las plantillas necesarias para la etapa de IA 

Instalar dependencias: 

`pip install -r requirements.txt`

Ejecución:

`cd scripts
pwsh run_pipeline.ps1`

---

## Estructura del repositorio
/scripts → Script principal de orquestación (run_pipeline.ps1)

/prompts → Plantillas para IA (prompt_v2.json)

/examples → Evidencias de ejecución (salidas)

/logs → Complemento de evidencias 

/docs → Documentación del proyecto y entregables

/tests → Scripts de prueba

/src → Código fuente

  - acquisition/ → Scripts de adquisición

  - analysis/ → Procesamiento y filtrado

  - integration/ → Cliente IA (ai_client.py)

  - reporting/ → Generación de reportes (generate_report.py)

---

## Ejemplos de salida
- findings.csv

Siempre contiene el encabezado category,detail.

Si no hay hallazgos, queda vacío salvo el encabezado (ejemplo: category,detail).

Si hay hallazgos, se agregan filas como:

csv
category,detail
process,SuspiciousProcess.exe (PID 1234)
file,C:\Temp\malware_sample.exe
network,Connection to 192.168.1.50:4444

- executive_summary.md

Con API key definida → contiene un resumen redactado por IA.

Sin API key → muestra un error controlado:

Código
[ERROR] No se encontró la API key. Configure OPENAI_API_KEY en el entorno.

---

## Estado actual del proyecto
Adquisición - Completado

Análisis - Completado

Reporte con IA - Implementado con manejo de errores

Pipeline - Funcional y reproducible

📷 Evidencia
Ejemplos de salidas y logs en /examples
