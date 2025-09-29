# Presentation Layer

from flask import Flask, jsonify, request, url_for, render_template, flash, redirect

from models.user import UserRepository
from services.user_service import UserService

#правка 29.09: secret key в ..env
from dotenv import load_dotenv
import os

# Загружает переменные из ..env в окружение
load_dotenv()

# Теперь можно получить секретный ключ(qwen подсказал)
secret_key = os.getenv("SECRET_KEY")

if not secret_key:
    raise ValueError("SECRET_KEY не задан в переменных окружения!")



app = Flask(__name__)
app.secret_key = secret_key



#--------------------для сайта-----------------------
@app.route("/", methods = ['GET'])
def main():
    return render_template("hub.html")


@app.route("/reg/", methods = ['GET'])
def reg_form_get():
    return render_template('register.html')


@app.route("/reg/", methods = ['POST'])
def reg_form_post():
    username = request.form.get('username')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm_password')

    if not username or not password or not confirm_password:
        flash("Логин и пароль обязательны!")
        return redirect(url_for('reg_form_get'))

    try:
        UserService.register_user(username, password, confirm_password)
        flash("Авторизация прошла успешно", 'success')
    except ValueError as err:
        flash(str(err), 'error')

#защищенная страница(только после авторизации(!!!подумать с сессиями!!!))
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

    if not username or not password:
        flash("Логин и пароль обязательны!", 'error')
        return redirect(url_for('log_form_get'))

    if UserService.login_user(username, password):
        return redirect(url_for('dashboard'))
    else:
        flash("Некорректные имя пользователя или пароль!", "error")
        return redirect(url_for('log_form_get'))
#-----------------теперь Rest API-------------------------
@app.route("/api/users/all/", methods=['GET'])
def get_all_users():
    users = UserRepository.get_all_users()
    return jsonify(users)


@app.route("/api/users/count/", methods=['GET'])
def get_user_count():
    count = UserRepository.get_users_count()
    return jsonify({"count": str(count)})


@app.route("/api/users/<username>/", methods=['GET'])
def get_user_by_username(username):
    user = UserRepository.get_user_by_name(username)
    return jsonify(user) #postman говорит, если пусто, то JSON ответ null


@app.route("/api/users/<user_id>/", methods=['GET'])
def get_user_by_id(user_id):
    user = UserRepository.get_user_by_id(user_id)
    return jsonify(user) #также как и сверху


@app.route("/api/users/exist_user/<username>/", methods=['GET'])
def exist_user_by_username(username):
    result = UserRepository.user_exists(username)
    return jsonify({result})


@app.route("/api/users/reg/", methods=['POST'])
def add_user():
    if not request.is_json:
        return jsonify({"error": "Ожидался JSON"}), 400

    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    confirm_password = data.get('confirm_password')

    if not username or not password or not confirm_password:
        return jsonify({"error": "Введите логин, пароль и подтверждение пароля!"}), 400

    try:
        success = UserService.register_user(username, password, confirm_password) #???
        if success:
            return jsonify({"success": "Регистрация прошла успешно!"})
        else:
            return jsonify({"error": "Registration failed"}), 500
    except ValueError as err:
        return jsonify({"error": str(err)})
    except Exception as e:
        return jsonify({"error": str(e)})


@app.route("/api/users/log/", methods=['POST'])
def log_user():
    if not request.is_json:
        return jsonify({"error": "Ожидался JSON"}), 400

    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"error": "Введите логин или пароль"})

    if UserService.login_user(username, password):
        return jsonify({"success": "Авторизация успешна"})
    else:
        return jsonify({"error": "Не существует пользователя с данным логином и паролем"})


@app.route("/", defaults={"path": ""})  # перенаправление всего
@app.route("/<path:path>")
def avtobus(path):
    return render_template("404.html")


if __name__ == "__main__":
    app.run(debug=True)