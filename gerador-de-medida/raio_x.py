import pandas as pd

try:
    print("--- RAIO-X DO ARQUIVO DE LOGS ---")
    df = pd.read_csv("Reduzido_Quiz.csv")
    
    print(f"Total de linhas (cliques encontrados): {len(df)}")
    if len(df) > 0:
        print("\nNome das colunas disponíveis:")
        print(list(df.columns))
        print("\nExemplo da primeira linha de dados:")
        print(df.iloc[0].to_dict())
    else:
        print("\nALERTA: O seu arquivo está completamente vazio! O filtro do Pandas não encontrou nada.")

except Exception as e:
    print(f"Erro ao ler o arquivo: {e}")