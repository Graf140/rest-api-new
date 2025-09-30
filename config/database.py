#config in database, пупупу...

import os
from dotenv import load_dotenv

load_dotenv()


class DatabaseConfig:
    db_name = os.getenv("DB_NAME")
    db_user = os.getenv("DB_USER")
    db_password = os.getenv("DB_PASSWORD")
    db_host = os.getenv("DB_HOST")
    db_port = os.getenv("DB_PORT")

    @classmethod #с cls рекомендовал Qwen, я все равно не знаю почему лучше именно так, почему нельзя задать жестко(!!!спросить!!!)
    def get_connection_parametres(cls):
        return {
            "host": cls.db_host,
            "port": cls.db_port,
            "database": cls.db_name,
            "user": cls.db_user,
            "password": cls.db_password
        }