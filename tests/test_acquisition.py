import os, json

def test_files_exist():
    assert os.path.exists("./src/acquisition/raw/process_list.json")
    assert os.path.exists("./src/acquisition/raw/files_list.json")

def test_json_format():
    for f in ["process_list.json", "files_list.json"]:
        with open(f"./src/acquisition/raw/{f}", "r", encoding="utf-8") as file:
            data = json.load(file)
            assert "FechaEjecucion" in data
            assert "Archivos" in data or "Procesos" in data
