import json
import re

def calcular_tentativas_por_questionario(statements):
    # Dicionário para contar as tentativas: {(usuario, url_atividade): contagem}
    contagem_tentativas = {}

    for statement in statements:
        # 1. Identifica o usuário (Actor)
        actor = statement.get("actor", {}).get("account", {}).get("name")
        if not actor:
            continue

        # 2. Identifica o Verbo e a Extensão do Moodle
        verb_id = statement.get("verb", {}).get("id", "")
        extensions = statement.get("context", {}).get("extensions", {})
        component = extensions.get("http://moodle.org/ext/component", "")

        # 3. Filtro: Verifica se a ação é uma submissão de questionário
        # No Moodle, finalizar uma tentativa gera o component 'mod_quiz' e a action 'submitted' ou 'completed'
        if component == 'mod_quiz' and verb_id in [
            'http://activitystrea.ms/schema/1.0/submit',
            'http://adlnet.gov/expapi/verbs/completed'
        ]:
            # Pega as informações de identificação do objeto
            definition = statement.get("object", {}).get("definition", {})
            atividade_nome = definition.get("name", {}).get("en-US", "Questionário Desconhecido")
            object_id = statement.get("object", {}).get("id", "URL_Desconhecida")

            # Extrai o ID do curso a partir da URL criada no teste.py
            match_curso = re.search(r'course=(\d+)', object_id)
            materia = f"Curso ID {match_curso.group(1)}" if match_curso else "Desconhecida"
        
            chave = (actor, object_id, materia, atividade_nome)

            # 4. Incrementa o contador de tentativas para este aluno neste quiz específico
            if chave not in contagem_tentativas:
                contagem_tentativas[chave] = 0
            
            contagem_tentativas[chave] += 1

    # 5. Prepara a lista final formatada
    resultado = []
    for (usuario, object_id, materia, atividade_nome), total_tentativas in contagem_tentativas.items():
        resultado.append({
            "usuario": usuario,
            "materia": materia,
            "atividade": atividade_nome,
            "url_atividade": object_id,
            "total_tentativas": total_tentativas
        })

    # 6. Salva o JSON estruturado
    nome_arquivo = "resultado_tentativas_por_questionario.json"
    with open(nome_arquivo, "w", encoding="utf-8") as f:
        json.dump(resultado, f, indent=4, ensure_ascii=False)

    print(f"[Métrica] Processamento concluído! Encontradas submissões de questionários para {len(resultado)} usuários/instâncias.")
    return resultado

# Caso queira rodar este arquivo isoladamente (sem o teste_metrica.py)
if __name__ == "__main__":
    from src.scripts.load_statements_from_file import load_statements_from_file
    try:
        # Carrega o JSON simulado gerado pelo teste.py
        statements = load_statements_from_file("xapi_statements_simulados.json")
        calcular_tentativas_por_questionario(statements)
    except FileNotFoundError:
        print("Erro: O arquivo 'xapi_statements_simulados.json' não foi encontrado.")