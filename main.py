from flask import Flask, jsonify
from flask import request
from flask import url_for
from flask import render_template
from flask import flash, redirect #пароли чичас

from werkzeug.security import generate_password_hash, check_password_hash #также пароли

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


app = Flask(__name__)
app.secret_key = "avtobus"

#жоский класс с импортированной бд(чутка воркинга)
class User:
    quantity = 1


    def __init__(self, password=None, name=None, user_id = 0):
        self.name = name
        self.password = password
        if user_id == 0:
            self.user_id = User.quantity
        else:
            self.user_id = user_id
        User.quantity += 1


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
    def get_user_by_id(user_id):
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute('SELECT * FROM users WHERE user_id = %s', (user_id,))
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



    @staticmethod
    def check_user(name, password): #ОБЯЗАТЕЛЬНО пароль, а не кеш
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute('SELECT * FROM users WHERE name = %s', (name,))
        user = cur.fetchone()
        cur.close()
        conn.close()
        if user and check_password_hash(user['password_hash'], password):
            return True
        return False


#rest-api работа


# @app.route("/api/user/", methods = ['GET']) #вернёт всех пользователей
# def get_all_users():
#     all_users = User.get_all_users()
#     return jsonify([user for user in all_users]), 200


@app.route("/", methods = ['GET'])
def main():
    return render_template("hub.html")

@app.route("/reg/", methods = ['POST'])
def reg_form_post():
    username = request.form.get('username')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm_password')

    if not username or not password:
        flash("Обязательно введите имя пользователя и пароль!", "error")
        return redirect(url_for('reg_form_get'))

    if password != confirm_password:
        flash("Ваши пароли не совпадают!", "error")
        return redirect(url_for('reg_form_get'))

    hashed_password = generate_password_hash(password)
    #all_users.append(tempuser) #было до ДБ, сейчас с бд
    result = User.add_user(username, hashed_password)
    if result == "True":
        flash("Регистрация успешна, теперь авторизируйтесь!", "success")
        return redirect(url_for('log_form_get'))
    elif result == "False users":
        flash("Ошибка при регистрации. Введенное имя пользователя уже существует", "error")
        return redirect(url_for('reg_form_get'))
    else:
        flash("Ошибка при регистрации. Пользователь не добавлен.", "error")
        return redirect(url_for('reg_form_get'))


@app.route("/reg/", methods = ['GET'])
def reg_form_get():
    return render_template('register.html')


@app.route("/dashboard/")
def dashboard():
    return render_template("rickroll.html")


@app.route("/log/", methods=['GET'])
def log_form_get():
    return render_template('login.html')


@app.route("/log/", methods=['POST'])
def log_form_post():
    username = request.form.get('username')
    password = request.form.get('password')

    if User.check_user(username, password):
        flash("Успех, авторизация прошла успешно", "success")
        return redirect(url_for('dashboard'))
    else:
        flash("Ошибка: логин или пароль не верны", "error")
        return redirect(url_for('log_form_get'))


    #после логирования на rick-roll(vibe-codding)


#ОБЯЗАТЕЛЬНО ПОСЛЕДНИЙ
@app.route("/", defaults={"path": ""})  # перенаправление всего
@app.route("/<path:path>")
def avtobus(path):
    return render_template("404.html")


if __name__ == "__main__":
    app.run(debug=True)

    #просто технический код для моего удобства при переносе с устройства на устройство(не удобно базы данных переносить(((()
# CREATE TABLE public.users (
#     user_id SERIAL PRIMARY KEY,
#     name TEXT NOT NULL UNIQUE,
#     password_hash TEXT NOT NULL
# );