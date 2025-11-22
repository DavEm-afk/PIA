import json
import os
import datetime
import logging
from src.analysis.process_network_analysis import perform_network_analysis
from src.analysis.hash_analysis import analyze_file_hashes
from src.analysis.filter_suspicious import filter_suspicious

# Definir BASE_DIR y carpetas
BASE_DIR = os.path.dirname(__file__)        
ACQ_DIR = os.path.join(BASE_DIR, "../acquisition/raw")
CONFIG_DIR = os.path.join(BASE_DIR, "config")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
LOG_DIR = os.path.join(BASE_DIR, "../../logs")

# Configuración de logs 
os.makedirs(LOG_DIR, exist_ok=True)
log_file = os.path.join(LOG_DIR, f"analysis_{datetime.datetime.now():%Y%m%d_%H%M%S}.jsonl")
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
config_paths = load_json(os.path.join(CONFIG_DIR, "paths.json"))
priorities = load_json(os.path.join(CONFIG_DIR, "priorities.json"))

# Variables a usar de priorities
suspicious_ports = priorities.get("suspicious_ports", [])
internal_ranges = priorities.get("internal_ip_ranges", [])

# Cargar datos de /acquisition/raw
processes = load_json(os.path.join(ACQ_DIR, "process_list.json")) or {}
files = load_json(os.path.join(ACQ_DIR, "files_list.json")) or {}
network = load_json(os.path.join(ACQ_DIR, "net_connections.json")) or {}

# Filtrar datos relevantes 
high_priority = [p.lower() for p in priorities.get("high_priority_processes", [])]
ignore_list = [p.lower() for p in priorities.get("ignore_processes", [])]

important_procs = []
for p in processes.get("Procesos", []):
    nombre = p.get("Nombre", "").lower()
    if nombre in high_priority and nombre not in ignore_list:
        important_procs.append(p)

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
    net_file=os.path.join(ACQ_DIR, "net_connections.json"),
    process_file=os.path.join(ACQ_DIR, "process_list.json"),
    config_dir=CONFIG_DIR
)
summary.update(network_result)

# Integracion de analisis de hashes
hash_result = analyze_file_hashes(
    files_list=files.get("Archivos", []),
    blacklist_path=os.path.join(CONFIG_DIR, "hash_blacklist.json")
)
summary.update({"AnalisisHashes": hash_result})

# Guardado
os.makedirs(OUTPUT_DIR, exist_ok=True)
output_path = os.path.join(OUTPUT_DIR, "filtered_summary.json")
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(summary, f, indent=4, ensure_ascii=False)

logging.info(json.dumps({
    "status": "OK",
    "message": f"Analisis completado correctamente. Resultado guardado en {output_path}"
}))

# Crear resumen compacto
filter_suspicious(
    summary_path=output_path,
    output_path=os.path.join(OUTPUT_DIR, "suspicious_only.json")
)

print(f"Análisis completado. Resultados en: {output_path}")
print(f"Log generado en: {log_file}")
