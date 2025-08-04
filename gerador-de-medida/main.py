from metrica_pontuacao import calcular_pontuacao
from metrica_tempo import calcular_tempo_resposta
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

if __name__ == "__main__":
    main()
