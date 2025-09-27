# Data Access Layer
import psycopg2 #бд
from psycopg2 import pool #для пула, логично

#если добавлять pool - то !!!СЮДА!!!
#шпора:
#Подключение к PostgreSQL — дорогая операция (TCP handshake, аутентификация, инициализация сессии).
# При высокой нагрузке (100+ запросов/сек) — сервер БД перегружается созданием/закрытием соединений.


# Глобальный пул подключений
# Минимум 1, максимум 20 подключений
connection_pool = psycopg2.pool.SimpleConnectionPool(
    1, 20,
    host='localhost',
    database='user_db',
    user='postgres',
    password='admin'
)

def get_db_connection():
    if connection_pool:
        return connection_pool.getconn()
    else:
        raise Exception("Пул подключений не инициализирован")

#ТЕПЕРЬ не закрываем con.close(), а юз эту функцию(тяяжко)
def release_db_connection(conn):
    if connection_pool:
        connection_pool.putconn(conn)