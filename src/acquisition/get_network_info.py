import psutil
import json
import os
from datetime import datetime

# Configuración de rutas
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RAW_DIR = os.path.join(BASE_DIR, "raw")
LOG_DIR = os.path.join(BASE_DIR, "../../logs")

# Crear directorios si no existen
os.makedirs(RAW_DIR, exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)

# Archivos de salida 
net_file = os.path.join(RAW_DIR, "net_connections.json")
process_file = os.path.join(RAW_DIR, "process_network.json")
log_file = os.path.join(LOG_DIR, "acquisition_net.jsonl")

# Escritura de log 
def write_log(event_type, message, level="INFO"):
    entry = {
        "timestamp": datetime.now().isoformat(timespec='seconds'),
        "level": level,
        "event": event_type,
        "message": message
    }
    with open(log_file, "a", encoding="utf-8") as log:
        log.write(json.dumps(entry) + "\n")

write_log("start", "Inicio de adquisición de conexiones de red")

try:
    #  Recolectar conexiones globales del sistema 
    system_connections = []
    for conn in psutil.connections(kind='inet'):
        system_connections.append({
            "fd": conn.fd,
            "family": str(conn.family),
            "type": str(conn.type),
            "laddr": f"{conn.laddr.ip}:{conn.laddr.port}" if conn.laddr else None,
            "raddr": f"{conn.raddr.ip}:{conn.raddr.port}" if conn.raddr else None,
            "status": conn.status,
            "pid": conn.pid
        })
    
    with open(net_file, "w", encoding="utf-8") as f:
        json.dump(system_connections, f, indent=4)
    write_log("save", f"Conexiones globales guardadas en {net_file}")

    #  Recolectar conexiones asociadas a procesos 
    process_data = []
    for proc in psutil.process_iter(['pid', 'name', 'username']):
        try:
            conns = proc.net_connections(kind='inet')
            if conns:
                conn_list = []
                for c in conns:
                    conn_list.append({
                        "laddr": f"{c.laddr.ip}:{c.laddr.port}" if c.laddr else None,
                        "raddr": f"{c.raddr.ip}:{c.raddr.port}" if c.raddr else None,
                        "status": c.status
                    })
                process_data.append({
                    "pid": proc.info['pid'],
                    "name": proc.info['name'],
                    "user": proc.info.get('username'),
                    "connections": conn_list
                })
        except (psutil.AccessDenied, psutil.NoSuchProcess):
            continue

    with open(process_file, "w", encoding="utf-8") as f:
        json.dump(process_data, f, indent=4)
    write_log("save", f"Procesos con conexiones guardados en {process_file}")

    write_log("end", "Adquisición de red completada correctamente")

except Exception as e:
    write_log("error", f"Error durante la adquisición de red: {str(e)}", level="ERROR")
    print(f"Error: {e}")

