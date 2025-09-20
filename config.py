import os
from dotenv import load_dotenv

# carrega as variáveis do arquivo .env para o ambiente
load_dotenv()

# ler as variáveis de ambiente.
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")

# parâmetros do ETL
QUERY_PESQUISA = os.getenv("QUERY_PESQUISA", "#brasil")
# converter o tipo para inteiro, pq vem como string
LIMITE_POSTS = int(os.getenv("LIMITE_POSTS", 100))

# garantir que a senha foi definida no .env
BEARER_TOKEN = os.getenv("BEARER_TOKEN")
if not BEARER_TOKEN:
    raise ValueError("BEARER_TOKEN não encontrado no arquivo .env")