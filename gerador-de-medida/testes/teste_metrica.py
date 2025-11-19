from src.scripts.load_statements_from_file import load_statements_from_file
from src.adivinhacao import adivinhar
from src.metricas.metrica_proporcao_reviews_lidos import calcular_feedback_lido_por_usuario
from src.metricas.metrica_nivel_desordem import calcular_nivel_desordem

statements_lidos = load_statements_from_file("statements.json")

adivinhar(statements_lidos)

arquivo_json = "atividades.json"
calcular_nivel_desordem('data/' + arquivo_json)