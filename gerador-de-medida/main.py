from metrica_pontuacao import calcular_pontuacao
from metrica_tempo import calcular_tempo_resposta
from metrica_tentativas_por_questionario import calcular_tentativas_por_questionario
from metrica_tempo_total_gasto_em_visitas_reais import calcular_tempo_total_gasto_em_visitas_reais
from fetch_statements import fetch_statements

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

if __name__ == "__main__":
    main()