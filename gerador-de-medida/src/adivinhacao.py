import json
import os
import re
from datetime import datetime
from src.fetch_statements import fetch_statements

# Caminho do arquivo JSON final
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_FILE = os.path.join(BASE_DIR, "..", "data", "atividades.json")

# Padrões para expressões regulares
RE_SLOT = re.compile(r" Review Slot\s+\d+$", re.IGNORECASE)
RE_ATTEMPT = re.compile(r"\s+Attempt\s+\d+$", re.IGNORECASE)

# Formato de data e hora do xAPI (ISO 8601 com e sem milissegundos)
DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ" 
DATETIME_FORMAT_NO_MS = "%Y-%m-%dT%H:%M:%SZ" 

# Função auxiliar para parsear o timestamp, lidando com formatos comuns
def parse_timestamp(ts_string):
    try:
        # Tenta o formato com milissegundos
        return datetime.strptime(ts_string, DATETIME_FORMAT)
    except ValueError:
        try:
            # Tenta o formato sem milissegundos
            return datetime.strptime(ts_string, DATETIME_FORMAT_NO_MS)
        except ValueError as e:
            # print(f"DEBUG: Falha ao parsear timestamp '{ts_string}': {e}")
            return None

# Funções de manipulação de arquivo JSON
def carregar_json_existente():
    if os.path.exists(OUTPUT_FILE):
        with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
            try:
                return json.load(f)

            except json.JSONDecodeError:
                return {}

    return {}

def salvar_json(dados):
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)

def extrair_id_atividade(url):
    match = re.search(r"id=(\d+)", url)
    return match.group(1) if match else "sem_id"

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

def limpar_nome_atividade(nome):
    nome = RE_ATTEMPT.sub("", nome).strip()
    return nome

def extrair_atividade_principal_revisao(st):
    context_activities = st.get("context", {}).get("contextActivities", {})
    parents = context_activities.get("parent", [])
    usuario = st.get("actor", {}).get("account", {}).get("name", "Usuário Desconhecido")
    
    for p in parents:
        atividade_type = p.get("definition", {}).get("type", "")
        if "assessment" in atividade_type or "quiz" in atividade_type:
            atividade_id = extrair_id_atividade(p.get("id", ""))
            atividade_nome = limpar_nome_atividade(p.get("definition", {}).get("name", {}).get("en", "Sem nome"))

            if atividade_id != "sem_id":
                return atividade_id, atividade_nome, usuario
            else:
                # print(f"DEBUG: Falha na extração (Revisão): ID da atividade principal é 'sem_id' para statement: {st.get('id', 'N/A')}")
                return None, None, None
                
    # print(f"DEBUG: Falha na extração (Revisão): Não encontrou atividade 'assessment/quiz' em parents para statement: {st.get('id', 'N/A')}")
    return None, None, None

