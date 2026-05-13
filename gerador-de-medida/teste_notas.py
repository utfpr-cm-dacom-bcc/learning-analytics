import csv
import json
from datetime import datetime

def converter_notas_para_xapi(caminho_notas, caminho_json):
    statements = []
    linhas_totais = 0
    linhas_sem_nota = 0

    try:
        # utf-8-sig resolve problemas de caracteres invisíveis no início do arquivo
        with open(caminho_notas, mode="r", encoding="utf-8-sig") as file:
            
            # Detetive de delimitador: verifica se o arquivo usa ',' ou ';'
            amostra = file.read(1024)
            file.seek(0) # Volta o cursor para o começo do arquivo
            delimitador_detectado = ';' if ';' in amostra and amostra.count(';') > amostra.count(',') else ','
            
            print(f"[*] Delimitador detectado: '{delimitador_detectado}'")
            
            reader = csv.DictReader(file, delimiter=delimitador_detectado)
            
            # Imprime as colunas encontradas para termos certeza
            print(f"[*] Colunas encontradas: {reader.fieldnames}\n")
            
            for row in reader:
                linhas_totais += 1
                
                # CORREÇÃO 1: O nome correto da coluna no seu CSV é 'username'
                userid = row.get("username", "").strip()
                itemid = row.get("itemid", "").strip()
                timemodified = row.get("timemodified", "").strip()
                
                # CORREÇÃO 2: Tenta a 'finalgrade'. Se estiver vazia, tenta a 'rawgrade'
                finalgrade = row.get("finalgrade", "").strip()
                if not finalgrade:
                    finalgrade = row.get("rawgrade", "").strip()
                
                # Agora o filtro vai funcionar perfeitamente
                if not userid or not finalgrade:
                    linhas_sem_nota += 1
                    continue

                try:
                    timestamp_iso = datetime.fromtimestamp(int(timemodified)).isoformat() + "Z"
                except (ValueError, TypeError):
                    timestamp_iso = datetime.utcnow().isoformat() + "Z"

                statement = {
                    "actor": {
                        "objectType": "Agent",
                        "account": {
                            "homePage": "http://seumoodle.com",
                            "name": userid
                        }
                    },
                    "verb": {
                        "id": "http://adlnet.gov/expapi/verbs/scored",
                        "display": {
                            "en-US": "scored",
                            "pt-BR": "pontuou"
                        }
                    },
                    "object": {
                        "objectType": "Activity",
                        "id": f"http://seumoodle.com/grade/item/{itemid}",
                        "definition": {
                            "name": {"pt-BR": f"Item de Avaliação {itemid}"}
                        }
                    },
                    "result": {
                        "score": {
                            "raw": float(finalgrade)
                        }
                    },
                    "timestamp": timestamp_iso
                }
                
                statements.append(statement)

    except FileNotFoundError:
        print(f"[Erro] O arquivo '{caminho_notas}' não foi encontrado.")
        return

    with open(caminho_json, "w", encoding="utf-8") as outfile:
        json.dump(statements, outfile, indent=4, ensure_ascii=False)

    # Relatório Final
    print("================ RELATÓRIO DE PROCESSAMENTO ================")
    print(f"Total de linhas lidas do CSV: {linhas_totais}")
    print(f"Linhas ignoradas (sem nota ou sem usuário): {linhas_sem_nota}")
    print(f"Registros gerados com SUCESSO: {len(statements)}")
    print("============================================================")

if __name__ == "__main__":
    converter_notas_para_xapi("mdl_grade_grades_history.csv", "xapi_notas.json")