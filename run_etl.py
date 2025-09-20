"""objetivo: conectar ao banco e ler o csv"""
import pandas as pd
from etl import database, transformer, loader

NOME_ARQUIVO_ENTRADA = "raw_tweets.csv"

def main():
    print("INICIANDO PIPELINE DE TRANSFORMAÇÃO E CARGA (TL)")
    try:
        df_bruto = pd.read_csv(NOME_ARQUIVO_ENTRADA)
    except FileNotFoundError:
        print(f"\n[ERRO] O arquivo de entrada '{NOME_ARQUIVO_ENTRADA}' não foi encontrado.")
        return
    df_transformado = transformer.transformar_dados(df_bruto)
    conn = database.connect()
    if conn:
        try:
            loader.carregar_dados(conn, df_transformado)
            print("PIPELINE TL CONCLUÍDO COM SUCESSO")
        finally:
            conn.close()
    else:
        print("Falha na conexão com o banco. O processo de carga foi abortado.")

if __name__ == "__main__":
    main()