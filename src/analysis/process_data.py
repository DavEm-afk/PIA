import json
import os
import datetime
import logging
from process_network_analysis import perform_network_analysis

# Configuración de logs 
os.makedirs("./logs", exist_ok=True)
log_file = f"./logs/analysis_{datetime.datetime.now():%Y%m%d_%H%M%S}.jsonl"
logging.basicConfig(filename=log_file, level=logging.INFO, format='%(message)s')

# Gestion de errores al cargar archivos
def load_json(path):
    try:
        with open(path, "r", encoding="utf-8-sig") as f:
            return json.load(f)
    except Exception as e:
        logging.error(json.dumps({"error": f"Error al cargar {path}: {str(e)}"}))
        return {}

# Cargar configuraciones de /config
config_paths = load_json("./src/analysis/config/paths.json")
priorities = load_json("./src/analysis/config/priorities.json")

# Variables a usar de priorities
suspicious_ports = priorities.get("suspicious_ports", [])
internal_ranges = priorities.get("internal_ip_ranges", [])

# Cargar datos de /acquisition
processes = load_json(config_paths.get("processes", "")) or {}
files = load_json(config_paths.get("files", "")) or {}
network = load_json(config_paths.get("connections", "")) or {}

# Filtrar datos relevantes 
# Procesos importantes por nombre o ruta
high_priority = [p.lower() for p in priorities.get("high_priority_processes", [])]
ignore_list = [p.lower() for p in priorities.get("ignore_processes", [])]

important_procs = []
for p in processes.get("Procesos", []):
    nombre = p.get("Nombre", "").lower()
    if nombre in high_priority and nombre not in ignore_list:
        important_procs.append(p)

# Archivos grandes o prioritarios
suspicious_ext = [e.lower() for e in priorities.get("suspicious_extensions", [])]
sensitive_paths = [p.lower() for p in priorities.get("sensitive_paths", [])]

important_files = []
for f in files.get("Archivos", []):
    ruta = f.get("Ruta", "").lower()
    ext = os.path.splitext(ruta)[1]
    if ext in suspicious_ext or any(sp in ruta for sp in sensitive_paths):
        important_files.append(f)

# Unir información (si hay red)
for proc in important_procs:
    related = [n for n in network if n.get("pid") == proc.get("ID")]
    for conn in related:
        raddr = conn.get("raddr")
        port = int(raddr.split(":")[1]) if raddr else None
        conn["Sospechosa"] = (port in suspicious_ports) if port else False
        # Identificar si la IP remota está fuera de rangos internos
        if raddr:
            conn_ip = raddr.split(":")[0]
            conn["Externa"] = not any(conn_ip.startswith(ir) for ir in internal_ranges)
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

# Integracion de analisis de red
network_result = perform_network_analysis(
    net_file=config_paths.get("connections", ""),
    process_file=config_paths.get("processes", ""),
    config_dir="./src/analysis/config"
)
summary.update(network_result)

# Guardado
os.makedirs("./output", exist_ok=True)
output_path = "./output/filtered_summary.json"
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(summary, f, indent=4, ensure_ascii=False)

logging.info(json.dumps({
    "status": "OK",
    "message": f"Análisis completado correctamente. Resultado guardado en {output_path}"
}))

print(f"Análisis completado. Resultados en: {output_path}")
print(f"Log generado en: {log_file}")
