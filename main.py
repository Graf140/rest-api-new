from flask import Flask, jsonify
from flask import request
from flask import url_for
from flask import render_template
from flask import flash, redirect #пароли чичас

from werkzeug.security import generate_password_hash, check_password_hash #также пароли

import psycopg2 #бд
from psycopg2.extras import RealDictCursor

DB_CONFIG = {
    'host': '127.0.0.1',
    'database': 'pupok_db',
    'user': 'pupok',
    'password': 'avtobus'
}

app = Flask(__name__)
app.secret_key = "avtobus"


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


    # def get_name(self):
    #     return self.name
    #
    #
    # def get_user_id(self):
    #     return self.user_id


    def to_dict(self):
        return {
                "name": self.name,
                "user_id": self.user_id
        }


    def update_id(self, user_id):
        self.user_id = user_id


    def update_name(self, name):
        self.name = name


all_users = []

#rest-api работа
@app.route("/", methods = ['GET']) #простенькая проверка
def avtobus():
    return "Воркает"


@app.route("/api/user/", methods = ['GET']) #вернёт всех пользователей
def get_all_users():
    return jsonify([user.to_dict() for user in all_users]), 200


@app.route("/api/user/<int:user_id>/", methods = ['GET']) #гет для айдишника
def get_current_user(user_id):
    for user in all_users:
        if user.user_id == user_id:
            return jsonify(user.to_dict())
    #если до сюда дошло, формально, ничего не нашло. так шо ашЫбка
    return jsonify({"Error": "In your id code there's no user"}), 400


# @app.route("/api/user/", methods = ['POST']) #нового пользователя накидали, проверочная тема
# def put_or_reload_user():
#     data = request.get_json()
#     for user in all_users:
#         if "user_id" in data and data["user_id"] is not None:
#             if user.user_id == data["user_id"]:
#                 return jsonify({"Error": "Current id is in our data"})
#     #если дошло отсюда - всё круто, воркаем
#     tempuser = User(name=data["name"], user_id=data.get("user_id", password = generate_password_hash(12345678)))
#     all_users.append(tempuser)
#     return jsonify({"Successfull": "Your user is added",
#                     "User": tempuser.to_dict()}), 201


@app.route("/reg/", methods = ['POST'])
def reg_form_post():
    username = request.form.get('username')
    password = request.form.get('password')

    if not username or not password:
        flash("Обязательно введите имя пользователя и пароль!", "error")
        return redirect(url_for('reg_form_get'))

    hashed_password = generate_password_hash(password)
    tempuser = User(name=username, password=hashed_password)
    all_users.append(tempuser)

    flash("Регистрация успешна, теперь авторизируйтесь!", "success")
    return redirect(url_for('log_form_get'))


@app.route("/reg/", methods = ['GET'])
def reg_form_get():
    return render_template('register.html')


@app.route("/log/", methods=['GET'])
def log_form_get():
    return render_template('login.html')


@app.route("/log/", methods=['POST'])
def log_form_post():
    username = request.form.get('username')
    password = request.form.get('password')

    if not username or not password:
        flash("Пожалуйста, введите свой логин или пароль!", "error")
        return redirect(url_for('log_form_get'))

    for user in all_users:
        if user.name == username:
            if check_password_hash(user.password, password):
                flash(f"Добро пожаловать, {username}!", "success")
                return redirect(url_for('avtobus'))

    flash(f"Не правильный логин или пароль", "error")
    return redirect(url_for('log_form_get'))


if __name__ == "__main__":
    app.run(debug=True)