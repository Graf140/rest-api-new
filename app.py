# Presentation Layer

from flask import Flask, jsonify, request, url_for, render_template, flash, redirect
from services.user_service import UserService

app = Flask(__name__)
app.secret_key = "avtobus"


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

    if UserService.login_user(username, password):
        return redirect(url_for('dashboard'))
    else:
        flash("Incorrect username or password", "error")
        return redirect(url_for('log_form_get'))


@app.route("/", defaults={"path": ""})  # перенаправление всего
@app.route("/<path:path>")
def avtobus(path):
    return render_template("404.html")


if __name__ == "__main__":
    app.run(debug=True)