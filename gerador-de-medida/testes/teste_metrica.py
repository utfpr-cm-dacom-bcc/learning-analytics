from src.scripts.load_statements_from_file import load_statements_from_file
from src.adivinhacao import adivinhar
from src.metricas.metrica_nivel_compreensao import calcular_nivel_compreensao
from src.metricas.metrica_nivel_confusao import calcular_nivel_confusao
from src.metricas.metrica_nivel_desordem import calcular_nivel_desordem
from src.metricas.metrica_pontuacao import calcular_pontuacao
from src.metricas.metrica_porcentagem_do_curso_acessada import calcular_porcentagem_do_curso_acessada
from src.metricas.metrica_proporcao_reviews_lidos import calcular_feedback_lido_por_usuario
from src.metricas.metrica_proporcao_visualizacoes_por_atividade import calcular_proporcao_visualizacoes_por_atividade
from src.metricas.metrica_tempo_total_gasto_em_visitas_reais import calcular_tempo_total_gasto_em_visitas_reais
from src.metricas.metrica_tempo import calcular_tempo_resposta
from src.metricas.metrica_tentativas_por_questionario import calcular_tentativas_por_questionario
from src.metricas.metrica_visualizacoes_por_objeto import calcular_visualizacoes_por_objeto

statements_lidos = load_statements_from_file("statements.json")

adivinhar(statements_lidos)

arquivo_json = "atividades.json"

# Métrica de Nível de Compreensão
#calcular_nivel_compreensao('data/' + arquivo_json)

# Métrica de Nível de Confusão
#calcular_nivel_confusao('data/' + arquivo_json)

# Métrica de Nível de Desordem
#calcular_nivel_desordem('data/' + arquivo_json)

# Métrica de Pontuação
#calcular_pontuacao(statements_lidos)

# Métrica de Porcentagem do Curso Acessada
#calcular_porcentagem_do_curso_acessada('data/' + arquivo_json)

# Métrica de Proporção de Reviews Lidos
#calcular_feedback_lido_por_usuario('data/' + arquivo_json)

# Métrica de Tempo Total Gasto em Visitas Reais
#calcular_tempo_total_gasto_em_visitas_reais(statements_lidos)

# Métrica de Tempo de Resposta
#calcular_tempo_resposta(statements_lidos)

# Métrica de Tentativas por Questionario
#calcular_tentativas_por_questionario(statements_lidos)

# Métrica de Visualizacoes por Objeto
#calcular_visualizacoes_por_objeto('data/' + arquivo_json)