# Sistema de Análisis Forense Automatizado para Windows

### Descripción general del proyecto
Este proyecto es una solución sencilla para la recolección, análisis y documentación de evidencias en equipos con sistema operativo Windows. En el proyecto se integran scripts de PowerShell para la adquisición de artefactos propios del sistema y módulos en Python para el procesamiento, comparación y análisis de los datos obtenidos. Finalmente, se hace uso de OpenAI API para enriquecer y redactar un informe detallado usando como base los hallazgos recaudados con Python.  
Flujo del proyecto: *Adquisición → Análisis/Comparación → Uso de IA → Reporte*

---

## Estado del proyecto

•⁠  ⁠*Tarea 1 — Adquisición de procesos y archivos* - Completado 
  Scripts en ⁠ /src/acquisition/ ⁠ generan salidas en JSON dentro de ⁠ /src/acquisition/raw/ ⁠.

•⁠  ⁠*Tarea 2 — Hashing y comparación de archivos* - Completado  
  Se ejecuta en ⁠ /src/analysis/process_data.py ⁠, (orquesta las funciones de hashing y filtrado).  
  Genera resultados en ⁠ /src/analysis/output/ ⁠ y correlaciona en base a listas de referencia.

•⁠  ⁠*Tarea 3 — Conexiones de red* - Completado  
  Implementada en ⁠ /src/acquisition/get_network_info.py ⁠ y utilizada también desde ⁠ process_data.py ⁠.  
  Genera salidas en ⁠ /src/acquisition/raw/net_connections.json ⁠ y ⁠ /src/acquisition/raw/process_network.json ⁠.

•⁠  ⁠*Pipeline de orquestación (⁠ /scripts/run_pipeline.ps1 ⁠)* - Completado  
  Integra adquisición, análisis y reporte.  
  Generacion de logs en ⁠ /logs/run_<timestamp>.log ⁠.

•⁠  ⁠*Etapa de IA / Reporte final* - Pendiente  
  El pipeline intenta invocar ⁠ src/reporting/generate_report.py ⁠; al no existir aún, se registra un error en el log como evidencia del manejo de fallos.

---

## Estructura del repositorio
•⁠  ⁠⁠ /src ⁠ → Código fuente principal  
  - ⁠ /acquisition ⁠ → Scripts de adquisición (⁠ get_files.ps1 ⁠, ⁠ get_processes.ps1 ⁠, ⁠ get_network_info.py ⁠, ⁠ run_acquisition.py ⁠)  
  - ⁠ /acquisition/raw ⁠ → Salidas en crudo (JSON)  
  - ⁠ /analysis ⁠ → Scripts de análisis  
    - ⁠ process_data.py ⁠ → Script principal que orquesta el análisis y llama a los demás módulos  
    - ⁠ filter_suspicious.py ⁠, ⁠ hash_analysis.py ⁠, ⁠ process_network_analysis.py ⁠ → Funciones auxiliares  
    - ⁠ /output ⁠ → Resultados filtrados y sospechosos  
    - ⁠ /config ⁠ → Parámetros de configuración (hashes, paths, prioridades)  
  - ⁠ /integration ⁠ → Módulos de integración (pendiente)  
  - ⁠ /reporting ⁠ → Módulos de reporte con IA (pendiente)  
  - ⁠ /utils ⁠ → Utilidades (pendiente)  
•⁠  ⁠⁠ /scripts ⁠ → Pipeline de orquestación  
•⁠  ⁠⁠ /logs ⁠ → Registros de ejecución  
•⁠  ⁠⁠ /examples ⁠ → Ejemplos de salidas y logs  
•⁠  ⁠⁠ /docs ⁠ → Documentación (plan de IA, entregables, controles éticos)  
•⁠  ⁠⁠ /prompts ⁠ → Prompts iniciales para IA  
•⁠  ⁠⁠ /tests ⁠ → Scripts de prueba

---

