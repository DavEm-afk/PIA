# Sistema de Análisis Forense Automatizado en Windows



## Objetivo del proyecto
Este proyecto implementa un flujo automatizado para la adquisición, análisis y documentación de elementos relevantes en Windows. Se combinan tres componentes principales:

Scripts de PowerShell: obtienen datos de procesos y archivos.

Módulos en Python: procesan, filtran y correlacionan la información.

Integración con OpenAI API: redacta un informe a partir de los hallazgos.

El flujo completo es: Adquisición → Análisis → Implementacion de IA → Evidencia documentada

---

### Requisitos previos
- Python 3.10+

- Librerías: pandas, openai, psutil

- PowerShell habilitado en Windows

- Variable de entorno OPENAI_API_KEY definida con tu clave de OpenAI

---

### Ejecución del pipeline
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

## Integrantes y roles

- **David Emiliano Rangel Tovar**  
  Responsable de la **adquisición y análisis**.  
  - Implementó los scripts de PowerShell y módulos en Python para la recolección de datos.  
  - Desarrolló el procesamiento y filtrado de la información en `/src/analysis`.  
  - Ejecutó pruebas de funcionamiento del pipeline y documentó evidencias en `/examples` y `/logs`.

- **Marcelo Hernández Chávez**  
  Responsable de la **integración de IA y generación de reportes**.  
  - Implementó los módulos de integración con OpenAI API en `/src/integration`.  
  - Diseñó los prompts en `/prompts` y desarrolló el flujo de generación de reportes en `/src/reporting`.  
  - Colaboró en la documentación del proyecto.

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

### Ejemplos de salida
`findings.csv`

- Siempre contiene el encabezado category,detail.

- Si no hay hallazgos, queda vacío salvo el encabezado (ejemplo: category,detail).

- Si hay hallazgos, se agregan filas como:

csv
category,detail, 
process,SuspiciousProcess.exe (PID 1234), 
file,C:\Temp\malware_sample.exe, 
network,Connection to 192.168.1.50:4444

`executive_summary.md`

- Con API key definida → contiene un resumen redactado por IA.

- Sin API key → muestra un error controlado:
 
[ERROR] No se encontró la API key. Configure OPENAI_API_KEY en el entorno.

---

## Estado actual del proyecto
Adquisición - Completado

Análisis - Completado

Reporte con IA - Implementado con manejo de errores

Pipeline - Funcional y reproducible

---

## Declaración ética

Este proyecto fue desarrollado exclusivamente con fines académicos.  
Todas las pruebas se realizaron en entornos con datos sintéticos o equipos autorizados por sus propietarios.  
En ningún momento se expusieron credenciales reales ni información personal; los datos recolectados se limitaron a procesos y rutas de archivos pertenecientes al sistema bajo análisis.  
El uso de credenciales, como la *API key* de la librería de OpenAI, se gestionó mediante variables de entorno.  

---

## Enlaces internos a entregables (docs)

- [Entregable 3](./docs/entregable_3.md)  
- [Entregable 4](./docs/entregable_4.md)  
- [Plan de IA](./docs/ai_plan.md)  
- [Reporte final](./docs/reporte_final.md)


