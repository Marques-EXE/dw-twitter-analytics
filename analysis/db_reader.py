import pandas as pd

def ler_dados_completos_dw(conn):
    print("Lendo dados do Data Warehouse para análise...")
    query = """
    SELECT
        f.curtidas, f.comentarios, f.compartilhamentos,
        d_t.ano, d_t.mes, d_t.dia_da_semana, d_t.hora,
        d_a.nome_usuario, d_a.seguidores,
        d_th.categoria_geral
    FROM Fato_EngajamentoPosts f
    JOIN Dim_Tempo d_t ON f.fk_tempo = d_t.sk_tempo
    JOIN Dim_Autor d_a ON f.fk_autor = d_a.sk_autor
    JOIN Dim_Tema d_th ON f.fk_tema = d_th.sk_tema;
    """
    return pd.read_sql(query, conn)