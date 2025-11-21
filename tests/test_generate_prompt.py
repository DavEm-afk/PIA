import os
import json

suspicious_file = os.path.join("analysis", "output", "suspicious_only.json")
prompt_file = os.path.join("prompts", "prompt_v2.json")

with open(suspicious_file, "r", encoding="utf-8") as f:
    data = f.read()
with open(prompt_file, "r", encoding="utf-8") as f:
    prompt_config = json.load(f)

template = prompt_config["template"].replace("{data}", data)
instrucciones = "\n".join(prompt_config["instrucciones"])
final_prompt = f"{template}\n{instrucciones}"


print("model=\"gpt-3.5-turbo\", messages=[ {\"role\": \"user\",  \"content\":", final_prompt, "} ]")
