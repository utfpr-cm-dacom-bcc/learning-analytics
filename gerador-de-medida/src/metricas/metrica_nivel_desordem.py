import json
import os
import math
from collections import Counter
from itertools import permutations

# --- Funções Auxiliares para Cálculo da Entropia de Permutação ---

def get_ordinal_pattern(window):
    """
    Calcula o padrão de ordem (permutação relativa) de uma janela.
    Ex: [3, 1, 2] -> o menor é 1, o intermediário é 2, o maior é 3. A ordem relativa é (2, 3, 1) -> Padrão 231.
    """
    # Cria tuplas (valor, índice_original)
    indexed_window = sorted([(val, idx) for idx, val in enumerate(window)], key=lambda x: x[0])
    # A ordem relativa é o índice original de cada elemento na janela ordenada
    # No exemplo [3, 1, 2]:
    # (1, 1) -> valor 1, índice original 1
    # (2, 2) -> valor 2, índice original 2
    # (3, 0) -> valor 3, índice original 0
    # A sequência de índices originais é (1, 2, 0).
    return tuple(x[1] for x in indexed_window)

def calculate_permutation_entropy(series, D=3, tau=1, normalize=True):
    """
    Calcula a Entropia de Permutação (H_o) da série.
    Args:
        series (list): A série numérica (a permutação pi).
        D (int): Dimensão de imersão (embedding dimension).
        tau (int): Atraso de tempo (time delay).
        normalize (bool): Se deve normalizar pela entropia máxima log2(D!).
    """
    n = len(series)
    if n < D:
        return 0.0

    # 1. Extrair os padrões ordinais
    patterns = []
    # Cria janelas de tamanho D com atraso tau
    for i in range(n - (D - 1) * tau):
        window = [series[i + j * tau] for j in range(D)]
        patterns.append(get_ordinal_pattern(window))

    # 2. Contar as frequências dos padrões
    pattern_counts = Counter(patterns)
    total_patterns = len(patterns)
    
    # 3. Calcular a Entropia de Shannon
    entropy = 0.0
    for count in pattern_counts.values():
        p_j = count / total_patterns
        if p_j > 0:
            entropy -= p_j * math.log2(p_j)
    
    # 4. Normalizar (para obter o Nível de Desordem)
    if normalize and D > 1:
        max_entropy = math.log2(math.factorial(D))
        if max_entropy > 0:
            return entropy / max_entropy
            
    return entropy

# --- Função Principal de Cálculo da Métrica ---

