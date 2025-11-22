# Estado actual
Las tareas pendientes fueron completadas, ademas de que se arreglaron problemas con las rutas dentro de los codigos y el pipeline ahora funciona completamente:

- Tarea 1 — Adquisición de procesos y archivos Scripts en `/src/acquisition/` generan salidas en JSON dentro de `/src/acquisition/raw/` . La etapa se mantiene estable.

- Tarea 2 — Hashing y comparación de archivos implementada en `/src/analysis/process_data.py` . Genera resultados en `/src/analysis/output/` y correlaciona contra listas de referencia. Se confirmó la integración con la etapa de reporte.

- Tarea 3 — Conexiones de red Implementada en `/src/acquisition/get_network_info.py`. Genera salidas en `/src/acquisition/raw/net_connections.json` y `/src/acquisition/raw/process_network.json` .

## Pipeline de orquestación (/scripts/run_pipeline.ps1) 
Integra adquisición, análisis y reporte. Genera logs estructurados en /logs/. Captura tanto ejecuciones correctas como errores controlados.

## Etapa de IA / Reporte final 
Implementada en /src/reporting/generate_report.py. El módulo genera:

- `executive_summary.md` → resumen redactado con IA (o muestra un error mencionando la falta de API key).

- `findings.csv` → tabla estructurada con hallazgos; si no hay hallazgos, se genera únicamente el encabezado category,detail.

## Por hacer
Ahora solamente nos quedará por revisar el funcionamiento, ademas de implementar algunas medidas como validaciones o agregado de logs donde consideremos necesario.
