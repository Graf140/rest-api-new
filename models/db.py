# Data Access Layer
import psycopg2 #бд
from psycopg2 import pool #для пула, логично

#правка от 30.09 обеденная
from config.database import DatabaseConfig


connection_pool = psycopg2.pool.SimpleConnectionPool(
    1, 20,
    **DatabaseConfig.get_connection_parametres() #** для распаковки словаря
)


def get_db_connection():
    if connection_pool:
        return connection_pool.getconn()
    else:
        raise Exception("Пул подключений не инициализирован")


def release_db_connection(conn):
    if connection_pool:
        connection_pool.putconn(conn)