# Função para processar os statements
def processar_statements(statements):
    dados = carregar_json_existente()

    for st in statements:
        verbo_id = st.get("verb", {}).get("id", "")
        objeto_id = st.get("object", {}).get("id", "")
        objeto_nome = st.get("object", {}).get("definition", {}).get("name", {}).get("en", "")
        timestamp = st.get("timestamp")
        
        if not timestamp:
            continue

        st_datetime = parse_timestamp(timestamp)
        if st_datetime is None:
            continue

        atividade = st.get("object", {})
        context = st.get("context", {}).get("contextActivities", {})
        
        curso, sessao_id = extrair_curso_sessao(context)
        if not curso or not sessao_id:
            continue

        atividade_id, atividade_nome, usuario, acao_tipo = None, None, None, None

        if "scored" in verbo_id:
            atividade_id, atividade_nome, usuario = extrair_atividade_principal_revisao(st)
            acao_tipo = "received_review"
            
        elif "receive" in verbo_id and "review" in objeto_id.lower() and "review" in objeto_nome.lower():
            actor_name = st.get("actor", {}).get("account", {}).get("name")
            instructor_name = st.get("context", {}).get("instructor", {}).get("account", {}).get("name")
            
            if actor_name == instructor_name:
                atividade_id, atividade_nome, usuario = extrair_atividade_principal_revisao(st)
                acao_tipo = "viewed_review"
            else:
                continue

        elif "viewed" in verbo_id or "completed" in verbo_id:
            atividade_id = extrair_id_atividade(atividade.get("id", ""))
            
            if atividade_id == "sem_id":
                continue
            
            atividade_nome = limpar_nome_atividade(atividade.get("definition", {}).get("name", {}).get("en", "Sem nome"))
            usuario = st.get("actor", {}).get("account", {}).get("name", "Usuário Desconhecido")
            acao_tipo = "viewed" if "viewed" in verbo_id else "completed"
        
        else:
            continue
            
        if not atividade_id:
            continue
        
        # Inicialização do Curso, Sessão e Atividade
        if curso not in dados:
            dados[curso] = {"curso": curso, "sessoes": {}}

        if sessao_id not in dados[curso]["sessoes"]:
            dados[curso]["sessoes"][sessao_id] = {"sessao_id": sessao_id, "atividades": {}}

        if atividade_id not in dados[curso]["sessoes"][sessao_id]["atividades"]:
            dados[curso]["sessoes"][sessao_id]["atividades"][atividade_id] = {
                "id": atividade_id,
                "nome": atividade_nome,
                "usuarios": {
                    "usuarios_viewed": [],
                    "usuarios_completed": [],
                    "usuarios_received_review": [],
                    "usuarios_viewed_review": [],
                    "qtd_viewed": 0,
                    "qtd_completed": 0,
                    "qtd_received_review": 0,
                    "qtd_viewed_review": 0
                }
            }
        
        usuarios_data = dados[curso]["sessoes"][sessao_id]["atividades"][atividade_id]["usuarios"]
        dados[curso]["sessoes"][sessao_id]["atividades"][atividade_id]["nome"] = atividade_nome 
        
        # Garante a existência das chaves
        for key in ["usuarios_viewed", "usuarios_completed", "usuarios_received_review", "qtd_received_review", "usuarios_viewed_review", "qtd_viewed_review", "qtd_viewed", "qtd_completed"]:
             if key not in usuarios_data:
                usuarios_data[key] = [] if "usuarios" in key else 0

        # Atualiza os dados de acordo com a ação (verbo)
        if acao_tipo == "viewed":
            ja_visualizou = any(item['usuario'] == usuario for item in usuarios_data["usuarios_viewed"])
            
            if not ja_visualizou:
                usuarios_data["usuarios_viewed"].append({
                    "usuario": usuario, 
                    "timestamp": timestamp
                })
                usuarios_data["qtd_viewed"] = len(usuarios_data["usuarios_viewed"])

        elif acao_tipo == "completed":
            ja_completou = any(item['usuario'] == usuario for item in usuarios_data["usuarios_completed"])
            
            if not ja_completou:
                usuarios_data["usuarios_completed"].append({
                    "usuario": usuario, 
                    "timestamp": timestamp
                })
                usuarios_data["qtd_completed"] = len(usuarios_data["usuarios_completed"])

        elif acao_tipo == "received_review":
            ja_recebeu = any(item['usuario'] == usuario for item in usuarios_data["usuarios_received_review"])
            
            if not ja_recebeu:
                usuarios_data["usuarios_received_review"].append({
                    "usuario": usuario, 
                    "timestamp": timestamp 
                })
                usuarios_data["qtd_received_review"] = len(usuarios_data["usuarios_received_review"])

        elif acao_tipo == "viewed_review":
            # Lógica de verificação estrita: Recebido deve existir e ser temporalmente anterior ou igual.
            
            pode_contar = False
            
            received_reviews = [item for item in usuarios_data["usuarios_received_review"] if item['usuario'] == usuario]
            
            if received_reviews:
                received_timestamp_str = received_reviews[-1]['timestamp']
                received_datetime = parse_timestamp(received_timestamp_str)
                
                if received_datetime:
                    if st_datetime >= received_datetime:
                        pode_contar = True
            
            if pode_contar:
                ja_visualizou_review = any(item == usuario for item in usuarios_data["usuarios_viewed_review"])
                
                if not ja_visualizou_review:
                    usuarios_data["usuarios_viewed_review"].append(usuario)
                    usuarios_data["qtd_viewed_review"] = len(usuarios_data["usuarios_viewed_review"])


    salvar_json(dados)

def adivinhar(statements):
    # A dupla chamada serve para garantir que statements de 'received_review' sejam processados antes dos 'viewed_review' se a ordem dos dados for inconsistente
    processar_statements(statements)
    processar_statements(statements)

if __name__ == "__main__":
    statements = fetch_statements({
        "limit": 1000
    })

    adivinhar(statements)