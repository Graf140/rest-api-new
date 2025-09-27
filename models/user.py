# Data Access Layer

from .db import get_db_connection
import psycopg2 #бд
from psycopg2.extras import RealDictCursor


class UserRepository:
    @staticmethod
    def get_all_users():
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute('SELECT * FROM users')
        users = cur.fetchall()
        cur.close()
        conn.close()
        return users


    @staticmethod
    def get_users_count():
        conn = get_db_connection()
        cur = conn.cursor()
        try:
            cur.execute('SELECT COUNT(*) FROM users')
            count = cur.fetchone()[0]
            return count
        finally:
            cur.close()
            conn.close()


    @staticmethod
    def user_exists(name):
        conn = get_db_connection()
        cur = conn.cursor()
        try:
            cur.execute('SELECT * FROM users WHERE name = %s', (name,))
            return cur.fetchone() is not None
        finally:
            cur.close()
            conn.close()


    @staticmethod
    def get_user_by_id(user_id):
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute('SELECT * FROM users WHERE user_id = %s', (user_id,))
        user = cur.fetchone()
        cur.close()
        conn.close()
        return user


    @staticmethod
    def get_user_by_name(name):
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute('SELECT * FROM users WHERE name = %s', (name,))
        user = cur.fetchone()
        cur.close()
        conn.close()
        return user


    @staticmethod
    def add_user(name, password_hash):
        conn = get_db_connection()
        try:
            cur = conn.cursor(cursor_factory=RealDictCursor)
            cur.execute('SELECT 1 FROM users WHERE name = %s', (name,))
            if cur.fetchone():
                print(f"Ошибка: пользователь с именем '{name}' уже существует.")
                return ("False users")
            cur.execute('INSERT INTO users (name, password_hash) VALUES (%s, %s)', (name, password_hash))
            conn.commit()
            return ("True")

        except Exception as e:
            # Любая ошибка
            conn.rollback()
            print(f"Неожиданная ошибка при добавлении пользователя: {e}")
            return ("False")

        finally:
            cur.close()
            conn.close()