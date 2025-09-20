import pandas as pd

def carregar_dados(conn, df):
    print("Iniciando processo de carga no Data Warehouse (MySQL)...")
    cursor = conn.cursor()

    # padroniza a coluna de data para ser um objeto datetime sem fuso horário, tava dando muito b.o....
    df['data_publicacao'] = pd.to_datetime(df['data_publicacao'], errors='coerce').dt.tz_convert('UTC').dt.tz_localize(None)

    # carga das dimenssões
    print("Carregando Dimensão Autor...")
    dim_autor = df[['nome_usuario', 'seguidores']].drop_duplicates(subset=['nome_usuario'])
    for _, row in dim_autor.iterrows():
        cursor.execute("INSERT IGNORE INTO Dim_Autor (nome_usuario, seguidores) VALUES (%s, %s)",
                       (row['nome_usuario'], row['seguidores']))

    print("Carregando Dimensão Tema...")
    dim_tema = df[['hashtag', 'categoria_geral']].drop_duplicates(subset=['hashtag'])
    for _, row in dim_tema.iterrows():
        cursor.execute("INSERT IGNORE INTO Dim_Tema (hashtag, categoria_geral) VALUES (%s, %s)",
                       (row['hashtag'], row['categoria_geral']))

    print("Carregando Dimensão Tempo...")
    dim_tempo = df[['data_publicacao', 'dia', 'mes', 'ano', 'semana', 'dia_da_semana', 'hora', 'minuto']].drop_duplicates(subset=['data_publicacao'])
    for _, row in dim_tempo.iterrows():
        cursor.execute("""
            INSERT IGNORE INTO Dim_Tempo (data_completa, dia, mes, ano, semana, dia_da_semana, hora, minuto)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, tuple(row))
    
    conn.commit()
    print("Dimensões carregadas com sucesso.")

    # preparação da tabela "FATO"
    dim_autor_map = pd.read_sql("SELECT sk_autor, nome_usuario FROM Dim_Autor", conn)
    dim_tema_map = pd.read_sql("SELECT sk_tema, hashtag FROM Dim_Tema", conn)
    dim_tempo_map = pd.read_sql("SELECT sk_tempo, data_completa FROM Dim_Tempo", conn)
    
    dim_tempo_map['data_completa'] = pd.to_datetime(dim_tempo_map['data_completa'])

    df = pd.merge(df, dim_autor_map, on='nome_usuario', how='left')
    df = pd.merge(df, dim_tema_map, on='hashtag', how='left')
    df = pd.merge(df, dim_tempo_map, left_on='data_publicacao', right_on='data_completa', how='left')

    # carga da tabela "FATO"
    df.rename(columns={'sk_autor': 'fk_autor', 'sk_tema': 'fk_tema', 'sk_tempo': 'fk_tempo'}, inplace=True)
    df.dropna(subset=['fk_autor', 'fk_tema', 'fk_tempo'], inplace=True)
    
    if len(df) == 0:
        print("\n[DIAGNÓSTICO] O DataFrame ficou vazio. Nenhuma linha será inserida.")
        cursor.close()
        return

    df[['fk_autor', 'fk_tema', 'fk_tempo']] = df[['fk_autor', 'fk_tema', 'fk_tempo']].astype(int)

    print(f"Carregando {len(df)} linhas na Tabela Fato...")
    for _, row in df.iterrows():
        cursor.execute("""
            INSERT IGNORE INTO Fato_EngajamentoPosts (fk_tempo, fk_autor, fk_tema, curtidas, comentarios, compartilhamentos, url_post)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (row['fk_tempo'], row['fk_autor'], row['fk_tema'], row['curtidas'], row['comentarios'], row['compartilhamentos'], row['url']))
    
    conn.commit()
    cursor.close()
    print(f"\n{len(df)} LINHAS INSERIDAS NA TABELA FATO. PROCESSO CONCLUÍDO COM SUCESSO!")