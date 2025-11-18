import json
import os

def load_json(path):
    try:
        with open(path, "r", encoding="utf-8-sig") as f:
            return json.load(f)
    except Exception as e:
        print(f"ERROR. No se pudo cargar {path}: {e}")
        return {}

def filter_suspicious(summary_path: str, output_path: str):

    data = load_json(summary_path)

    suspicious_out = {
        "ProcesosSospechosos": [],
        "ConexionesSospechosas": [],
        "ArchivosMaliciosos": []
    }

    # Procesos sospechosos
    for proc in data.get("ProcesosRelevantes", []):
        conexiones = proc.get("ConexionesActivas", [])

        conexiones_sos = [
            c for c in conexiones
            if c.get("Sospechosa") or c.get("Externa")
        ]

        if conexiones_sos:
            proc_copy = proc.copy()
            proc_copy["ConexionesActivas"] = conexiones_sos
            suspicious_out["ProcesosSospechosos"].append(proc_copy)

    # Conexiones de procesos
    for proc in data.get("ProcesosRelevantes", []):
        for conn in proc.get("ConexionesActivas", []):
            if conn.get("Sospechosa") or conn.get("Externa"):
                suspicious_out["ConexionesSospechosas"].append(conn)

    # Hashes sospechosos
    hash_res = data.get("AnalisisHashes", {})

    for entry in hash_res.get("coincidencias", []):
        if entry.get("malicioso") is True:
            suspicious_out["ArchivosMaliciosos"].append(entry)

    # Guardado
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(suspicious_out, f, indent=4, ensure_ascii=False)

    print(f"Resumen de informacion sospechosa generado en: {output_path}")
