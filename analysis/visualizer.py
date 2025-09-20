# analysis/visualizer.py (VERSÃO MELHORADA COM ANOTAÇÕES)
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def gerar_todas_visualizacoes(df):
    """Chama todas as funções de plotagem para gerar os gráficos aprimorados."""
    print("Iniciando geração dos gráficos aprimorados...")
    sns.set_theme(style="whitegrid")

    # Garante que as colunas de engajamento são numéricas
    for col in ['curtidas', 'comentarios', 'compartilhamentos']:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

    df['engajamento_total'] = df['curtidas'] + df['comentarios'] + df['compartilhamentos']

    # Chamando as novas versões das funções de plotagem
    plotar_evolucao_engajamento_tempo(df)
    plotar_engajamento_por_tema(df)
    plotar_top_usuarios_empilhado(df)
    plotar_heatmap_dia_semana(df)
    plotar_seguidores_vs_engajamento(df)
    
    print("\n[SUCESSO] Gráficos aprimorados gerados e salvos com sucesso.")

def plotar_evolucao_engajamento_tempo(df):
    """
    Gráfico de linha APRIMORADO: Evolução de TODAS as métricas de engajamento ao longo do tempo.
    """
    print("Gerando Gráfico 1: Evolução do Engajamento no Tempo (3 Métricas)...")
    
    # Prepara os dados agrupando por mês
    engajamento_por_mes = df.groupby(['ano', 'mes'])[['curtidas', 'comentarios', 'compartilhamentos']].sum().reset_index()
    engajamento_por_mes['periodo'] = engajamento_por_mes['ano'].astype(str) + '-' + engajamento_por_mes['mes'].astype(str).str.zfill(2)
    
    # Usa o 'melt' para transformar as colunas de métricas em linhas, ideal para o Seaborn
    engajamento_melted = engajamento_por_mes.melt(id_vars='periodo', var_name='metrica', value_name='total')
    
    plt.figure(figsize=(14, 7))
    sns.lineplot(data=engajamento_melted, x='periodo', y='total', hue='metrica', marker='o', palette='viridis')
    plt.title('Evolução do Engajamento no Tempo', fontsize=16)
    plt.xlabel('Período (Ano-Mês)', fontsize=12)
    plt.ylabel('Total de Interações', fontsize=12)
    plt.xticks(rotation=45)
    plt.legend(title='Métrica de Engajamento')
    plt.tight_layout()
    plt.savefig('1_evolucao_engajamento_tempo.png')
    plt.show()
    print("---")
    print("Interpretação do Gráfico 1:")
    print("Este gráfico de linha mostra como as curtidas, comentários e compartilhamentos se comportam ao longo do tempo. Ele ajuda a identificar tendências, como picos de engajamento em meses específicos ou se um tipo de interação (ex: curtidas) está crescendo mais rápido que outro.")
    print("---")

