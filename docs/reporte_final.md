# Reporte final – Cambios importantes en la planeación

> Este documento forma parte del entregable final del proyecto PIA. Su propósito es dejar constancia de los ajustes significativos realizados durante el desarrollo del proyecto que afectaron el resultado final.

---

## Cambios en tareas técnicas

- **Tarea 1 — Adquisición de artefactos del sistema**  
  Se mantuvo el propósito original de recolectar procesos, conexiones y eventos del sistema mediante PowerShell.  

- **Tarea 2 — Verificación de integridad de archivos mediante hashing**  
  Inicialmente se planeaba comparar los hashes actuales contra una lista de referencia generada previamente.  
  Para evitar repetir lo visto en clase, se modificó el diseño: aunque algo mas simple, se optó por comparar los hashes de archivos sospechosos previamente filtrados, contra una base de hashes de malwares instalables conocidos.  
  La lista utilizada es limitada debido a su uso meramente academico.

- **Tarea 3 — Adquisición extendida de red**  
  Esta tarea fue un agregado respecto a la propuesta inicial.  
  Se implementó la **correlación entre procesos activos y sus conexiones de red** usando la librería `psutil`.   

---

## Cambios en el uso de IA

- El propósito inicial era generar un resumen básico se amplió a un informe más detallado, con hallazgos y recomendaciones.   
- Se implementó un manejo de errores en caso de que falte la API key.
- En caso de que no se obtengan anomalías, el reporte generado se enfocará en  dar recomendaciones para mantener la seguridad. 

---

## Cambios en roles o distribución del trabajo

- **David Emiliano Rangel Tovar**: responsable de la **adquisición y análisis**. Implementó los scripts de PowerShell y módulos en Python para recolectar artefactos y procesar la información. También realizó las pruebas de ejecución y documentó la evidencia.  
- **Marcelo Hernández Chávez**: responsable de la **integración de IA y generación de reportes**. Implementó los módulos de integración con OpenAI y diseñó los prompts.  

---

## Decisiones técnicas relevantes

- Adición de la tarea 3 y su implementación en el flujo de ejecución. 
- Agregado de la carpeta `/src/analysis/configuration`, para mayor claridad en cuanto a los métodos utilizados para identificar anomalías.   

---

## Impacto en el entregable final
  
- La implementación de la tarea 3 favoreció la adquisición de evidencia y enriqueció el análisis.  
- Se facilitó la comprensión del pipeline con ayuda de los archivos agregados en la carpeta `/src/analysis/config` , ademas de ayudar en la modularización del proyecto.

---

## Confirmación de cierre

> Confirmamos que la última actualización del repositorio fue realizada **antes del 26 de noviembre a las 10:00 hrs (hora local de Monterrey)**.

- Fecha del último commit: [2025-11-25 19:05]  
- Usuario responsable del cierre: [David Emiliano Rangel Tovar]
