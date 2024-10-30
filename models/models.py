# models/models.py
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Tarefa(db.Model):
    __tablename__ = "tarefas"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), unique=True, nullable=False)
    custo = db.Column(db.Float, nullable=False)
    data_limite = db.Column(db.Date, nullable=False)
    ordem = db.Column(db.Integer, unique=True, nullable=False)

    def __repr__(self) -> str:
        return f"<Tarefa {self.nome}>"
