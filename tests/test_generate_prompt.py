import os
import json

# Rutas base
BASE_DIR = os.path.dirname(__file__)

suspicious_file = os.path.join(BASE_DIR, "../src/analysis/output/suspicious_only.json")
prompt_file = os.path.join(BASE_DIR, "../prompts/prompt_v2.json")


with open(suspicious_file, "r", encoding="utf-8") as f:
    data = f.read()
with open(prompt_file, "r", encoding="utf-8") as f:
    prompt_config = json.load(f)

# Construir prompt
template = prompt_config["template"].replace("{data}", data)
instrucciones = "\n".join(prompt_config["instrucciones"])
final_prompt = f"{template}\n{instrucciones}"

print(f'model="gpt-3.5-turbo", messages=[{{"role": "user", "content": "{final_prompt}"}}]')
