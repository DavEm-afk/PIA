import os
import openai
import json

def call_ai(suspicious_file: str, prompt_file: str) -> str:

    # Cargar datos sospechosos
    with open(suspicious_file, "r", encoding="utf-8") as f:
        data = f.read()

    # Cargar configuración del archivo prompt
    with open(prompt_file, "r", encoding="utf-8") as f:
        prompt_config = json.load(f)

    # Construir el prompt final
    template = prompt_config["template"].replace("{data}", data)
    instrucciones = "\n".join(prompt_config["instrucciones"])
    final_prompt = f"{template}\n{instrucciones}"

    # Uso de variable de entorno para API key
    api_key = os.getenv("OPENAI_API_KEY")
    client = openai.OpenAI(api_key=api_key)

    # Llamar al modelo 
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", 
             "content": final_prompt}
        ]
    )

    # Texto generado por la IA
    return response.choices[0].message.content
