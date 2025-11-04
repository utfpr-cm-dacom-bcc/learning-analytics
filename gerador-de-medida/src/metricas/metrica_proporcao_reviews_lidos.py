import json
import os
from collections import defaultdict

def calcular_feedback_lido_por_usuario(caminho_entrada, caminho_saida="resultado_feedback_lido_por_usuario.json"):
    """
    Carrega dados de 'atividades.json', calcula a métrica "Porcentagem de Feedback Lido (FR)"
    para cada USUÁRIO dentro de cada seção e salva o resultado.

    A métrica FR por usuário é calculada como:
    FR_Usuario = (Total de feedbacks lidos pelo usuário na seção) / 
                 (Total de feedbacks disponíveis para o usuário na seção) * 100

    Args:
        caminho_entrada (str): O caminho para o arquivo 'atividades.json'.
        caminho_saida (str): O nome do arquivo JSON onde o resultado será salvo.
    """
    
    # --- Passo 1: Ler e validar o arquivo de entrada ---
    if not os.path.exists(caminho_entrada):
        print(f"Erro: O arquivo de entrada '{caminho_entrada}' não foi encontrado.")
        return

    try:
        with open(caminho_entrada, "r", encoding="utf-8") as f:
            dados_atividades = json.load(f) # Carrega os dados
    except json.JSONDecodeError:
        print(f"Erro: O arquivo '{caminho_entrada}' não é um JSON válido.")
        return
    except Exception as e:
        print(f"Ocorreu um erro inesperado ao ler o arquivo: {e}")
        return

    # --- Passo 2: Calcular a métrica FR por usuário e por seção ---
    resultados_fr_cursos = {}

    # Itera sobre cada curso no arquivo
    for curso_nome, curso_info in dados_atividades.items():
        resultados_fr_cursos[curso_nome] = {"sessoes": {}}
        sessoes = curso_info.get("sessoes", {}) # Acessa o dicionário de seções

        # Itera sobre cada seção dentro do curso
        for sessao_id, sessao_info in sessoes.items():
            atividades = sessao_info.get("atividades", {}) # Acessa as atividades da seção

            # Dicionários para agregar contagens por usuário DENTRO desta seção
            feedbacks_disponiveis_por_usuario = defaultdict(int)
            feedbacks_lidos_por_usuario = defaultdict(int)
            
            # Dicionário para armazenar nomes de usuários (bônus)
            nomes_usuarios = {}

            # Itera sobre cada atividade na seção para somar os totais por usuário
            for atividade_id, atividade_info in atividades.items():
                usuarios_data = atividade_info.get("usuarios", {})
                
                # Conta feedbacks disponíveis (denominador)
                # A lista 'usuarios_received_review' contém objetos {"usuario": "ID", ...}
                for review_info in usuarios_data.get("usuarios_received_review", []):
                    usuario_id = review_info.get("usuario")
                    if usuario_id:
                        feedbacks_disponiveis_por_usuario[usuario_id] += 1
                        # Armazena o nome se ainda não tivermos (assumindo que o nome do usuário está no 'actor' dos dados originais)
                        # Como não temos o nome aqui, usaremos o ID.
                
                # Conta feedbacks lidos (numerador)
                # A lista 'usuarios_viewed_review' contém strings "ID"
                for usuario_id in usuarios_data.get("usuarios_viewed_review", []):
                    feedbacks_lidos_por_usuario[usuario_id] += 1

            # --- Agora, calcula a métrica para cada usuário na seção ---
            
            resultados_por_usuario = {}
            sessao_total_disponiveis = 0
            sessao_total_lidos = 0

            # Itera apenas sobre os usuários que tinham feedback disponível
            for usuario_id, total_disponivel in feedbacks_disponiveis_por_usuario.items():
                total_lido = feedbacks_lidos_por_usuario.get(usuario_id, 0) # Pega o total lido (ou 0 se não leu)
                
                # Calcula a porcentagem para este usuário
                if total_disponivel > 0:
                    percentual_usuario = (total_lido / total_disponivel) * 100
                else:
                    percentual_usuario = 0.0 # Caso de segurança, embora total_disponivel deva ser > 0 aqui
                
                resultados_por_usuario[usuario_id] = {
                    "feedbacks_disponiveis": total_disponivel,
                    "feedbacks_lidos": total_lido,
                    "fr_porcentagem_lida": round(percentual_usuario, 2)
                }
                
                # Soma para o total da seção
                sessao_total_disponiveis += total_disponivel
                sessao_total_lidos += total_lido

            # Calcula a métrica geral da seção
            if sessao_total_disponiveis > 0:
                fr_sessao_geral = (sessao_total_lidos / sessao_total_disponiveis) * 100
            else:
                fr_sessao_geral = 0.0

            # Armazena os resultados da seção (com os usuários aninhados)
            if sessao_total_disponiveis > 0:
                resultados_fr_cursos[curso_nome]["sessoes"][sessao_id] = {
                    "geral_sessao": {
                        "total_feedbacks_disponiveis_na_sessao": sessao_total_disponiveis,
                        "total_feedbacks_lidos_na_sessao": sessao_total_lidos,
                        "fr_porcentagem_lida_geral": round(fr_sessao_geral, 2)
                    },
                    "usuarios": resultados_por_usuario
                }

    # --- Passo 3: Salvar o resultado em um novo arquivo JSON ---
    try:
        with open(caminho_saida, "w", encoding="utf-8") as f:
            json.dump(resultados_fr_cursos, f, indent=4, ensure_ascii=False)
        print(f"Métrica 'FR por Usuário' calculada! Resultado salvo em '{caminho_saida}'.")
    except Exception as e:
        print(f"Erro ao salvar o arquivo de resultado '{caminho_saida}': {e}")


# --- Exemplo de uso ---
if __name__ == "__main__":
    # Caminho para o seu arquivo de entrada
    caminho_do_arquivo = "atividades.json" 
    
    # Nome do arquivo de saída
    arquivo_de_saida = "resultado_feedback_lido_por_usuario.json"

    try:
        calcular_feedback_lido_por_usuario(caminho_do_arquivo, arquivo_de_saida)
    except FileNotFoundError as e:
        print(e)
    except json.JSONDecodeError as e:
        print(e)
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")