# prepare_dataset.py (VERSÃO FINAL COM CLASSIFICAÇÃO DE TEMAS)
import pandas as pd
import numpy as np

# --- CONFIGURAÇÕES ---
ARQUIVO_DE_ENTRADA = 'Twitterdatainsheets.csv'
ARQUIVO_DE_SAIDA = 'raw_tweets.csv'
NUMERO_DE_TWEETS = 200000

def classificar_tema(texto):
    """
    Classifica o tema de um tweet com base em palavras-chave no texto.
    """
    if not isinstance(texto, str):
        return 'Outros'
    
    texto = texto.lower()
    
    # Palavras-chave para cada tema
    temas = {
        'Tecnologia': ['aws', 'cloud', 'python', 'java', 'devops', 'software', 'dados', 'analytics', 'ia', 'ai'],
        'Futebol': ['futebol', 'jogo', 'time', 'campeonato', 'gol', 'copa', 'seleção', 'flamengo', 'palmeiras', 'corinthians', 'brasil'],
        'Política': ['política', 'governo', 'presidente', 'eleição', 'congresso', 'federal', 'senado', 'câmara'],
        'Entretenimento': ['filme', 'série', 'show', 'música', 'artista', 'cinema', 'novela', 'netflix', 'disney'],
        'Negócios': ['negócios', 'economia', 'investimento', 'mercado', 'empresa', 'finanças', 'bitcoin', 'crypto'],
    }
    
    for tema, palavras_chave in temas.items():
        for palavra in palavras_chave:
            if palavra in texto:
                return tema
    
    return 'Outros'

print(f"Lendo o dataset: {ARQUIVO_DE_ENTRADA}...")
df = pd.read_csv(ARQUIVO_DE_ENTRADA, low_memory=False)

# --- LIMPEZA E PREPARAÇÃO ---
print("Limpando e adaptando o dataset...")

# 1. LIMPEZA DOS NOMES DAS COLUNAS
df.columns = df.columns.str.strip()
print("Nomes das colunas limpos com sucesso.")

# 2. RENOMEAR COLUNAS
df.rename(columns={
    'text': 'conteudo',
    'Likes': 'curtidas',
    'RetweetCount': 'compartilhamentos',
    'UserID': 'user_id',
    'TweetID': 'tweet_id'
}, inplace=True)

# 3. PEGAR UMA AMOSTRA
df = df.sample(n=NUMERO_DE_TWEETS, random_state=42).reset_index(drop=True)
print(f"Usando uma amostra de {len(df)} tweets.")

# 4. GERAR COLUNAS QUE FALTAM
print("Gerando colunas fictícias e adaptando as existentes...")

# CONSERTO: Tratar valores NaN na coluna 'curtidas' antes de usá-la.
df['curtidas'] = pd.to_numeric(df['curtidas'], errors='coerce').fillna(0)

# AQUI ESTÁ A MUDANÇA PRINCIPAL: Criando a coluna de temas
df['categoria_geral'] = df['conteudo'].apply(classificar_tema)

df['nome_usuario'] = 'usuario_' + df['user_id'].astype(str)
df['comentarios'] = (df['curtidas'] * np.random.uniform(0.05, 0.2)).astype(int)
df['seguidores'] = np.random.randint(1000, 1000000, size=len(df))

# 5. CONSTRUIR A DATA DE PUBLICAÇÃO
df['ano'] = 2025
df['mes'] = 9

df['dia'] = pd.to_numeric(df['Day'], errors='coerce').fillna(1).astype(int)
df['hora'] = pd.to_numeric(df['Hour'], errors='coerce').fillna(0).astype(int)

# CONSERTO: Criar uma string de data combinada para evitar erros.
df['data_publicacao'] = pd.to_datetime(
    df['ano'].astype(str) + '-' + df['mes'].astype(str) + '-' + df['dia'].astype(str) + ' ' + df['hora'].astype(str) + ':00:00', 
    errors='coerce'
)

# 6. CRIAR A URL
df['url'] = 'https://twitter.com/' + df['nome_usuario'] + '/status/' + df['tweet_id'].astype(str)

# 7. SELECIONAR E SALVAR O ARQUIVO FINAL
colunas_finais = [
    'data_publicacao', 'nome_usuario', 'seguidores', 'conteudo', 'categoria_geral',
    'curtidas', 'comentarios', 'compartilhamentos', 'url'
]
df_final = df[colunas_finais].copy()
df_final.dropna(subset=['data_publicacao', 'conteudo'], inplace=True)

df_final.to_csv(ARQUIVO_DE_SAIDA, index=False)

print(f"\n[SUCESSO] Novo arquivo '{ARQUIVO_DE_SAIDA}' com {len(df_final)} tweets foi gerado!")
print("Agora você pode executar o 'run_etl.py' para carregar esses dados no banco.")