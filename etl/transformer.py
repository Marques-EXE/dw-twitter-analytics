import pandas as pd
import re
from unidecode import unidecode

def transformar_dados(df):
    print("Iniciando transformação dos dados...")
    df_copy = df.copy()

    # conversões de tipo
    for col in ['curtidas', 'comentarios', 'compartilhamentos', 'seguidores']:
        df_copy[col] = pd.to_numeric(df_copy[col], errors='coerce').fillna(0).astype(int)

    def higienizar_texto(texto):
        texto = unidecode(str(texto)).upper()
        return re.sub(r'[^A-Z0-9\s#]', '', texto)

    def extrair_hashtag(texto):
        hashtags = re.findall(r'#(\w+)', texto)
        return hashtags[0] if hashtags else 'SEM_HASHTAG'

    def categorizar_tema(hashtag):
        if hashtag in ['FUTEBOL', 'COPA', 'BRASILEIRAO', 'ESPORTES']: return 'Esportes'
        if hashtag in ['POLITICA', 'ELEICOES', 'GOVERNO']: return 'Política'
        if hashtag in ['TECNOLOGIA', 'IA', 'PYTHON', 'SOFTWARE', 'TI']: return 'Tecnologia'
        return 'Geral'

    df_copy['conteudo_higienizado'] = df_copy['conteudo'].apply(higienizar_texto)
    df_copy['hashtag'] = df_copy['conteudo_higienizado'].apply(extrair_hashtag)
    df_copy['categoria_geral'] = df_copy['hashtag'].apply(categorizar_tema)

    df_copy['data_publicacao'] = pd.to_datetime(df_copy['data_publicacao'], utc=True)
    df_copy['dia'] = df_copy['data_publicacao'].dt.day
    df_copy['mes'] = df_copy['data_publicacao'].dt.month
    df_copy['ano'] = df_copy['data_publicacao'].dt.year
    df_copy['semana'] = df_copy['data_publicacao'].dt.isocalendar().week
    df_copy['dia_da_semana'] = df_copy['data_publicacao'].dt.day_name()
    df_copy['hora'] = df_copy['data_publicacao'].dt.hour
    df_copy['minuto'] = df_copy['data_publicacao'].dt.minute

    print("Transformação concluída.")
    return df_copy