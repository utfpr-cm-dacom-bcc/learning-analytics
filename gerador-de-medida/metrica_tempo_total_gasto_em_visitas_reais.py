import json
from datetime import datetime
from fetch_statements import fetch_statements

def calcular_tempo_total_gasto_em_visitas_reais(statements):
    # Ordena statements por timestamp (garante ordem cronológica)
    statements.sort(key=lambda s: s.get("timestamp", ""))

    # Agrupa por usuário
    usuarios_statements = {}
    for statement in statements:
        actor = statement.get("actor", {}).get("account", {}).get("name")
        if not actor:
            continue
        usuarios_statements.setdefault(actor, []).append(statement)

    resultado = []

    for usuario, stmts in usuarios_statements.items():
        login_time = None
        last_activity_before_next_login = None

        for i, statement in enumerate(stmts):
            timestamp_str = statement.get("timestamp")
            if not timestamp_str:
                continue
            try:
                ts = datetime.fromisoformat(timestamp_str.replace("Z", "+00:00"))
            except ValueError:
                continue

            verb_display = (
                statement.get("verb", {})
                .get("display", {})
                .get("en", "")
                .strip()
                .lower()
            )

            if verb_display == "logged in":
                # Se já havia um login anterior, finaliza a sessão anterior
                if login_time is not None and last_activity_before_next_login is not None:
                    diff_seconds = int((last_activity_before_next_login - login_time).total_seconds())
                    duration_str = f"PT{diff_seconds}S"
                    resultado.append({
                        "usuario": usuario,
                        "timestamp_login": login_time.isoformat(),
                        "timestamp_atividade": last_activity_before_next_login.isoformat(),
                        "tempo_passado": duration_str
                    })

                # Inicia nova sessão
                login_time = ts
                last_activity_before_next_login = None
            else:
                # Atualiza última atividade na sessão atual
                if login_time is not None:
                    last_activity_before_next_login = ts

        # Se terminou os statements e ainda tem sessão aberta, finaliza com a última atividade encontrada
        if login_time is not None and last_activity_before_next_login is not None:
            diff_seconds = int((last_activity_before_next_login - login_time).total_seconds())
            duration_str = f"PT{diff_seconds}S"
            resultado.append({
                "usuario": usuario,
                "timestamp_login": login_time.isoformat(),
                "timestamp_atividade": last_activity_before_next_login.isoformat(),
                "tempo_passado": duration_str
            })

    # Salva em JSON
    with open("resultado_tempo_total_gasto_em_visitas_reais.json", "w", encoding="utf-8") as f:
        json.dump(resultado, f, indent=2, ensure_ascii=False)

    return resultado


if __name__ == "__main__":
    statements = fetch_statements({
        "limit": 1000
    })
    calcular_tempo_total_gasto_em_visitas_reais(statements)