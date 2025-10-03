# Data Access Layer
import psycopg2.errors

from .db import get_db_connection, release_db_connection
from psycopg2 import DatabaseError
from psycopg2.extras import RealDictCursor
from psycopg2.errors import UniqueViolation
from exceptions import *


class UserRepository:
    @staticmethod
    def get_all_users():
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute('SELECT * FROM users')
        users = cur.fetchall()
        cur.close()
        release_db_connection(conn)
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
            release_db_connection(conn)


    @staticmethod
    def user_exists(name):
        conn = get_db_connection()
        cur = conn.cursor()
        try:
            cur.execute('SELECT * FROM users WHERE name = %s', (name,))
            return cur.fetchone() is not None #шпора: вернет True или False
        finally:
            cur.close()
            release_db_connection(conn)


    @staticmethod
    def get_user_by_id(user_id):
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute('SELECT * FROM users WHERE user_id = %s', (user_id,))
        user = cur.fetchone()
        cur.close()
        release_db_connection(conn)
        return user


    @staticmethod
    def get_user_by_name(name):
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute('SELECT * FROM users WHERE name = %s', (name,))
        user = cur.fetchone()
        cur.close()
        release_db_connection(conn)
        return user


    @staticmethod
    def create_user(name, password_hash):
        conn = get_db_connection()
        try:
            cur = conn.cursor(cursor_factory=RealDictCursor)
            cur.execute('INSERT INTO users (name, password_hash) VALUES (%s, %s)', (name, password_hash))
            conn.commit()
            return True

        except UniqueViolation: #когда добавляешь уникальное имя(если оно уже есть), то выскакивает эта ошибка
            conn.rollback()
            raise UserAlreadyExistsError(f"Пользователь с именем '{name}' уже существует")

        except DatabaseError: #не бизнес ошибка, не обрабатываем как кастомную
            conn.rollback()
            raise

        finally:
            if cur is not None:
                cur.close()
            release_db_connection(conn)