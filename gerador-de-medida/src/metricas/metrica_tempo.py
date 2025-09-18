import json
from ..fetch_statements import fetch_statements
from datetime import datetime

def calcular_tempo_resposta(statements):
    tempos = []

    for statement in statements:
        actor = statement.get("actor", {}).get("account", {}).get("name")
        timestamp = statement.get("timestamp")
        duration = statement.get("result", {}).get("duration")

        # Extraindo a "matéria"
        materia = (
            statement.get("context", {})
            .get("contextActivities", {})
            .get("parent", [{}])[0]
            .get("definition", {})
            .get("name", {})
            .get("en")
        )

        # Extraindo a "atividade"
        atividade = (
            statement.get("object", {})
            .get("definition", {})
            .get("name", {})
            .get("en")
        )

        if actor and timestamp and duration:
            tempos.append({
                "usuario": actor,
                "tempo_resposta": duration,
                "timestamp": timestamp,
                "materia": materia or "Desconhecida",
                "atividade": atividade or "Desconhecida"
            })

    with open("resultado_tempo_resposta.json", "w", encoding="utf-8") as f:
        json.dump(tempos, f, indent=2, ensure_ascii=False)

    return tempos

if __name__ == "__main__":
    statements = fetch_statements({
        "verb": "http://adlnet.gov/expapi/verbs/completed",
        "limit": 1000
    })
    calcular_tempo_resposta(statements)
