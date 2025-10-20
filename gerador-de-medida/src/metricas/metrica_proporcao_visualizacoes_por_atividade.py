import json
import os

def calcular_proporcao_visualizacoes_por_atividade(caminho_entrada, caminho_saida="resultado_proporcao_visualizacoes.json"):
    """
    Carrega dados de atividades, calcula a proporção de visualizações de cada atividade
    em relação ao total da sua seção e salva o resultado em um novo JSON.

    A métrica calculada para cada atividade é:
    Proporção = (qtd_viewed da atividade) / (Total de qtd_viewed de todas as atividades na seção)

    Args:
        caminho_entrada (str): O caminho completo para o arquivo JSON de atividades (ex: 'data/atividades.json').
        caminho_saida (str): O nome do arquivo JSON onde o resultado será salvo.

    Raises:
        FileNotFoundError: Se o arquivo de entrada não for encontrado.
        json.JSONDecodeError: Se o arquivo de entrada não for um JSON válido.
    """
    # --- Passo 1: Ler e validar o arquivo de entrada ---
    if not os.path.exists(caminho_entrada):
        raise FileNotFoundError(f"Erro: O arquivo de entrada '{caminho_entrada}' não foi encontrado.")

    try:
        with open(caminho_entrada, "r", encoding="utf-8") as f:
            dados_atividades = json.load(f)
    except json.JSONDecodeError:
        raise json.JSONDecodeError(f"Erro: O arquivo '{caminho_entrada}' não é um JSON válido.", caminho_entrada, 0)
    except Exception as e:
        print(f"Ocorreu um erro inesperado ao ler o arquivo: {e}")
        return # Ou raise e para parar a execução

    # --- Passo 2: Calcular a métrica ---
    resultados_proporcao = {}

    # Itera sobre cada curso no arquivo
    for curso_nome, curso_info in dados_atividades.items():
        resultados_proporcao[curso_nome] = {"sessoes": {}}
        sessoes = curso_info.get("sessoes", {}) # Acessa o dicionário de seções

        # Itera sobre cada seção dentro do curso
        for sessao_id, sessao_info in sessoes.items():
            atividades = sessao_info.get("atividades", {}) # Acessa as atividades da seção
            resultados_proporcao[curso_nome]["sessoes"][sessao_id] = {
                "atividades": {},
                "total_visualizacoes_sessao": 0
            }

            # --- Primeiro, calcula o total de visualizações da seção ---
            total_visualizacoes_sessao = 0
            for atividade_id, atividade_info in atividades.items():
                total_visualizacoes_sessao += atividade_info.get("usuarios", {}).get("qtd_viewed", 0) # Soma qtd_viewed de cada atividade
            
            # Armazena o total para referência no resultado
            resultados_proporcao[curso_nome]["sessoes"][sessao_id]["total_visualizacoes_sessao"] = total_visualizacoes_sessao

            # --- Segundo, calcula a proporção para cada atividade na seção ---
            for atividade_id, atividade_info in atividades.items():
                qtd_viewed_atividade = atividade_info.get("usuarios", {}).get("qtd_viewed", 0) # Pega qtd_viewed da atividade atual
                nome_atividade = atividade_info.get("nome", f"ID_{atividade_id}") # Pega o nome da atividade

                # Calcula a proporção, evitando divisão por zero
                if total_visualizacoes_sessao > 0:
                    proporcao = qtd_viewed_atividade / total_visualizacoes_sessao
                else:
                    proporcao = 0.0

                # Armazena os resultados para esta atividade
                resultados_proporcao[curso_nome]["sessoes"][sessao_id]["atividades"][atividade_id] = {
                    "nome": nome_atividade,
                    "qtd_viewed_atividade": qtd_viewed_atividade,
                    "proporcao_visualizacoes_na_sessao_percentual": round(proporcao * 100, 2) # Salva como porcentagem arredondada
                }

    # --- Passo 3: Salvar o resultado em um novo arquivo JSON ---
    try:
        with open(caminho_saida, "w", encoding="utf-8") as f:
            json.dump(resultados_proporcao, f, indent=4, ensure_ascii=False)
        print(f"Métrica de proporção de visualizações calculada! Resultado salvo em '{caminho_saida}'.")
    except Exception as e:
        print(f"Erro ao salvar o arquivo de resultado '{caminho_saida}': {e}")


# --- Como usar a função ---
if __name__ == "__main__":
    # Defina o caminho para o seu arquivo de entrada aqui
    # Exemplo: Se o script está na mesma pasta que 'atividades.json'
    caminho_do_arquivo_json = "../../data/atividades.json" 
    # Exemplo: Se 'atividades.json' está em uma subpasta 'data'
    # caminho_do_arquivo_json = os.path.join("data", "atividades.json") 
    
    # Nome do arquivo de saída desejado
    arquivo_de_saida = "../../resultado_proporcao_views_por_atividade.json"

    try:
        calcular_proporcao_visualizacoes_por_atividade(caminho_do_arquivo_json, arquivo_de_saida)
    except FileNotFoundError as e:
        print(e)
    except json.JSONDecodeError as e:
        print(e)
    except Exception as e:
        print(f"Ocorreu um erro inesperado durante o cálculo: {e}")