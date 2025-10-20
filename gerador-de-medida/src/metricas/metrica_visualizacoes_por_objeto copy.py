import json
import os

def calcular_visualizacoes_por_objeto(caminho_arquivo_entrada, caminho_arquivo_saida="resultado_calcular_visualizacoes_por_objeto.json"):
    """
    Carrega dados de atividades, calcula a métrica VC e salva o resultado em um novo JSON.

    A métrica VC (Visualizações por Objeto de Conteúdo) é calculada por seção como:
    VC = Total de visualizações na seção / Número de objetos únicos acessados na seção

    Args:
        caminho_arquivo_entrada (str): O caminho completo para o arquivo JSON de atividades (ex: 'data/atividades.json').
        caminho_arquivo_saida (str): O nome do arquivo JSON onde o resultado será salvo.
    """
    # --- Passo 1: Ler e validar o arquivo de entrada ---
    if not os.path.exists(caminho_arquivo_entrada):
        print(f"Erro: O arquivo de entrada '{caminho_arquivo_entrada}' não foi encontrado.")
        return

    try:
        with open(caminho_arquivo_entrada, "r", encoding="utf-8") as f:
            dados_atividades = json.load(f)
    except json.JSONDecodeError:
        print(f"Erro: O arquivo '{caminho_arquivo_entrada}' não é um JSON válido.")
        return
    except Exception as e:
        print(f"Ocorreu um erro inesperado ao ler o arquivo: {e}")
        return

    # --- Passo 2: Calcular a métrica VC ---
    resultados_vc = {}

    # Itera sobre cada curso no arquivo
    for curso_nome, curso_info in dados_atividades.items():
        resultados_vc[curso_nome] = {"sessoes": {}}
        sessoes = curso_info.get("sessoes", {}) # Acessa o dicionário de seções

        # Itera sobre cada seção dentro do curso
        for sessao_id, sessao_info in sessoes.items():
            atividades = sessao_info.get("atividades", {}) # Acessa as atividades da seção

            total_visualizacoes_sessao = 0
            objetos_unicos_acessados_sessao = 0

            # Itera sobre cada atividade para somar as visualizações
            for atividade_id, atividade_info in atividades.items():
                # Extrai a quantidade de visualizações de cada atividade
                qtd_viewed = atividade_info.get("usuarios", {}).get("qtd_viewed", 0)
                
                total_visualizacoes_sessao += qtd_viewed

                # Se a atividade teve ao menos uma visualização, conta como um objeto acessado
                if qtd_viewed > 0:
                    objetos_unicos_acessados_sessao += 1

            # Evita divisão por zero se nenhuma atividade foi acessada na seção
            if objetos_unicos_acessados_sessao > 0:
                vc_sessao = total_visualizacoes_sessao / objetos_unicos_acessados_sessao
            else:
                vc_sessao = 0.0

            # Armazena os resultados calculados para a seção
            resultados_vc[curso_nome]["sessoes"][sessao_id] = {
                "total_visualizacoes": total_visualizacoes_sessao,
                "objetos_unicos_acessados": objetos_unicos_acessados_sessao,
                "vc_visualizacoes_por_objeto": round(vc_sessao, 2)
            }

    # --- Passo 3: Salvar o resultado em um novo arquivo JSON ---
    try:
        with open(caminho_arquivo_saida, "w", encoding="utf-8") as f:
            json.dump(resultados_vc, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"Erro ao salvar o arquivo de resultado: {e}")

# Exemplo de uso
if __name__ == "__main__":
    arquivo_json = "../../data/atividades.json"

    calcular_visualizacoes_por_objeto(arquivo_json)