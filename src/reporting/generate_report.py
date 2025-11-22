from src.integration.ai_client import call_ai
import os
import json
import pandas as pd

# Definir BASE_DIR 
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

OUTPUT_ANALYSIS_DIR = os.path.join(BASE_DIR, "src", "analysis", "output")
PROMPTS_DIR = os.path.join(BASE_DIR, "prompts")
OUTPUTS_DIR = os.path.join(BASE_DIR, "src", "reporting", "outputs")

os.makedirs(OUTPUTS_DIR, exist_ok=True)

def generate_report():
    suspicious_file = os.path.join(OUTPUT_ANALYSIS_DIR, "suspicious_only.json")
    prompt_file = os.path.join(PROMPTS_DIR, "prompt_v2.json")


    # Generar resumen con IA
    report_text = call_ai(suspicious_file, prompt_file)
    output_md = os.path.join(OUTPUTS_DIR, "executive_summary.md")
    with open(output_md, "w", encoding="utf-8") as f:
        f.write(report_text)
    print(f"Resumen ejecutivo generado en: {output_md}")


    # Exportar findings.csv con pandas
    with open(suspicious_file, "r", encoding="utf-8") as f:
        suspicious = json.load(f)

    rows = []
    for category, items in suspicious.items():
        for item in items:
            rows.append({"category": category, "detail": item})

    df = pd.DataFrame(rows, columns=["category", "detail"])
    output_csv = os.path.join(OUTPUTS_DIR, "findings.csv")
    df.to_csv(output_csv, index=False, encoding="utf-8")
    print(f"Findings exportados en: {output_csv}")


if __name__ == "__main__":
    generate_report()
