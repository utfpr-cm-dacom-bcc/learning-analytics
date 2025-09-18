import json
import os

def save_statements_to_file(statements, filename="statements.json", folder="data"):
    os.makedirs(folder, exist_ok=True)  # cria a pasta se não existir
    filepath = os.path.join(folder, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(statements, f, ensure_ascii=False, indent=4)
    print(f"Arquivo salvo em: {filepath}")

