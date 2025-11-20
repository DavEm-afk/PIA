import subprocess
import json
import os
from datetime import datetime

# Carpeta base: /src/acquisition
BASE_DIR = os.path.dirname(__file__)

# Rutas de los scripts PowerShell
process_script = os.path.join(BASE_DIR, "get_processes.ps1")
files_script = os.path.join(BASE_DIR, "get_files.ps1")

# Carpeta de logs (en la raíz del proyecto)
LOG_DIR = os.path.abspath(os.path.join(BASE_DIR, "../../logs"))
os.makedirs(LOG_DIR, exist_ok=True)

# Nombre del archivo de log con timestamp
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
log_file_path = os.path.join(LOG_DIR, f"acquisition_{timestamp}.jsonl")

def run_powershell(script_path):
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "script": os.path.basename(script_path),
        "status": "",
        "output_file": ""
    }

    try:
        result = subprocess.run(
            ["powershell", "-ExecutionPolicy", "Bypass", "-File", script_path],
            capture_output=True, text=True, check=True
        )
        print(f"Ejecución exitosa: {os.path.basename(script_path)}")
        print(result.stdout)

        log_entry["status"] = "success"
        # Extraer ruta del archivo JSON generado desde la salida del PS
        for line in result.stdout.splitlines():
            if "Archivo generado:" in line:
                log_entry["output_file"] = line.split("Archivo generado:")[-1].strip()
        return log_entry

    except subprocess.CalledProcessError as e:
        print(f"Error al ejecutar {script_path}:")
        print(e.stderr)
        log_entry["status"] = "error"
        return log_entry

# Ejecutar scripts y guardar logs
print("=== Ejecución de scripts PowerShell ===")
log_entries = []
for script in [process_script, files_script]:
    entry = run_powershell(script)
    log_entries.append(entry)

# Guardar log en formato JSON Lines
with open(log_file_path, "w", encoding="utf-8") as f:
    for entry in log_entries:
        f.write(json.dumps(entry) + "\n")

print(f"\nLog generado: {log_file_path}")
