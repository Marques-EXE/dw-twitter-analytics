""" objetivo: coletar dados da API e ADICIONAR ao arquivo CSV existente, sem duplicatas ou pelo menos tentar não passar KKKKKKKKKKKKKKK """
import config
import pandas as pd
from etl import extractor
import os

# o nome do arquivo onde os dados serão salvos
NOME_ARQUIVO_SAIDA = "raw_tweets.csv"

def main():
    """
    executa a etapa de extração e adiciona os novos dados ao CSV existente.
    
    """
    print(f"--- INICIANDO COLETA E APPEND DE DADOS DA API ---")
    
    df_antigo = pd.DataFrame()
    
    # verificar se o arquivo já existe e carregar dados antigos
    if os.path.exists(NOME_ARQUIVO_SAIDA):
        print(f"Arquivo '{NOME_ARQUIVO_SAIDA}' encontrado. Carregando dados existentes...")
        df_antigo = pd.read_csv(NOME_ARQUIVO_SAIDA)
        print(f"{len(df_antigo)} tweets carregados do arquivo local.")
    else:
        print(f"Arquivo '{NOME_ARQUIVO_SAIDA}' não encontrado. Um novo arquivo será criado.")

    # coletar novos dados da API
    print(f"\nBuscando por: '{config.QUERY_PESQUISA}' | Limite: {config.LIMITE_POSTS} posts.")
    df_novo = extractor.extrair_dados_twitter(
        config.QUERY_PESQUISA, 
        config.LIMITE_POSTS
    )

    if df_novo.empty:
        print("\n[AVISO] Nenhum dado novo foi retornado pela API. O arquivo não foi modificado.")
        return

    # juntar os DataFrames antigo e novo
    print("\nCombinando dados antigos e novos...")
    df_combinado = pd.concat([df_antigo, df_novo], ignore_index=True)

    # remover duplicatas (passo crucial!)
    contagem_antes = len(df_combinado)
    df_final = df_combinado.drop_duplicates(subset=['url'], keep='last')
    contagem_depois = len(df_final)
    
    duplicatas_removidas = contagem_antes - contagem_depois
    if duplicatas_removidas > 0:
        print(f"{duplicatas_removidas} tweets duplicados foram removidos.")

    # salvar o resultado final no arquivo CSV
    df_final.to_csv(NOME_ARQUIVO_SAIDA, index=False)
    
    print(f"\n[SUCESSO] O arquivo '{NOME_ARQUIVO_SAIDA}' foi atualizado.")
    print(f"Total de tweets no arquivo agora: {len(df_final)}")

if __name__ == "__main__":
    main()