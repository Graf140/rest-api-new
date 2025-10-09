# Presentation Layer

from flask import Flask
from dotenv import load_dotenv
import os
from presentation.routes.user_bp import user_bp
from presentation.routes.forum_bp import forum_bp
from presentation.error_handlers import register_error_handlers

load_dotenv()
secret_key = os.getenv("SECRET_KEY")

if not secret_key:
    raise ValueError("SECRET_KEY не задан в переменных окружения!")

app = Flask(__name__)
app.secret_key = secret_key
app.config['SECRET_KEY'] = secret_key

app.register_blueprint(user_bp)
app.register_blueprint(forum_bp)

register_error_handlers(app)

if __name__ == "__main__":
    app.run(debug=True)