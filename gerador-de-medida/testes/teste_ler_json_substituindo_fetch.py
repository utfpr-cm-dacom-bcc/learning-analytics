from src.scripts.load_statements_from_file import load_statements_from_file
from src.metricas.metrica_pontuacao import calcular_pontuacao

statements_lidos = load_statements_from_file("statements.json")

print(f"Statements lidos: {len(statements_lidos)}")

resultado = calcular_pontuacao(statements_lidos)

print(f"Resultado da pontuação: {resultado}")