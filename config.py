import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "minha_chave_secreta")
    SQLALCHEMY_DATABASE_URI = "sqlite:///tarefas.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
