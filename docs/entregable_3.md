# Entregable 3 — Avance del Proyecto

## Estado actual
El proyecto avanzó en comparación al entregable 2. Todas las tareas técnicas se encuentran terminadas:

- **Tarea 1 — Adquisición de procesos y archivos**  
  Scripts en `/src/acquisition/` generan salidas en JSON dentro de `/src/acquisition/raw/`.

- **Tarea 2 — Hashing y comparación de archivos**  
  Implementada en `/src/analysis/process_data.py`.  
  Genera resultados en `/src/analysis/output/` y correlaciona contra listas de referencia.

- **Tarea 3 — Conexiones de red**  
  Implementada en `/src/acquisition/get_network_info.py`.  
  Genera salidas en `/src/acquisition/raw/net_connections.json` y `/src/acquisition/raw/process_network.json`.

Además, se desarrolló el **pipeline de orquestación (`/scripts/run_pipeline.ps1`)**, que integra todas las etapas del proyecto (adquisición, análisis y reporte).  
El pipeline genera logs estructurados en `/logs/` y captura tanto ejecuciones correctas como errores.
(Se modificó el tipo de salida de archivo del log generado por el pipeline de .log a .jsonl).

## Pendiente
La etapa de generación de reportes con IA aún está por terminar.  
En la evidencia de ejecución, el pipeline intenta invocar `src/reporting/generate_report.py`, pero al no existir, se registra un error en el log.  
Se decidió dejar esto de manera intencional, funcionando asi como evidencia para demostrar la generación de logs implementada en `run_pipeline.ps1`.

## Evidencias
- Ejemplo de log en `/examples/logs.jsonl` mostrando ejecución correcta y error controlado.  
- Captura de pantalla del flujo enviada por MS Teams.  
- Actualización del `README.md` reflejando la estructura y estado actual del proyecto.

## Próximos pasos
- Implementar el módulo de IA para generación de reportes.  
- Mejorar logs y agregar las validaciones necesarias.  
