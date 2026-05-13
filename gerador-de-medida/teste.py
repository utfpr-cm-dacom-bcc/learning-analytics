import csv
import json
from datetime import datetime

def converter_csv_moodle_para_xapi(caminho_csv, caminho_json):
    statements = []

    try:
        with open(caminho_csv, mode="r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            
            for row in reader:
                # 1. Extração dos dados (CORREÇÃO: Usando 'username' ao invés de 'userid')
                userid = row.get("username", "").strip()
                action = row.get("action", "").strip()
                component = row.get("component", "").strip()
                contextinstanceid = row.get("contextinstanceid", "0").strip()
                courseid = row.get("courseid", "0").strip()
                timecreated = row.get("timecreated", "").strip()
                
                # Filtro de ruído: Ignora se a coluna username estiver vazia, for 0 ou "nan"
                if not userid or userid == "0" or userid.startswith("-") or userid.lower() == "nan":
                    continue

                # 2. Definição Inteligente do Verbo (Identifica pedaços da palavra)
                action_lower = action.lower()
                if "submit" in action_lower:
                    verb_id = "http://activitystrea.ms/schema/1.0/submit"
                elif "view" in action_lower:
                    verb_id = "http://id.tincanapi.com/verb/viewed"
                elif "complet" in action_lower:
                    verb_id = "http://adlnet.gov/expapi/verbs/completed"
                elif "start" in action_lower or "launch" in action_lower:
                    verb_id = "http://adlnet.gov/expapi/verbs/launched"
                else:
                    verb_id = "http://adlnet.gov/expapi/verbs/interacted" # Fallback

                # 3. Definição do Objeto (A URL única daquela atividade específica)
                nome_modulo = component.replace("mod_", "") if component.startswith("mod_") else component
                object_id = f"http://seumoodle.com/mod/{nome_modulo}/view.php?id={contextinstanceid}&course={courseid}"
                
                # 4. Tratamento Temporal
                try:
                    timestamp_iso = datetime.fromtimestamp(int(timecreated)).isoformat() + "Z"
                except (ValueError, TypeError):
                    timestamp_iso = datetime.utcnow().isoformat() + "Z"

                # 5. Montagem do Statement xAPI
                statement = {
                    "actor": {
                        "objectType": "Agent",
                        "account": {
                            "homePage": "http://seumoodle.com",
                            "name": userid
                        }
                    },
                    "verb": {
                        "id": verb_id,
                        "display": {
                            "en-US": action # Salva a ação original do Moodle aqui para referência
                        }
                    },
                    "object": {
                        "objectType": "Activity",
                        "id": object_id,
                        "definition": {
                            "name": {
                                "en-US": f"Atividade do tipo {component}"
                            }
                        }
                    },
                    "context": {
                        "extensions": {
                            "http://moodle.org/ext/component": component,
                            "http://moodle.org/ext/courseid": courseid
                        }
                    },
                    "timestamp": timestamp_iso
                }
                
                statements.append(statement)

    except FileNotFoundError:
        print(f"[Erro] O arquivo '{caminho_csv}' não foi encontrado.")
        return

    # Salva o arquivo JSON final
    with open(caminho_json, "w", encoding="utf-8") as outfile:
        json.dump(statements, outfile, indent=4, ensure_ascii=False)

    print(f"[Conversão] Sucesso! {len(statements)} logs do Moodle foram convertidos para xAPI.")
    print(f"[Conversão] Arquivo gerado: '{caminho_json}'.")

if __name__ == "__main__":
    # Executa a conversão lendo o CSV focado em Questionários
    converter_csv_moodle_para_xapi("Reduzido_Quiz.csv", "xapi_statements_simulados.json")