def plotar_engajamento_por_tema(df):
    """
    Gráfico de barras APRIMORADO para temas: usa barras horizontais empilhadas
    para mostrar o total de engajamento e a contribuição de cada métrica.
    """
    print("\nGerando Gráfico 2: Engajamento por Tema (Detalhado)...")
    
    # 1. Agrupa por tema e soma as métricas de engajamento
    engajamento_tema = df.groupby('categoria_geral')[['curtidas', 'comentarios', 'compartilhamentos']].sum()
    
    # 2. VERIFICAÇÃO IMPORTANTE: Se o DataFrame de temas tiver menos de duas linhas,
    # significa que a amostra tem apenas um ou nenhum tema para comparar.
    if len(engajamento_tema) <= 1:
        print("\nAVISO: Não foi possível gerar o gráfico de temas.")
        print("Motivo: A amostra de tweets contém apenas um tema. Para gerar o gráfico,")
        print("é necessário ter pelo menos dois temas diferentes para comparar.")
        print("Tente aumentar o número de tweets na amostra no arquivo 'prepare_dataset.py' ou")
        print("verifique se o seu dataset original possui conteúdo de múltiplos temas.")
        print("Contagem de temas encontrados:")
        print(df['categoria_geral'].value_counts())
        return # Sai da função para evitar o erro

    # 3. Ordena os temas com base no engajamento total para uma melhor visualização
    engajamento_tema['total'] = engajamento_tema.sum(axis=1)
    engajamento_tema = engajamento_tema.sort_values('total', ascending=True)
    engajamento_tema.drop('total', axis=1, inplace=True)
    
    plt.figure(figsize=(12, 8))
    # Cria o gráfico de barras horizontais empilhadas
    engajamento_tema.plot(kind='barh', stacked=True, figsize=(12, 8), colormap='plasma')
    
    plt.title('Composição do Engajamento por Tema', fontsize=16)
    plt.xlabel('Total de Interações', fontsize=12)
    plt.ylabel('Tema', fontsize=12)
    plt.legend(title='Métrica', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout(rect=[0, 0, 0.9, 1])
    
    plt.savefig('2_engajamento_por_tema.png')
    plt.show()
    print("---")
    print("Interpretação do Gráfico 2:")
    print("Este gráfico de barras empilhadas é ideal para comparar os temas. A barra completa de cada tema representa seu engajamento total. As diferentes cores dentro da barra mostram a contribuição de curtidas, comentários e compartilhamentos. Isso permite ver rapidamente qual tema é mais popular e como o público interage com ele (ex: um tema pode ter muitas curtidas e outro muitos compartilhamentos).")
    print("---")

def plotar_top_usuarios_empilhado(df):
    """
    Gráfico de barras horizontais APRIMORADO: Ranking dos usuários com barras empilhadas
    mostrando a composição do engajamento.
    """
    print("\nGerando Gráfico 3: Top 10 Usuários por Engajamento (Detalhado)...")
    
    top_10_usuarios_nomes = df.groupby('nome_usuario')['engajamento_total'].sum().nlargest(10).index
    df_top_10 = df[df['nome_usuario'].isin(top_10_usuarios_nomes)]
    engajamento_detalhado = df_top_10.groupby('nome_usuario')[['curtidas', 'comentarios', 'compartilhamentos']].sum()
    engajamento_detalhado['total'] = engajamento_detalhado.sum(axis=1)
    engajamento_detalhado = engajamento_detalhado.sort_values(by='total', ascending=True)
    engajamento_detalhado.drop(columns='total', inplace=True)
    
    engajamento_detalhado.plot(kind='barh', stacked=True, figsize=(12, 8), colormap='cividis')
    plt.title('Top 10 Usuários e a Composição do Seu Engajamento', fontsize=16)
    plt.xlabel('Engajamento Total', fontsize=12)
    plt.ylabel('Nome do Usuário', fontsize=12)
    plt.legend(title='Tipo de Engajamento')
    plt.tight_layout()
    plt.savefig('3_top_usuarios_detalhado.png')
    plt.show()
    print("---")
    print("Interpretação do Gráfico 3:")
    print("Este gráfico mostra os perfis mais influentes em termos de engajamento total. As cores nas barras revelam se o engajamento de um usuário vem mais de curtidas, comentários ou compartilhamentos. Isso é essencial para entender a estratégia de conteúdo de cada um.")
    print("---")


def plotar_heatmap_dia_semana(df):
    """Heatmap: Distribuição de engajamento por dia da semana e hora."""
    print("\nGerando Gráfico 4: Engajamento por Dia da Semana e Hora...")
    dias_ordem = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    dias_pt = ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado', 'Domingo']
    df['dia_da_semana_pt'] = pd.Categorical(df['dia_da_semana'].replace(dict(zip(dias_ordem, dias_pt))), categories=dias_pt, ordered=True)
    
    heatmap_data = df.pivot_table(values='engajamento_total', index='dia_da_semana_pt', columns='hora', aggfunc='sum')
    
    plt.figure(figsize=(16, 8))
    sns.heatmap(heatmap_data, cmap="YlGnBu", annot=True, fmt=".0f", linewidths=.5) # Adicionei 'annot=True' e 'fmt' para ver os valores
    plt.title('Mapa de Calor do Engajamento por Dia da Semana e Hora', fontsize=16)
    plt.xlabel('Hora do Dia', fontsize=12)
    plt.ylabel('Dia da Semana', fontsize=12)
    plt.tight_layout()
    plt.savefig('4_heatmap_dia_semana_hora.png')
    plt.show()
    print("---")
    print("Interpretação do Gráfico 4:")
    print("O mapa de calor revela os melhores horários para postar. As células mais escuras indicam os períodos de maior engajamento. Por exemplo, se a célula 'Quinta-feira' e '17h' estiver escura, esse é um momento ideal para publicar um tweet.")
    print("---")

def plotar_seguidores_vs_engajamento(df):
    """Scatter plot: Relação entre número de seguidores e engajamento médio por post."""
    print("\nGerando Gráfico 5: Seguidores vs. Engajamento Médio por Post...")
    engajamento_autor = df.groupby(['nome_usuario', 'seguidores'])['engajamento_total'].mean().reset_index()
    
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=engajamento_autor, x='seguidores', y='engajamento_total', alpha=0.6, size='engajamento_total', sizes=(20, 500))
    plt.title('Relação entre Seguidores e Engajamento Médio', fontsize=16)
    plt.xlabel('Número de Seguidores', fontsize=12)
    plt.ylabel('Engajamento Médio por Post', fontsize=12)
    plt.xscale('log')
    plt.yscale('log')
    plt.tight_layout()
    plt.savefig('5_seguidores_vs_engajamento.png')
    plt.show()
    print("---")
    print("Interpretação do Gráfico 5:")
    print("Este gráfico de dispersão com escala logarítmica mostra se o número de seguidores influencia o engajamento. Ele ajuda a identificar 'influenciadores de nicho' (usuários com menos seguidores mas alto engajamento) e perfis que têm muitos seguidores, mas baixo engajamento médio.")
    print("---")