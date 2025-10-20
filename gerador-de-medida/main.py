from src.fetch_statements import fetch_statements
from src.scripts.load_statements_from_file import load_statements_from_file

from src.metricas.metrica_pontuacao import calcular_pontuacao
from src.metricas.metrica_tempo import calcular_tempo_resposta
from src.metricas.metrica_tentativas_por_questionario import calcular_tentativas_por_questionario
from src.metricas.metrica_tempo_total_gasto_em_visitas_reais import calcular_tempo_total_gasto_em_visitas_reais
from src.metricas.metrica_porcentagem_do_curso_acessada import calcular_porcentagem_do_curso_acessada


def main():
    statements = fetch_statements({
        "verb": "http://adlnet.gov/expapi/verbs/completed",
        "limit": 1000
    })
    
    print("Calculando métrica de pontuação...")
    calcular_pontuacao(statements)

    statements = fetch_statements({
        "verb": "http://adlnet.gov/expapi/verbs/completed",
        "limit": 1000
    })

    print("Calculando métrica de tempo de resposta...")
    calcular_tempo_resposta(statements)

    statements = fetch_statements({
        "verb": "http://adlnet.gov/expapi/verbs/completed",
        "limit": 1000
    })
    
    print("Calculando métrica de tentativas por questionario...")
    calcular_tentativas_por_questionario(statements)

    statements = fetch_statements({
        "limit": 1000
    })

    print("Calculando métrica de tempo total gasto em visitas reais...")
    calcular_tempo_total_gasto_em_visitas_reais(statements)

    arquivo_json = "atividades.json"

    print("Calculando métrica de porcentagem do curso acessada...")
    calcular_porcentagem_do_curso_acessada(arquivo_json)

def main2():
    
    statements = load_statements_from_file("statements_1.json",folder='data/statements_adivinhacao')

    print("Calculando métrica de pontuação...")
    calcular_pontuacao(statements)
   
    print("Calculando métrica de tempo de resposta...")
    calcular_tempo_resposta(statements)

    print("Calculando métrica de tentativas por questionario...")
    calcular_tentativas_por_questionario(statements)

    print("Calculando métrica de tempo total gasto em visitas reais...")
    calcular_tempo_total_gasto_em_visitas_reais(statements)

    arquivo_json = "atividades.json"

    print("Calculando métrica de porcentagem do curso acessada...")
    calcular_porcentagem_do_curso_acessada('data/' + arquivo_json)

if __name__ == "__main__":
    main2()