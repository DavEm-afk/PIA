import json
import os
import logging
import datetime

def load_json_utf8_sig(path):
    try:
        with open(path, "r", encoding="utf-8-sig") as f:
            return json.load(f)
    except Exception as e:
        logging.error(json.dumps({
            "module": "hash_analysis",
            "error": f"Error al cargar {path}: {str(e)}"
        }))
        return {}

def analyze_file_hashes(files_list, blacklist_path):
    # Carga de blacklist
    blacklist = load_json_utf8_sig(blacklist_path).get("hash_blacklist", [])
    blacklist = [h.lower() for h in blacklist]

    matches = []
    total_files = len(files_list)

    for file in files_list:
        file_hash = file.get("HashSHA256", "").lower()

        if file_hash and file_hash in blacklist:
            matches.append({
                "Ruta": file.get("Ruta"),
                "HashSHA256": file_hash,
                "CoincidenciaBlacklist": True
            })

    return {
        "TotalArchivosAnalizados": total_files,
        "TotalCoincidencias": len(matches),
        "Coincidencias": matches,
        "FechaAnalisisHash": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

