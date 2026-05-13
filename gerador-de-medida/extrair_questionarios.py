import pandas as pd

# Lê o arquivo original gigante de logs
# Substitua o nome se o seu log principal se chamar diferente
print("Lendo o banco de dados gigante. Isso pode levar alguns segundos...")
df = pd.read_csv("mdl_logstore_standard_log.csv")

# Filtra estritamente as linhas onde o componente é um questionário
df_quiz = df[df['component'] == 'mod_quiz']

# Salva esse arquivo filtrado para usarmos na esteira
df_quiz.to_csv("Reduzido_Quiz.csv", index=False)

print(f"Sucesso! Encontramos {len(df_quiz)} cliques em questionários.")
print("Arquivo 'Reduzido_Quiz.csv' criado!")