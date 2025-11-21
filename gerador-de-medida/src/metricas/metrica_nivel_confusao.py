import json
import os

def get_numero_de_trocas(caminho_arquivo, curso_id, sessao_id, atividade_id, usuario_id):
    """
    Retorna a quantidade de vezes que o aluno trocou a alternativa escolhida
    antes de submeter a resposta final.
    
    Exemplo de lógica futura: Consultar tabela de logs de eventos 'user_updated_answer'.
    """
    return False

def get_tempo_interacao(caminho_arquivo, curso_id, sessao_id, atividade_id, usuario_id):
    """
    Retorna o tempo total (em segundos) que o aluno passou na questão/atividade.
    Um tempo muito alto combinado com muitas trocas indica maior confusão.
    """
    return False

def get_limiar_tempo_esperado(caminho_arquivo, curso_id, sessao_id, atividade_id):
    """
    Retorna o tempo médio estimado pelo professor para resolver a questão.
    Serve para comparar se o tempo do aluno foi 'excessivamente longo'.
    """
    return False

def calcular_score_confusao(qtd_trocas, tempo_aluno, tempo_esperado):
    """
    Calcula o Nível de Confusão baseado nas premissas de Leitão (2017).
    
    Lógica:
    1. A base da confusão é o número de trocas.
    2. Se o tempo for excessivo (> 1.5x o esperado) E houver trocas, a confusão é penalizada (aumentada).
    
    Retorna:
        float: Um score sugerido de 0.0 a 1.0 (normalizado) ou o valor bruto.
    """
    if qtd_trocas is False or tempo_aluno is False:
        return None

    # Definição simplificada de peso para o exemplo
    score_base = qtd_trocas * 1.0 
    
    # Fator de amplificação por tempo excessivo
    fator_tempo = 1.0
    if tempo_esperado and tempo_aluno > (tempo_esperado * 1.5):
        fator_tempo = 1.2 # Aumenta a confusão em 20% se demorou muito

    nivel_confusao = score_base * fator_tempo
    
    return round(nivel_confusao, 2)

def calcular_nivel_confusao(caminho_arquivo_entrada, caminho_arquivo_saida="resultado_nivel_confusao.json"):
    """
    Itera sobre os dados, coleta informações via getters e aplica a lógica de confusão.
    Salva o resultado em JSON.
    """
    
    if not os.path.exists(caminho_arquivo_entrada):
        print(f"Erro: O arquivo '{caminho_arquivo_entrada}' não foi encontrado.")
        return

    try:
        with open(caminho_arquivo_entrada, "r", encoding="utf-8") as f:
            dados_atividades = json.load(f)
    except json.JSONDecodeError:
        print("Erro: O arquivo de entrada não é um JSON válido.")
        return

    resultados_confusao = {}

    for curso_nome, curso_data in dados_atividades.items():
        resultados_confusao[curso_nome] = {"sessoes": {}}
        
        sessoes = curso_data.get("sessoes", {})
        for sessao_id, sessao_data in sessoes.items():
            resultados_confusao[curso_nome]["sessoes"][sessao_id] = {"atividades": {}}
            
            atividades = sessao_data.get("atividades", {})
            for atividade_id, atividade_data in atividades.items():
                
                resultados_confusao[curso_nome]["sessoes"][sessao_id]["atividades"][atividade_id] = {
                    "nome": atividade_data.get("nome"),
                    "analise_confusao_usuarios": {}
                }

                usuarios_completed = atividade_data.get("usuarios", {}).get("usuarios_completed", [])
                
                if not usuarios_completed:
                     pass

                for user_entry in usuarios_completed:
                    usuario_id = user_entry.get("usuario")
                    
                    qtd_trocas = get_numero_de_trocas(caminho_arquivo_entrada, curso_nome, sessao_id, atividade_id, usuario_id)
                    tempo_gasto = get_tempo_interacao(caminho_arquivo_entrada, curso_nome, sessao_id, atividade_id, usuario_id)
                    tempo_esperado = get_limiar_tempo_esperado(caminho_arquivo_entrada, curso_nome, sessao_id, atividade_id)
                    
                    resultado_user = {
                        "nivel_confusao": None,
                        "dados_brutos": {
                            "trocas_resposta": "N/A",
                            "tempo_gasto": "N/A"
                        },
                        "status": "Não calculado",
                        "mensagem": ""
                    }

                    if qtd_trocas is not False and tempo_gasto is not False:
                        
                        score = calcular_score_confusao(qtd_trocas, tempo_gasto, tempo_esperado)
                        
                        resultado_user["nivel_confusao"] = score
                        resultado_user["dados_brutos"]["trocas_resposta"] = qtd_trocas
                        resultado_user["dados_brutos"]["tempo_gasto"] = tempo_gasto
                        
                        if score == 0:
                            resultado_user["status"] = "Baixa Incerteza (Fluxo Direto)"
                        elif score > 3:
                            resultado_user["status"] = "Alta Incerteza (Muitas Trocas)"
                        else:
                            resultado_user["status"] = "Incerteza Moderada"
                            
                    else:
                        resultado_user["status"] = "Dados Insuficientes"
                        resultado_user["mensagem"] = (
                            "Não foi possível detectar trocas de alternativas. "
                            "O arquivo 'atividades.json' não possui logs de interação (cliques) intra-atividade."
                        )

                    resultados_confusao[curso_nome]["sessoes"][sessao_id]["atividades"][atividade_id]["analise_confusao_usuarios"][usuario_id] = resultado_user

    try:
        with open(caminho_arquivo_saida, "w", encoding="utf-8") as f:
            json.dump(resultados_confusao, f, indent=4, ensure_ascii=False)
        print(f"Cálculo de Nível de Confusão concluído. Arquivo salvo em: {caminho_arquivo_saida}")
    except Exception as e:
        print(f"Erro crítico ao salvar JSON: {e}")

if __name__ == "__main__":
    arquivo_entrada = "atividades.json"
    arquivo_saida = "resultado_nivel_confusao.json"
    
    calcular_nivel_confusao(arquivo_entrada, arquivo_saida)