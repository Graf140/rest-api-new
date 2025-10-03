# presentation АшЫбки
from flask import jsonify
from exceptions import *


def register_error_handlers(app):
    @app.errorhandler(ValueError)
    def handle_value_error(e):
        return jsonify({"error": str(e)}), 400

    @app.errorhandler(PustoyLoginParolError)
    def handle_pustoy_login_parol_error(e):
        return jsonify({"error": str(e)}), 400

    @app.errorhandler(UserAlreadyExistsError)
    def handle_user_already_exists(e):
        return jsonify({"error": str(e)}), 409

    @app.errorhandler(InvalidPasswordError)
    def handle_invalid_password_error(e):
        return jsonify({"error": str(e)}), 400

    @app.errorhandler(UserNotFoundError)
    def handle_user_not_found(e):
        return jsonify({"error": str(e)}), 404 #404 - это not found

    @app.errorhandler(ValidationError)
    def handle_validation_error(e):
        return jsonify({"error": str(e)}), 400


    # Обработка всех остальных ошибок
    @app.errorhandler(Exception)
    def handle_exception(e):
        app.logger.error("необработанное исключение", exc_info=True)

        return jsonify({"error": "Произошла внутренняя ошибка"}), 500