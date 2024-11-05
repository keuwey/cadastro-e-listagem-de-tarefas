from datetime import datetime

from flask import Flask, flash, redirect, render_template, request, url_for

from config import Config
from models.models import Tarefa, db

app = Flask(__name__)

app.config.from_object(Config)

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
        data_limite_str = request.form["data_limite"]
        data_limite = datetime.strptime(data_limite_str, "%Y-%m-%d").date()

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
        data_limite_str = request.form["data_limite"]
        data_limite = datetime.strptime(data_limite_str, "%Y-%m-%d").date()

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


@app.route("/reordenar/<int:tarefa_id>/<string:direcao>", methods=["POST", "PATCH"])
def reordenar(tarefa_id: int, direcao: str):
    tarefa = Tarefa.query.get_or_404(tarefa_id)
    ordem_atual = tarefa.ordem

    with db.session.no_autoflush:
        if direcao == "cima":
            tarefa_anterior = (
                Tarefa.query.filter(Tarefa.ordem < ordem_atual).order_by(Tarefa.ordem.desc()).first()
            )
            if tarefa_anterior:
                tarefa.ordem = -1
                db.session.flush()

                tarefa.ordem = tarefa_anterior.ordem
                tarefa_anterior.ordem = ordem_atual

        elif direcao == "baixo":
            tarefa_sucessora = Tarefa.query.filter(Tarefa.ordem > ordem_atual).order_by(Tarefa.ordem).first()
            if tarefa_sucessora:
                tarefa.ordem = -1
                db.session.flush()

                tarefa.ordem = tarefa_sucessora.ordem
                tarefa_sucessora.ordem = ordem_atual

    # Renumera todas as tarefas para garantir unicidade
    tarefas = Tarefa.query.order_by(Tarefa.ordem).all()
    for index, t in enumerate(tarefas):
        t.ordem = index + 1

    db.session.commit()
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=False)
