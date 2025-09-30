# Presentation Layer

from flask import Flask
from dotenv import load_dotenv
import os
from presentation.routes import register_routes
from presentation.error_handlers import register_error_handlers

load_dotenv()
secret_key = os.getenv("SECRET_KEY")

if not secret_key:
    raise ValueError("SECRET_KEY не задан в переменных окружения!")

app = Flask(__name__)
app.secret_key = secret_key

register_routes(app)
register_error_handlers(app)

if __name__ == "__main__":
    app.run(debug=True)