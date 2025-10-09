import json
import os

def load_statements_from_file(filename="statements.json", folder="data"):
    filepath = os.path.join(folder, filename)
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"O arquivo {filepath} não foi encontrado.")

    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Se for um dicionário com chave "statements", pega apenas essa parte
    if isinstance(data, dict) and "statements" in data:
        return data["statements"]

    # Se for uma lista, retorna direto
    if isinstance(data, list):
        return data

    # Caso inesperado
    raise ValueError("Formato de arquivo JSON inválido. Esperado lista ou dicionário com 'statements'.")