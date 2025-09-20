import tweepy
import pandas as pd
import config

def extrair_dados_twitter(query, limit):
    """
    coleta posts do Twitter/X usando a API v2 com Tweepy.

    """
    print(f"Iniciando coleta de até {limit} posts com Tweepy...")
    
    # autenticação com o Bearer Token (API do X)
    client = tweepy.Client(bearer_token=config.BEARER_TOKEN)

    """
    realiza a busca
    'expansions' inclui os dados do autor no resultado
    'tweet.fields' pede métricas públicas (likes, retweets, etc)
    'user.fields' pede o número de seguidores do autor

    """
    response = client.search_recent_tweets(
        query=query,
        max_results=limit,
        expansions=['author_id'],
        tweet_fields=['public_metrics', 'created_at'],
        user_fields=['public_metrics']
    )

    # a API pode não retornar nada
    if not response.data:
        print("Nenhum post encontrado para a query.")
        return pd.DataFrame()

    # processa a resposta da API
    tweets_data = response.data
    users_data = {user["id"]: user for user in response.includes['users']}
    
    posts = []
    for tweet in tweets_data:
        author_info = users_data[tweet.author_id]
        posts.append([
            tweet.created_at,
            author_info.username,
            author_info.public_metrics['followers_count'],
            tweet.text,
            tweet.public_metrics['like_count'],
            tweet.public_metrics['reply_count'],
            tweet.public_metrics['retweet_count'],
            f"https://twitter.com/{author_info.username}/status/{tweet.id}"
        ])

    df = pd.DataFrame(posts, columns=[
        'data_publicacao', 'nome_usuario', 'seguidores',
        'conteudo', 'curtidas', 'comentarios', 'compartilhamentos', 'url'
    ])
    
    print(f"{len(df)} posts coletados com sucesso via API.")
    return df