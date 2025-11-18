import json
import os
import datetime

def load_json(path):
    try:
        with open(path, "r", encoding="utf-8-sig") as f:
            return json.load(f)
    except Exception as e:
        print(f"[ERROR] No se pudo cargar {path}: {e}")
        return {}

def filter_suspicious(summary_path, output_path="./output/suspicious_only.json"):
    # Genera archivo con SOLO información sospechosa
    data = load_json(summary_path)
    if not data:
        print("ERROR. El summary está vacío o no se pudo leer.")
        return

    resultado = {
        "FechaAnalisis": data.get("FechaAnalisis", datetime.datetime.now().isoformat()),
        "ProcesosSospechosos": [],
        "ArchivosSospechosos": []
    }

    # Procesos sospechosos
    for proc in data.get("ProcesosRelevantes", []):
        
        conexiones = proc.get("ConexionesActivas", [])
        conexiones_sospechosas = []

        for c in conexiones:
            if c.get("Sospechosa") or c.get("Externa"):
                conexiones_sospechosas.append(c)

        if conexiones_sospechosas:
            copia = {
                "ID": proc.get("ID"),
                "Nombre": proc.get("Nombre"),
                "Ruta": proc.get("Ruta"),
                "ConexionesSospechosas": conexiones_sospechosas
            }
            resultado["ProcesosSospechosos"].append(copia)

    # Archivos sospechosos
    for f in data.get("ArchivosRelevantes", []):
        
        if f.get("CoincideBlacklist") or f.get("SospechosoPorExtension"):
            resultado["ArchivosSospechosos"].append({
                "Ruta": f.get("Ruta"),
                "HashSHA256": f.get("HashSHA256"),
                "CoincideBlacklist": f.get("CoincideBlacklist", False),
                "Motivo": "Hash malicioso" if f.get("CoincideBlacklist") else "Extensión/Directorio sospechoso"
            })

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(resultado, f, indent=4, ensure_ascii=False)

    print(f"Resumen compacto generado en: {output_path}")
