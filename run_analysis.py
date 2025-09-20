""" objetivo: plotar o gráfico da análise feita"""
from etl import database
from analysis import visualizer
import pandas as pd

def main():
    print("INICIANDO PROCESSO DE ANÁLISE E BI (LENDO DO BANCO DE DADOS)")
    conn = database.connect()
    if not conn:
        return
    try:
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
        df_analise = pd.read_sql(query, conn)
        if df_analise.empty:
            print("Não há dados no Data Warehouse para analisar.")
            return
        visualizer.gerar_todas_visualizacoes(df_analise)
    finally:
        conn.close()

if __name__ == "__main__":
    main()