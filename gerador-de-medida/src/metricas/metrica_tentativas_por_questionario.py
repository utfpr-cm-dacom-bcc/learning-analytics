import json
import re
from ..fetch_statements import fetch_statements

# def calcular_tentativas_por_questionario(statements):
#     tentativas_mais_recentes = {}

#     for statement in statements:
#         actor = statement.get("actor", {}).get("account", {}).get("name")

#         # Extraindo a "matéria"
#         materia = (
#             statement.get("context", {})
#             .get("contextActivities", {})
#             .get("parent", [{}])[0]
#             .get("definition", {})
#             .get("name", {})
#             .get("en")
#         ) or "Desconhecida"

#         # Extraindo a "atividade"
#         atividade = (
#             statement.get("object", {})
#             .get("definition", {})
#             .get("name", {})
#             .get("en")
#         )

#         # Pegando o número da tentativa e a parte fixa da atividade
#         match = re.search(r'(.*)\s+Attempt\s*(\d+)$', atividade or "")
#         if not match:
#             continue  # Se não bate o padrão, pula

#         atividade_base = match.group(1).strip()
#         tentativa_num = int(match.group(2))

#         if actor and atividade_base:
#             chave = (actor, materia, atividade_base)

#             # Guarda só se for a primeira vez ou se a tentativa atual for maior
#             if chave not in tentativas_mais_recentes or tentativa_num > tentativas_mais_recentes[chave]["tentativa_num"]:
#                 tentativas_mais_recentes[chave] = {
#                     "usuario": actor,
#                     "materia": materia,
#                     "atividade": f"{atividade_base} Attempt {tentativa_num}",
#                     "tentativas": str(tentativa_num),
#                     "tentativa_num": tentativa_num  # para comparação interna
#                 }

#     # Converte para lista e remove campo interno de controle
#     resultado = []
#     for registro in tentativas_mais_recentes.values():
#         registro.pop("tentativa_num", None)
#         resultado.append(registro)

#     with open("resultado_tentativas_por_questionario.json", "w", encoding="utf-8") as f:
#         json.dump(resultado, f, indent=2, ensure_ascii=False)

#     return resultado

def calcular_tentativas_por_questionario(statements):
    # Dicionário principal para guardar o placar de cada aluno
    # A "Chave" será a combinação única de: (Aluno, Materia, Atividade)
    contagem_tentativas = {}

    for statement in statements:
        # 1. O GATEKEEPER (Filtro): Só deixamos passar eventos de conclusão/entrega
        verb_id = statement.get("verb", {}).get("id", "")
        if "completed" not in verb_id:
            continue

        actor = statement.get("actor", {}).get("account", {}).get("name")
        if not actor:
            continue

        # 2. EXTRAINDO A MATÉRIA (Buscamos dentro do parent onde o type é 'course')
        parents = statement.get("context", {}).get("contextActivities", {}).get("parent", [])
        materia = "Desconhecida"
        for p in parents:
            tipo_contexto = p.get("definition", {}).get("type", "")
            if "course" in tipo_contexto:
                materia = p.get("definition", {}).get("name", {}).get("en", "Desconhecida")
                break

        # 3. EXTRAINDO A ATIVIDADE (Ex: "Quiz (ID: 28062)")
        atividade = statement.get("object", {}).get("definition", {}).get("name", {}).get("en")
        
        # Filtro opcional: Se quiser contar tentativas APENAS em questionários (Quiz)
        if not atividade or "Quiz" not in atividade:
            continue

        # 4. A LÓGICA DA CONTAGEM (O Coração da Métrica)
        chave = (actor, materia, atividade)

        # Se for a primeira vez que vemos esse aluno terminando esse Quiz, criamos o registro dele
        if chave not in contagem_tentativas:
            contagem_tentativas[chave] = {
                "usuario": actor,
                "materia": materia,
                "atividade": atividade,
                "total_tentativas": 0
            }
        
        # Como passamos pelo filtro do 'completed', somamos +1 tentativa matemática e real!
        contagem_tentativas[chave]["total_tentativas"] += 1

    # Converte o dicionário em uma lista bonita para exportar
    resultado = list(contagem_tentativas.values())

    with open("resultado_tentativas_por_questionario.json", "w", encoding="utf-8") as f:
        json.dump(resultado, f, indent=2, ensure_ascii=False)

    return resultado

if __name__ == "__main__":
    statements = fetch_statements({
        "verb": "http://adlnet.gov/expapi/verbs/completed",
        "limit": 1000
    })
    calcular_tentativas_por_questionario(statements)