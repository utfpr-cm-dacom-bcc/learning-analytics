from collections import defaultdict
import json
from fetch_statements import fetch_statements

def calcular_pontuacao(statements):
    usuarios = defaultdict(lambda: defaultdict(dict))

    for statement in statements:
        actor = statement.get("actor", {}).get("account", {}).get("name")
        result = statement.get("result", {})
        score = result.get("score", {})
        raw = score.get("raw")
        max_score = score.get("max")

        parents = statement.get("context", {}).get("contextActivities", {}).get("parent", [])

        materia = None
        quiz_id = None

        for parent in parents:
            id_parent = parent.get("id", "")
            definition = parent.get("definition", {})
            tipo = definition.get("type", "")

            if "activitytype/course" in tipo:
                materia = definition.get("name", {}).get("en")
            elif "mod/quiz/view.php" in id_parent:
                quiz_id = id_parent

        if actor and raw is not None and max_score and materia and quiz_id:
            atual = usuarios[actor][materia].get(quiz_id, {"acertos": 0, "total_questoes": max_score})
            if raw > atual["acertos"]:
                usuarios[actor][materia][quiz_id] = {
                    "acertos": raw,
                    "total_questoes": max_score
                }

    resultados = []
    for usuario, materias in usuarios.items():
        for materia, quizzes in materias.items():
            total_acertos = sum(q["acertos"] for q in quizzes.values())
            total_questoes = sum(q["total_questoes"] for q in quizzes.values())

            pontuacao = (10 / total_questoes) * total_acertos if total_questoes else 0

            resultados.append({
                "usuario": usuario,
                "materia": materia,
                "acertos": total_acertos,
                "total_questoes": total_questoes,
                "pontuacao": round(pontuacao, 2)
            })

    with open("resultado_pontuacao.json", "w", encoding="utf-8") as f:
        json.dump(resultados, f, indent=2, ensure_ascii=False)

    return resultados

if __name__ == "__main__":
    statements = fetch_statements({
        "verb": "http://adlnet.gov/expapi/verbs/completed",
        "limit": 1000
    })
    calcular_pontuacao(statements)
