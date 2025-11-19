import json
import os

# --- Funções de Coleta de Dados (Stubs/Placeholders) ---

def get_idt(caminho_arquivo, curso_id, sessao_id, atividade_id, questao_id):
    """Retorna o Índice de Dificuldade do Tópico (IDT)."""
    return False

def get_idc(caminho_arquivo, curso_id, sessao_id, atividade_id, questao_id):
    """Retorna o Índice de Dificuldade do Conceito (IDC)."""
    return False

def get_idq(caminho_arquivo, curso_id, sessao_id, atividade_id, questao_id):
    """Retorna o Índice de Dificuldade da Questão (IDQ)."""
    return False

def get_desvio(caminho_arquivo, curso_id, sessao_id, atividade_id, questao_id, alternativa_id):
    """
    Retorna o Desvio (proximidade da alternativa marcada em relação à correta).
    Geralmente 1.0 para acerto total, valores menores para erros parciais.
    """
    return False

def get_tempo_de_resposta(caminho_arquivo, curso_id, sessao_id, atividade_id, questao_id, usuario_id):
    """
    Retorna o Tempo de Resposta do aluno para a questão específica.
    Deve ser um valor numérico (ex: segundos ou minutos).
    """
    return False

# --- Função Principal ---

def calcular_nivel_compreensao(caminho_arquivo_entrada, caminho_arquivo_saida):
    """
    Calcula a métrica Lu (Nível de Compreensão) percorrendo a estrutura do JSON.
    Lu = (IDT * IDC * IDQ * Desvio) / TempoDeResposta
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

    resultados_lu = {}

    for curso_nome, curso_data in dados_atividades.items():
        resultados_lu[curso_nome] = {"sessoes": {}}
        
        sessoes = curso_data.get("sessoes", {})
        for sessao_id, sessao_data in sessoes.items():
            resultados_lu[curso_nome]["sessoes"][sessao_id] = {"atividades": {}}
            
            atividades = sessao_data.get("atividades", {})
            for atividade_id, atividade_data in atividades.items():
                
                resultados_lu[curso_nome]["sessoes"][sessao_id]["atividades"][atividade_id] = {
                    "nome": atividade_data.get("nome"),
                    "usuarios_analisados": {}
                }

                usuarios_completed = atividade_data.get("usuarios", {}).get("usuarios_completed", [])

                for user_entry in usuarios_completed:
                    usuario_id = user_entry.get("usuario")
                    
                    # O arquivo atividades.json para no nível de 'Atividade'.
                    # A métrica de Leitão exige nível de 'Questão' e 'Alternativa'.
                    # Como não temos esses dados no JSON, definimos como None para sinalizar aos 'gets' e ao log de erro.
                    questao_id = None 
                    alternativa_id = None # O ID da resposta que o aluno deu
                    
                    # Chamada aos Getters com o contexto completo
                    idt = get_idt(caminho_arquivo_entrada, curso_nome, sessao_id, atividade_id, questao_id)
                    idc = get_idc(caminho_arquivo_entrada, curso_nome, sessao_id, atividade_id, questao_id)
                    idq = get_idq(caminho_arquivo_entrada, curso_nome, sessao_id, atividade_id, questao_id)
                    desvio = get_desvio(caminho_arquivo_entrada, curso_nome, sessao_id, atividade_id, questao_id, alternativa_id)
                    tempo = get_tempo_de_resposta(caminho_arquivo_entrada, curso_nome, sessao_id, atividade_id, questao_id, usuario_id)

                    # Lógica de Cálculo e Validação
                    resultado_usuario = {
                        "Lu_nivel_compreensao": None,
                        "status": "Não calculado",
                        "detalhes_erro": []
                    }

                    parametros_validos = True
                    
                    # Checagem de dados faltantes
                    if questao_id is None:
                        resultado_usuario["detalhes_erro"].append("Aviso: JSON de entrada não detalha questões individuais dentro da atividade.")
                        parametros_validos = False

                    if any(v is False for v in [idt, idc, idq, desvio, tempo]):
                        resultado_usuario["detalhes_erro"].append("Faltam valores métricos (retorno False nos getters).")
                        parametros_validos = False

                    if tempo == 0:
                        resultado_usuario["detalhes_erro"].append("Tempo de resposta igual a zero (divisão impossível).")
                        parametros_validos = False

                    # Cálculo Matemático
                    if parametros_validos:
                        try:
                            # Fórmula: Lu = (IDT * IDC * IDQ * Desvio) / Tempo
                            lu = (idt * idc * idq * desvio) / tempo
                            resultado_usuario["Lu_nivel_compreensao"] = round(lu, 4)
                            resultado_usuario["status"] = "Sucesso"
                        except Exception as e:
                            resultado_usuario["status"] = f"Erro matemático: {str(e)}"
                    else:
                        resultado_usuario["status"] = "Dados Insuficientes"

                    # Salva o resultado para este usuário nesta atividade
                    resultados_lu[curso_nome]["sessoes"][sessao_id]["atividades"][atividade_id]["usuarios_analisados"][usuario_id] = resultado_usuario

    try:
        with open(caminho_arquivo_saida, "w", encoding="utf-8") as f:
            json.dump(resultados_lu, f, indent=4, ensure_ascii=False)
        print(f"Processamento concluído. Resultados salvos em '{caminho_arquivo_saida}'.")
    except Exception as e:
        print(f"Erro ao salvar arquivo de saída: {e}")

if __name__ == "__main__":
    arquivo_json = "data/atividades.json"
    caminho_saida = "resultado_nivel_compreensao.json"
    
    calcular_nivel_compreensao(arquivo_json, caminho_saida)