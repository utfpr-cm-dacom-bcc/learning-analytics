import json

def investigar_questionarios():
    try:
        with open("xapi_notas.json", "r", encoding="utf-8") as f:
            statements = json.load(f)
            
        acoes_moodle = set()
        
        for st in statements:
            # Pega o componente
            ext = st.get("context", {}).get("extensions", {})
            component = ext.get("http://moodle.org/ext/component", "")
            
            # Se for qualquer coisa relacionada a quiz, captura a ação original
            if "quiz" in component:
                acao = st.get("verb", {}).get("display", {}).get("en-US", "desconhecida")
                acoes_moodle.add(acao)
                
        print("================ RESULTADO DA INVESTIGAÇÃO ================")
        print("As ações reais que o Moodle registrou para questionários foram:")
        for a in acoes_moodle:
            print(f" -> {a}")
        print("===========================================================")
        
    except FileNotFoundError:
        print("Arquivo JSON não encontrado.")

if __name__ == "__main__":
    investigar_questionarios()