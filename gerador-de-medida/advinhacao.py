import json
import os
import re
from fetch_statements import fetch_statements

# Caminho do arquivo JSON final
OUTPUT_FILE = "atividades.json"

# Função para carregar o JSON existente (se houver)
def carregar_json_existente():
    if os.path.exists(OUTPUT_FILE):
        with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {}
    return {}

# Função para salvar o JSON atualizado
def salvar_json(dados):
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)

# Extrair id da atividade a partir do link do object.id
def extrair_id_atividade(url):
    match = re.search(r"id=(\d+)", url)
    return match.group(1) if match else "sem_id"

# Extrair nome do curso e id da sessão
def extrair_curso_sessao(context_activities):
    if not context_activities:
        return None, None

    candidatos = context_activities.get("parent", []) + context_activities.get("grouping", [])
    for c in candidatos:
        nome = c.get("definition", {}).get("name", {}).get("en", "")
        if "Section" in nome:
            partes = nome.rsplit("Section", 1)
            curso = partes[0].strip()
            sessao_id = partes[1].strip()
            return curso, sessao_id
    return None, None

# Limpar nome da atividade (remover "Attempt X")
def limpar_nome_atividade(nome):
    return re.sub(r"\s+Attempt\s+\d+$", "", nome).strip()

# Função para processar os statements
def processar_statements(statements):
    dados = carregar_json_existente()

    for st in statements:
        verbo = st.get("verb", {}).get("id", "")
        if "viewed" not in verbo and "completed" not in verbo:
            continue  # ignora verbos que não sejam viewed ou completed

        atividade = st.get("object", {})
        context = st.get("context", {}).get("contextActivities", {})

        curso, sessao_id = extrair_curso_sessao(context)
        if not curso or not sessao_id:
            continue  # ignora statements sem curso/sessão válidos

        atividade_id = extrair_id_atividade(atividade.get("id", ""))
        atividade_nome = limpar_nome_atividade(atividade.get("definition", {}).get("name", {}).get("en", "Sem nome"))
        usuario = st.get("actor", {}).get("account", {}).get("name", "Usuário Desconhecido")

        # Se o curso ainda não existe, inicializa
        if curso not in dados:
            dados[curso] = {
                "curso": curso,
                "sessoes": {}
            }

        # Se a sessão ainda não existe dentro do curso, inicializa
        if sessao_id not in dados[curso]["sessoes"]:
            dados[curso]["sessoes"][sessao_id] = {
                "sessao_id": sessao_id,
                "atividades": {}
            }

        # Se a atividade ainda não existe dentro da sessão, inicializa
        if atividade_id not in dados[curso]["sessoes"][sessao_id]["atividades"]:
            dados[curso]["sessoes"][sessao_id]["atividades"][atividade_id] = {
                "id": atividade_id,
                "nome": atividade_nome,
                "usuarios": {
                    "usuarios_viewed": [],
                    "usuarios_completed": [],
                    "qtd_viewed": 0,
                    "qtd_completed": 0
                }
            }

        usuarios_data = dados[curso]["sessoes"][sessao_id]["atividades"][atividade_id]["usuarios"]

        # Atualiza os dados de acordo com o verbo
        if "viewed" in verbo:
            if usuario not in usuarios_data["usuarios_viewed"]:
                usuarios_data["usuarios_viewed"].append(usuario)
                usuarios_data["qtd_viewed"] = len(usuarios_data["usuarios_viewed"])

        elif "completed" in verbo:
            if usuario not in usuarios_data["usuarios_completed"]:
                usuarios_data["usuarios_completed"].append(usuario)
                usuarios_data["qtd_completed"] = len(usuarios_data["usuarios_completed"])

    salvar_json(dados)

# ==============================
# Exemplo de uso
# ==============================
if __name__ == "__main__":
    statements = fetch_statements({
        "limit": 1000
    })

    processar_statements(statements)