def calcular_nivel_desordem(caminho_arquivo_entrada, caminho_arquivo_saida="resultado_nivel_desordem.json", D=3):
    """
    Calcula o Nível de Desordem (H_o) para cada usuário por sessão
    baseado na entropia das permutações da ordem de resposta vs. a ordem esperada.

    Args:
        caminho_arquivo_entrada (str): Caminho para o arquivo JSON de atividades.
        caminho_arquivo_saida (str): Nome do arquivo JSON onde o resultado será salvo.
        D (int): Dimensão de imersão para a entropia de permutação (usado para o cálculo do Ho).
    """
    if not os.path.exists(caminho_arquivo_entrada):
        print(f"Erro: O arquivo de entrada '{caminho_arquivo_entrada}' não foi encontrado.")
        return

    try:
        with open(caminho_arquivo_entrada, "r", encoding="utf-8") as f:
            dados_atividades = json.load(f)
    except Exception as e:
        print(f"Ocorreu um erro ao ler ou decodificar o arquivo JSON: {e}")
        return

    resultados_desordem = {}

    for curso_nome, curso_info in dados_atividades.items():
        resultados_desordem[curso_nome] = {"sessoes": {}}
        sessoes = curso_info.get("sessoes", {})

        for sessao_id, sessao_info in sessoes.items():
            atividades = sessao_info.get("atividades", {})
            
            # 1. Determinar a ORDEM ESPERADA (P)
            # A ordem esperada é a ordem crescente dos IDs das atividades na sessão.
            # IDs são strings no JSON, então convertemos para int para ordenar.
            all_activity_ids = sorted([int(a_id) for a_id in atividades.keys()])
            
            # Se a sessão tem menos atividades que a dimensão D, não é possível calcular a permutação.
            if len(all_activity_ids) < D:
                resultados_desordem[curso_nome]["sessoes"][sessao_id] = {
                    "aviso": f"Mínimo de {D} atividades necessárias para calcular a métrica com D={D}. Atividades encontradas: {len(all_activity_ids)}.",
                    "nivel_desordem_por_usuario": {}
                }
                continue

            # Mapeamento do ID da Atividade para seu RANK na Ordem Esperada (P)
            # Ex: {10: 1, 20: 2, 30: 3, ...}
            activity_rank_map = {act_id: rank for rank, act_id in enumerate(all_activity_ids, 1)}

            # Armazenará a ordem de resposta do aluno: {usuario_id: [(timestamp, activity_id), ...]}
            user_timestamps = {}
            
            for atividade_id_str, atividade_info in atividades.items():
                atividade_id = int(atividade_id_str)
                # Usamos o timestamp de VISUALIZAÇÃO (response order)
                usuarios_viewed = atividade_info.get("usuarios", {}).get("usuarios_viewed", [])
                
                for view in usuarios_viewed:
                    usuario_id = view["usuario"]
                    timestamp = view["timestamp"]
                    
                    if usuario_id not in user_timestamps:
                        user_timestamps[usuario_id] = []
                    
                    user_timestamps[usuario_id].append((timestamp, atividade_id))

            # Armazenará o Nível de Desordem calculado para cada usuário
            disorder_by_user = {}

            for usuario_id, timestamps_list in user_timestamps.items():
                
                # 2. Determinar a ORDEM DE RESPOSTA (R)
                # Ordena as atividades do usuário pelo timestamp
                timestamps_list.sort(key=lambda x: x[0]) # x[0] é o timestamp
                observed_activity_order = [item[1] for item in timestamps_list] # A sequência de IDs
                
                # Garante que a ordem de resposta não tenha duplicatas
                # Em caso de múltiplas visualizações, consideramos apenas a primeira
                unique_observed_order = []
                seen_ids = set()
                for act_id in observed_activity_order:
                    if act_id not in seen_ids:
                        unique_observed_order.append(act_id)
                        seen_ids.add(act_id)
                
                # 3. Criar a Permutação pi (Série Temporal de Ranks)
                # pi = [rank(R1), rank(R2), rank(R3), ...]
                # O rank é baseado na Ordem Esperada (P)
                permutation_pi = [activity_rank_map[act_id] for act_id in unique_observed_order if act_id in activity_rank_map]

                # 4. Calcular o Nível de Desordem (Entropia de Permutação Normalizada)
                nivel_desordem = calculate_permutation_entropy(permutation_pi, D=D, normalize=True)
                
                disorder_by_user[usuario_id] = round(nivel_desordem, 4)

            # Armazena os resultados calculados para a sessão
            resultados_desordem[curso_nome]["sessoes"][sessao_id] = {
                "D": D,
                "total_atividades_na_sessao": len(all_activity_ids),
                "nivel_desordem_por_usuario": disorder_by_user
            }

    # Salva o resultado em um novo arquivo JSON
    try:
        with open(caminho_arquivo_saida, "w", encoding="utf-8") as f:
            json.dump(resultados_desordem, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"Erro ao salvar o arquivo de resultado: {e}")

# Exemplo de uso
if __name__ == "__main__":
    arquivo_json = "data/atividades.json"
    caminho_saida = "resultado_nivel_desordem_por_sessao.json"
    DIMENSAO_D = 3 

    calcular_nivel_desordem(arquivo_json, caminho_arquivo_saida=caminho_saida, D=DIMENSAO_D)