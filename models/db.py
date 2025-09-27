# Data Access Layer
import psycopg2 #бд
from psycopg2.extras import RealDictCursor


def get_db_connection():
    try:
        conn = psycopg2.connect(
            host='localhost',
            database='user_db',
            user='postgres',
            password='admin'
        )
        return conn
    except psycopg2.Error as e:
        print(f"Ошибка подключения к БД: {e}")
        raise