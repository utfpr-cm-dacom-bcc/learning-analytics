from collections import defaultdict
import json
from ..fetch_statements import fetch_statements

def calcular_pontuacao(statements):
    usuarios = defaultdict(lambda: defaultdict(dict))
    
    falhas = {
        "sem_actor": 0,
        "sem_raw": 0,
        "sem_max": 0,
        "sem_materia": 0,
        "sem_quiz_id": 0
    }

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
            if "mod/quiz/view.php" in id_parent:
                quiz_id = id_parent

        # === REGISTRO DE DEBUG: Onde está faltando dado? ===
        if not actor: falhas["sem_actor"] += 1
        if raw is None: falhas["sem_raw"] += 1
        if not max_score: falhas["sem_max"] += 1
        if not materia: falhas["sem_materia"] += 1
        if not quiz_id: falhas["sem_quiz_id"] += 1
        # ===================================================

        if actor and raw is not None and max_score and materia and quiz_id:
            atual = usuarios[actor][materia].get(quiz_id, {"acertos": 0, "total_questoes": max_score})
            if raw > atual["acertos"]:
                usuarios[actor][materia][quiz_id] = {
                    "acertos": raw,
                    "total_questoes": max_score
                }

    # === IMPRESSÃO DO DIAGNÓSTICO FINAL ===
    print("\n" + "="*40)
    print("        RELATÓRIO DE DEBUG")
    print("="*40)
    print(f"Total de statements recebidos: {len(statements)}")
    print(f"Falhas por falta de Actor (usuário): {falhas['sem_actor']}")
    print(f"Falhas por falta de Nota Raw (score): {falhas['sem_raw']}")
    print(f"Falhas por falta de Nota Max (score max): {falhas['sem_max']}")
    print(f"Falhas por falta de Matéria (course parent): {falhas['sem_materia']}")
    print(f"Falhas por falta de Quiz ID (quiz parent): {falhas['sem_quiz_id']}")
    print("="*40)

    if len(statements) > 0 and not usuarios:
        print("\n[ALERTA] Nenhuma linha passou no IF! Veja a estrutura real do seu primeiro statement:")
        print(json.dumps(statements[0], indent=2, ensure_ascii=False))
        print("="*40 + "\n")
    # ======================================

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
