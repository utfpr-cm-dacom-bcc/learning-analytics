import json
import os

def load_statements_from_file(filename="statements.json", folder="data"):
    filepath = os.path.join(folder, filename)
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"O arquivo {filepath} não foi encontrado.")
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)
