import matplotlib.pyplot as plt
import seaborn as sns

def gerar_todas_visualizacoes(df):
    """Chama todas as funções de plotagem para gerar os gráficos."""
    print("Iniciando geração dos gráficos...")
    sns.set_theme(style="whitegrid")
    df['engajamento_total'] = df['curtidas'] + df['comentarios'] + df['compartilhamentos']

    _plotar_evolucao_curtidas(df)
    _plotar_engajamento_por_tema(df)
    _plotar_top_usuarios(df)
    _plotar_heatmap_dia_semana(df)
    _plotar_seguidores_vs_engajamento(df)
    print("Gráficos gerados e salvos com sucesso.")

def _plotar_evolucao_curtidas(df):
    plt.figure(figsize=(12, 6))
    curtidas_por_mes = df.groupby(['ano', 'mes'])['curtidas'].sum().reset_index()
    curtidas_por_mes['periodo'] = curtidas_por_mes['ano'].astype(str) + '-' + curtidas_por_mes['mes'].astype(str).str.zfill(2)
    sns.lineplot(data=curtidas_por_mes, x='periodo', y='curtidas', marker='o')
    plt.title('Evolução de Curtidas ao Longo do Tempo'); plt.xlabel('Período'); plt.ylabel('Total de Curtidas'); plt.xticks(rotation=45); plt.tight_layout(); plt.savefig('1_evolucao_curtidas.png')
    plt.show()

def _plotar_engajamento_por_tema(df):
    plt.figure(figsize=(12, 7))
    eng_tema = df.groupby('categoria_geral')[['curtidas', 'comentarios', 'compartilhamentos']].sum().reset_index()
    eng_tema_melted = eng_tema.melt(id_vars='categoria_geral', var_name='tipo', value_name='total')
    sns.barplot(data=eng_tema_melted, x='categoria_geral', y='total', hue='tipo')
    plt.title('Comparação de Engajamento Total por Tema'); plt.xlabel('Categoria'); plt.ylabel('Total de Interações'); plt.tight_layout(); plt.savefig('2_engajamento_por_tema.png')
    plt.show()

def _plotar_top_usuarios(df):
    plt.figure(figsize=(12, 8))
    top_usuarios = df.groupby('nome_usuario')['engajamento_total'].sum().nlargest(10).reset_index()
    sns.barplot(data=top_usuarios, y='nome_usuario', x='engajamento_total', orient='h')
    plt.title('Top 10 Usuários por Engajamento Total'); plt.xlabel('Engajamento Total'); plt.ylabel('Usuário'); plt.tight_layout(); plt.savefig('3_top_usuarios.png')
    plt.show()

def _plotar_heatmap_dia_semana(df):
    plt.figure(figsize=(14, 7))
    dias_ordem = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    heatmap_data = df.pivot_table(values='engajamento_total', index='dia_da_semana', columns='hora', aggfunc='sum').reindex(dias_ordem)
    sns.heatmap(heatmap_data, cmap="viridis", annot=False)
    plt.title('Heatmap de Engajamento por Dia da Semana e Hora'); plt.xlabel('Hora do Dia'); plt.ylabel('Dia da Semana'); plt.tight_layout(); plt.savefig('4_heatmap_dia_semana_hora.png')
    plt.show()

def _plotar_seguidores_vs_engajamento(df):
    plt.figure(figsize=(10, 6))
    eng_autor = df.groupby(['nome_usuario', 'seguidores'])['engajamento_total'].mean().reset_index()
    sns.scatterplot(data=eng_autor, x='seguidores', y='engajamento_total', alpha=0.6)
    plt.title('Seguidores vs. Engajamento Médio'); plt.xlabel('Número de Seguidores'); plt.ylabel('Engajamento Médio por Post'); plt.xscale('log'); plt.yscale('log'); plt.tight_layout(); plt.savefig('5_seguidores_vs_engajamento.png')
    plt.show()