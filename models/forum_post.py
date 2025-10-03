#форум пост, !!работаем с другой дб!!!

from .db import get_db_connection, release_db_connection
from psycopg2 import DatabaseError
from psycopg2.extras import RealDictCursor
from psycopg2.errors import UniqueViolation
from exceptions import *

class ForumPost:
    @staticmethod
    def create_post(user_id, title, content):
        conn = get_db_connection()
        try:
            cur = conn.cursor(cursor_factory=RealDictCursor)
            cur.execute('INSERT INTO forum_posts (user_id, title, content) VALUES (%s, %s, %s) RETURNING post_id, created_at', (user_id, title, content))
            post = cur.fetchone()
            conn.commit()
            return post
        finally:
            if cur is not None:
                cur.close()
            release_db_connection(conn)

    @staticmethod
    def get_all_posts():
        conn = get_db_connection()
        try:
            cur = conn.cursor(cursor_factory=RealDictCursor)
            cur.execute('SELECT * FROM forum_posts ORDER BY created_at DESC')
            data = cur.fetchall()
            return data
        finally:
            if cur is not None:
                cur.close()
            release_db_connection(conn)

    @staticmethod
    def get_post_by_id(post_id):
        conn = get_db_connection()
        try:
            cur = conn.cursor(cursor_factory=RealDictCursor)
            cur.execute('SELECT * FROM forum_posts WHERE post_id = %s', (post_id))
            data = cur.fetchone()
            return data
        finally:
            if cur is not None:
                cur.close()
            release_db_connection(conn)

    @staticmethod
    def get_post_by_username(username):
        conn = get_db_connection();
        try:
            cur = conn.cursor(cursor_factory=RealDictCursor)
            cur.execute('SELECT * FROM forum_posts WHERE username = %s', (username))
            data = cur.fetchone()
            return data
        finally:
            if cur is not None:
                cur.close()
            release_db_connection(conn)