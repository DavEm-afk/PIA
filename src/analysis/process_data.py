import json
import os
import datetime
import logging

# Configuración de logs 
os.makedirs("./logs", exist_ok=True)
log_file = f"./logs/analysis_{datetime.datetime.now():%Y%m%d_%H%M%S}.jsonl"
logging.basicConfig(filename=log_file, level=logging.INFO, format='%(message)s')

# Gestion de errores al cargar archivos
def load_json(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        logging.error(json.dumps({"error": f"Error al cargar {path}: {str(e)}"}))
        return {}

# Cargar configuraciones de /config
config_paths = load_json("./src/analysis/config/paths.json")
priorities = load_json("./src/analysis/config/priorities.json")

# Cargar datos de /acquisition
processes = load_json(config_paths.get("processes", "")) or {}
files = load_json(config_paths.get("files", "")) or {}
network = load_json(config_paths.get("connections", "")) or {}

# Filtrar datos relevantes 
# Procesos importantes por nombre o ruta
important_procs = []
if "Procesos" in processes:
    for p in processes["Procesos"]:
        if any(key.lower() in p["Nombre"].lower() for key in priorities.get("process_names", [])):
            important_procs.append(p)

# Archivos grandes o prioritarios
important_files = []
if "Archivos" in files:
    for f in files["Archivos"]:
        if f["TamañoKB"] > priorities.get("min_file_size_kb", 1024):  # por defecto >1 MB
            important_files.append(f)

# Unir información (si hay red)
for proc in important_procs:
    if network:
        related = [n for n in network.get("Conexiones", []) if n.get("pid") == proc.get("Id")]
        if related:
            proc["ConexionesActivas"] = related

# Generacion de salidas
summary = {
    "FechaAnalisis": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "TotalProcesos": len(processes.get("Procesos", [])),
    "TotalArchivos": len(files.get("Archivos", [])),
    "ProcesosRelevantes": important_procs,
    "ArchivosRelevantes": important_files,
}

# Guardado
os.makedirs("./src/analysis/output", exist_ok=True)
output_path = "./src/analysis/output/filtered_summary.json"
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(summary, f, indent=4, ensure_ascii=False)

logging.info(json.dumps({
    "status": "OK",
    "message": f"Análisis completado correctamente. Resultado guardado en {output_path}"
}))

print(f"Análisis completado. Resultados en: {output_path}")
print(f"Log generado en: {log_file}")
