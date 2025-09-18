from projeto.fetch_statements import fetch_statements

import scripts 
from scripts import load_statements_from_file
from scripts import save_statements_to_file

# Buscar do RALPH
statements = fetch_statements({"limit": 10})

# Salvar no arquivo
save_statements_to_file(statements, filename="statements.json")

# Ler de volta do arquivo
statements_lidos = load_statements_from_file("statements.json")

print(f"Statements lidos: {len(statements_lidos)}")