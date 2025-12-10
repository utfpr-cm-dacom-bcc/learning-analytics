import json
from collections import defaultdict

def calcular_porcentagem_do_curso_acessada(arquivo_json):
    with open(arquivo_json, "r", encoding="utf-8") as f:
        dados = json.load(f)

    resultados = {}

    # Percorre cada curso
    for curso_nome, curso_info in dados.items():
        sessoes = curso_info["sessoes"]

        # Primeiro, identificar todos os usuários que participaram do curso
        usuarios_curso = set()
        for sessao_id, sessao_info in sessoes.items():
            for atividade_id, atividade in sessao_info["atividades"].items():
                for u in atividade["usuarios"]["usuarios_viewed"]:
                    usuarios_curso.add(u["usuario"])
                for u in atividade["usuarios"]["usuarios_completed"]:
                    usuarios_curso.add(u["usuario"])

        # Preparar resultados por curso
        resultados[curso_nome] = {}

        # Para cada usuário do curso, calcular percentuais
        for usuario in usuarios_curso:
            resultados[curso_nome][usuario] = {"sessoes": {}, "geral": 0.0}

            total_atividades_curso = 0
            total_acessadas_curso = 0

            # Percorre cada sessão do curso
            for sessao_id, sessao_info in sessoes.items():
                atividades = sessao_info["atividades"]

                total_atividades_sessao = len(atividades)
                acessadas_sessao = 0

                # Contar quantas atividades o usuário acessou nessa sessão
                for atividade_id, atividade in atividades.items():
                    usuarios_viewed_ids = {u["usuario"] for u in atividade["usuarios"]["usuarios_viewed"]}
                    usuarios_completed_ids = {u["usuario"] for u in atividade["usuarios"]["usuarios_completed"]}

                    if (usuario in usuarios_viewed_ids or
                        usuario in usuarios_completed_ids):
                        acessadas_sessao += 1

                # Percentual por sessão
                percentual_sessao = (acessadas_sessao / total_atividades_sessao * 100
                                     if total_atividades_sessao > 0 else 0)

                resultados[curso_nome][usuario]["sessoes"][sessao_id] = round(percentual_sessao, 2)

                # Acumular para cálculo do curso
                total_atividades_curso += total_atividades_sessao
                total_acessadas_curso += acessadas_sessao

            # Percentual geral do curso
            percentual_curso = (total_acessadas_curso / total_atividades_curso * 100
                                if total_atividades_curso > 0 else 0)

            resultados[curso_nome][usuario]["geral"] = round(percentual_curso, 2)

    # Salvar resultados em JSON
    with open("resultado_porcentagem_do_curso_acessada.json", "w", encoding="utf-8") as f:
        json.dump(resultados, f, indent=4, ensure_ascii=False)


# Exemplo de uso
if __name__ == "__main__":
    arquivo_json = "atividades.json"

    calcular_porcentagem_do_curso_acessada(arquivo_json)