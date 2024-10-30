import os

from dotenv import load_dotenv
from flask import Flask, flash, redirect, render_template, request, url_for

from models.models import Tarefa, db

app = Flask(__name__)

db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_host = os.getenv("DB_HOST")
db_name = os.getenv("DB_NAME")

app.config["SQLALCHEMY_DATABASE_URI"] = (
    "mssql+pyodbc://DB_USER:DB_PASSWORD@DB_HOST/DB_NAME?driver=ODBC+Driver+18+for+SQL+Server"
)


app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
load_dotenv()
app.secret_key = os.getenv("SECRET_KEY")  # Necessário para flash messages
db.init_app(app)

with app.app_context():
    db.create_all()


@app.route("/")
def index():
    tarefas = Tarefa.query.order_by(Tarefa.ordem).all()
    return render_template("index.html", tarefas=tarefas)


@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    if request.method == "POST":
        nome = request.form["nome"]
        custo = float(request.form["custo"])
        data_limite = request.form["data_limite"]

        # Verificar se a tarefa já existe
        if Tarefa.query.filter_by(nome=nome).first():
            flash("Uma tarefa com esse nome já existe. Tente outro.")
            return redirect(url_for("cadastro"))

        # Criar a nova tarefa
        nova_tarefa = Tarefa(nome=nome, custo=custo, data_limite=data_limite)
        # Define a ordem como o último número atual + 1
        nova_tarefa.ordem = Tarefa.query.count() + 1
        db.session.add(nova_tarefa)
        db.session.commit()
        return redirect(url_for("index"))

    return render_template("cadastro.html")


@app.route("/editar/<int:tarefa_id>", methods=["GET", "POST"])
def editar_tarefa(tarefa_id: int):
    tarefa = Tarefa.query.get_or_404(tarefa_id)

    if request.method == "POST":
        nome = request.form["nome"]
        custo = float(request.form["custo"])
        data_limite = request.form["data_limite"]

        # Verificar se o novo nome já existe
        if tarefa.nome != nome and Tarefa.query.filter_by(nome=nome).first():
            flash("Uma tarefa com esse nome já existe. Tente outro.")
            return redirect(url_for("editar_tarefa", tarefa_id=tarefa_id))

        # Atualizar a tarefa
        tarefa.nome = nome
        tarefa.custo = custo
        tarefa.data_limite = data_limite
        db.session.commit()
        return redirect(url_for("index"))

    return render_template("editar.html", tarefa=tarefa)


@app.route("/excluir/<int:tarefa_id>", methods=["POST"])
def excluir_tarefa(tarefa_id: int):
    tarefa = Tarefa.query.get_or_404(tarefa_id)
    db.session.delete(tarefa)
    db.session.commit()
    return redirect(url_for("index"))


@app.route("/reordenar/<int:tarefa_id>/<string:direcao>")
def reordenar(tarefa_id: int, direcao: str):
    tarefa = Tarefa.query.get_or_404(tarefa_id)
    if direcao == "cima" and tarefa.ordem > 1:
        tarefa_anterior = Tarefa.query.filter_by(ordem=tarefa.ordem - 1).first()
        tarefa_anterior.ordem += 1
        tarefa.ordem -= 1
    elif direcao == "baixo":
        tarefa_proxima = Tarefa.query.filter_by(ordem=tarefa.ordem + 1).first()
        if tarefa_proxima:
            tarefa_proxima.ordem -= 1
            tarefa.ordem += 1

    db.session.commit()
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
