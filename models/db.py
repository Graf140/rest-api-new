# Data Access Layer
import psycopg2 #бд
from psycopg2 import pool #для пула, логично
import os
from dotenv import load_dotenv

#если добавлять pool - то !!!СЮДА!!!
#шпора:
#Подключение к PostgreSQL — дорогая операция (TCP handshake, аутентификация, инициализация сессии).
# При высокой нагрузке (100+ запросов/сек) — сервер БД перегружается созданием/закрытием соединений.

load_dotenv()

db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")
db_name = os.getenv("DB_NAME")
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")


# Глобальный пул подключений
# Минимум 1, максимум 20 подключений
connection_pool = psycopg2.pool.SimpleConnectionPool(
    1, 20,
    host=db_host,
    port=db_port,
    database=db_name,
    user=db_user,
    password=db_password
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