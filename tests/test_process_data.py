from src.analysis.process_data import summarize_process_info

def test_summarize_process_info():

    fake_processes = [
        {
            "PID": 10,
            "Nombre": "chrome.exe",
            "User": "user",
            "ConexionesActivas": []
        }
    ]

    summary = summarize_process_info(fake_processes)

    assert len(summary) == 1
    assert summary[0]["PID"] == 10
    assert summary[0]["Nombre"] == "chrome.exe"
