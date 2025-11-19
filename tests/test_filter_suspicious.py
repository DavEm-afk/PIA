import json
import os
from src.analysis.filter_suspicious import filter_suspicious

def test_filter_suspicious(tmp_path):

    # Crear archivo de entrada falso
    fake_input = tmp_path / "input.json"
    fake_output = tmp_path / "output.json"

    data = {
        "ProcesosRelevantes": [
            {
                "PID": 100,
                "Nombre": "malware.exe",
                "Sospechoso": True,
                "ConexionesActivas": []
            }
        ],
        "AnalisisHashes": [
            {
                "path": "C:/test.exe",
                "sha256": "abc123",
                "blacklist_match": True
            }
        ]
    }

    fake_input.write_text(json.dumps(data, indent=4), encoding="utf-8")

    # Ejecutar función real
    filter_suspicious(str(fake_input), str(fake_output))

    # Leer resultado
    out = json.loads(fake_output.read_text(encoding="utf-8"))

    assert len(out["ProcesosSospechosos"]) == 1
    assert len(out["ArchivosMaliciosos"]) == 1
