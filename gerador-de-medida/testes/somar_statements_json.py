from src.scripts.load_statements_from_file import load_statements_from_file
from src.scripts.save_statements_to_file import save_statements_to_file

all_statements = []

statements_lidos = load_statements_from_file("statements_1.json",folder='data/statements_adivinhacao')
all_statements.extend(statements_lidos)
statements_lidos = load_statements_from_file("statements_2.json",folder='data/statements_adivinhacao')
all_statements.extend(statements_lidos)
statements_lidos = load_statements_from_file("statements_3.json",folder='data/statements_adivinhacao')
all_statements.extend(statements_lidos)
statements_lidos = load_statements_from_file("statement_gerais.json",folder='data/statements_adivinhacao')
all_statements.extend(statements_lidos)
statements_lidos = load_statements_from_file("statement_gerais.json")
all_statements.extend(statements_lidos)
statements_lidos = load_statements_from_file("statements_feedback_leitura.json")
all_statements.extend(statements_lidos)
statements_lidos = load_statements_from_file("statements_feedback.json")
all_statements.extend(statements_lidos)
statements_lidos = load_statements_from_file("statements.json")
all_statements.extend(statements_lidos)

save_statements_to_file(all_statements)

