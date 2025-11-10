import subprocess
import json
import os

# Rutas de los scripts (ajusta según tu estructura de carpetas)
process_script = r"./get_processes.ps1"
files_script = r"./get_files.ps1"

def run_powershell(script_path):
    try:
        result = subprocess.run(
            ["powershell", "-ExecutionPolicy", "Bypass", "-File", script_path],
            capture_output=True, text=True, check=True
        )
        print(f"Ejecución exitosa: {os.path.basename(script_path)}")
        print(result.stdout)  # Muestra lo que el script imprime (ruta del archivo JSON)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error al ejecutar {script_path}:")
        print(e.stderr)
        return None

# Ejecutar ambos scripts
print("=== Ejecución de scripts PowerShell ===")
run_powershell(process_script)
run_powershell(files_script)
