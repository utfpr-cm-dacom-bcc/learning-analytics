from src.scripts.load_statements_from_file import load_statements_from_file
from src.metricas.metrica_pontuacao import calcular_pontuacao
from src.adivinhacao import processar_statements, adivinhar

statements_lidos = load_statements_from_file("statements_feedback.json")

#print(f"Statements lidos: {len(statements_lidos)}")

#processar_statements(statements_lidos)
adivinhar(statements_lidos)

#print("Statements lidos e processados")

resultado = calcular_pontuacao(statements_lidos)

#print(f"Resultado da pontuação: {resultado}")

statements_lidos = load_statements_from_file("statements_1.json",folder='data/statements_adivinhacao')

#print(f"Statements lidos: {len(statements_lidos)}")
