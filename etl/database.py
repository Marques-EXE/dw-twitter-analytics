import mysql.connector
from mysql.connector import errorcode
import config

def connect():
    """conecta ao banco de dados MySQL."""
    try:
        conn = mysql.connector.connect(
            host=config.DB_HOST,
            user=config.DB_USER,
            password=config.DB_PASSWORD,
            database=config.DB_NAME
        )
        print("Conexão com o MySQL bem-sucedida.")
        return conn
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Erro de acesso: verifique seu usuário e senha no arquivo .env.")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print(f"Banco de dados '{config.DB_NAME}' não existe.")
        else:
            print(f"Erro ao conectar ao MySQL: {err}")
        return None