from flask import Flask, render_template, request, redirect, url_for, flash
import os
from dotenv import load_dotenv
from db import query_db

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "dev-secret-key")

# ──────────────────────────────────────────────
# HOME / DASHBOARD
# ──────────────────────────────────────────────
@app.route("/")
def index():
    stats = {
        "clientes":      query_db("SELECT COUNT(*) AS n FROM clientes",     one=True)["n"],
        "pets":          query_db("SELECT COUNT(*) AS n FROM pets",          one=True)["n"],
        "agendamentos":  query_db("SELECT COUNT(*) AS n FROM agendamentos WHERE status='agendado'", one=True)["n"],
        "funcionarios":  query_db("SELECT COUNT(*) AS n FROM funcionarios WHERE ativo=1", one=True)["n"],
    }
    proximos = query_db("""
        SELECT a.id, a.data_hora, a.status,
               p.nome AS pet, c.nome AS cliente,
               s.nome AS servico
        FROM agendamentos a
        JOIN pets p        ON p.id = a.pet_id
        JOIN clientes c    ON c.id = p.cliente_id
        JOIN servicos s    ON s.id = a.servico_id
        WHERE a.status = 'agendado' AND a.data_hora >= NOW()
        ORDER BY a.data_hora
        LIMIT 5
    """)
    return render_template("index.html", stats=stats, proximos=proximos)


# ──────────────────────────────────────────────
# CLIENTES
# ──────────────────────────────────────────────
@app.route("/clientes")
def clientes():
    rows = query_db("SELECT * FROM clientes ORDER BY nome")
    return render_template("clientes/index.html", clientes=rows)

@app.route("/clientes/novo", methods=["GET","POST"])
def cliente_novo():
    if request.method == "POST":
        f = request.form
        if not f["nome"] or not f["telefone"]:
            flash("Nome e telefone são obrigatórios.", "error")
            return render_template("clientes/form.html", cliente=f, action="novo")
        query_db(
            "INSERT INTO clientes (nome, cpf, telefone, email, endereco) VALUES (%s,%s,%s,%s,%s)",
            (f["nome"], f["cpf"] or None, f["telefone"], f["email"] or None, f["endereco"] or None),
            commit=True
        )
        flash("Cliente cadastrado com sucesso!", "success")
        return redirect(url_for("clientes"))
    return render_template("clientes/form.html", cliente={}, action="novo")

@app.route("/clientes/<int:id>/editar", methods=["GET","POST"])
def cliente_editar(id):
    cliente = query_db("SELECT * FROM clientes WHERE id=%s", (id,), one=True)
    if not cliente:
        flash("Cliente não encontrado.", "error")
        return redirect(url_for("clientes"))
    if request.method == "POST":
        f = request.form
        if not f["nome"] or not f["telefone"]:
            flash("Nome e telefone são obrigatórios.", "error")
            return render_template("clientes/form.html", cliente=f, action="editar", id=id)
        query_db(
            "UPDATE clientes SET nome=%s, cpf=%s, telefone=%s, email=%s, endereco=%s WHERE id=%s",
            (f["nome"], f["cpf"] or None, f["telefone"], f["email"] or None, f["endereco"] or None, id),
            commit=True
        )
        flash("Cliente atualizado!", "success")
        return redirect(url_for("clientes"))
    return render_template("clientes/form.html", cliente=cliente, action="editar", id=id)

@app.route("/clientes/<int:id>/excluir", methods=["POST"])
def cliente_excluir(id):
    query_db("DELETE FROM clientes WHERE id=%s", (id,), commit=True)
    flash("Cliente excluído.", "success")
    return redirect(url_for("clientes"))


# ──────────────────────────────────────────────
# PETS
# ──────────────────────────────────────────────
@app.route("/pets")
def pets():
    rows = query_db("""
        SELECT p.*, c.nome AS dono
        FROM pets p JOIN clientes c ON c.id = p.cliente_id
        ORDER BY p.nome
    """)
    return render_template("pets/index.html", pets=rows)

@app.route("/pets/novo", methods=["GET","POST"])
def pet_novo():
    clientes = query_db("SELECT id, nome FROM clientes ORDER BY nome")
    if request.method == "POST":
        f = request.form
        if not f["nome"] or not f["especie"] or not f["cliente_id"]:
            flash("Nome, espécie e dono são obrigatórios.", "error")
            return render_template("pets/form.html", pet=f, clientes=clientes, action="novo")
        query_db(
            "INSERT INTO pets (nome, especie, raca, idade, peso, cliente_id) VALUES (%s,%s,%s,%s,%s,%s)",
            (f["nome"], f["especie"], f["raca"] or None,
             f["idade"] or None, f["peso"] or None, f["cliente_id"]),
            commit=True
        )
        flash("Pet cadastrado com sucesso!", "success")
        return redirect(url_for("pets"))
    return render_template("pets/form.html", pet={}, clientes=clientes, action="novo")

@app.route("/pets/<int:id>/editar", methods=["GET","POST"])
def pet_editar(id):
    pet = query_db("SELECT * FROM pets WHERE id=%s", (id,), one=True)
    clientes = query_db("SELECT id, nome FROM clientes ORDER BY nome")
    if not pet:
        flash("Pet não encontrado.", "error")
        return redirect(url_for("pets"))
    if request.method == "POST":
        f = request.form
        query_db(
            "UPDATE pets SET nome=%s, especie=%s, raca=%s, idade=%s, peso=%s, cliente_id=%s WHERE id=%s",
            (f["nome"], f["especie"], f["raca"] or None,
             f["idade"] or None, f["peso"] or None, f["cliente_id"], id),
            commit=True
        )
        flash("Pet atualizado!", "success")
        return redirect(url_for("pets"))
    return render_template("pets/form.html", pet=pet, clientes=clientes, action="editar", id=id)

@app.route("/pets/<int:id>/excluir", methods=["POST"])
def pet_excluir(id):
    query_db("DELETE FROM pets WHERE id=%s", (id,), commit=True)
    flash("Pet excluído.", "success")
    return redirect(url_for("pets"))


# ──────────────────────────────────────────────
# SERVIÇOS
# ──────────────────────────────────────────────
@app.route("/servicos")
def servicos():
    rows = query_db("SELECT * FROM servicos ORDER BY nome")
    return render_template("servicos/index.html", servicos=rows)

@app.route("/servicos/novo", methods=["GET","POST"])
def servico_novo():
    if request.method == "POST":
        f = request.form
        if not f["nome"] or not f["preco"]:
            flash("Nome e preço são obrigatórios.", "error")
            return render_template("servicos/form.html", servico=f, action="novo")
        query_db(
            "INSERT INTO servicos (nome, descricao, preco, duracao_min) VALUES (%s,%s,%s,%s)",
            (f["nome"], f["descricao"] or None, f["preco"], f["duracao_min"] or 60),
            commit=True
        )
        flash("Serviço cadastrado!", "success")
        return redirect(url_for("servicos"))
    return render_template("servicos/form.html", servico={}, action="novo")

@app.route("/servicos/<int:id>/editar", methods=["GET","POST"])
def servico_editar(id):
    servico = query_db("SELECT * FROM servicos WHERE id=%s", (id,), one=True)
    if not servico:
        flash("Serviço não encontrado.", "error")
        return redirect(url_for("servicos"))
    if request.method == "POST":
        f = request.form
        query_db(
            "UPDATE servicos SET nome=%s, descricao=%s, preco=%s, duracao_min=%s, ativo=%s WHERE id=%s",
            (f["nome"], f["descricao"] or None, f["preco"], f["duracao_min"] or 60,
             1 if f.get("ativo") else 0, id),
            commit=True
        )
        flash("Serviço atualizado!", "success")
        return redirect(url_for("servicos"))
    return render_template("servicos/form.html", servico=servico, action="editar", id=id)

@app.route("/servicos/<int:id>/excluir", methods=["POST"])
def servico_excluir(id):
    query_db("DELETE FROM servicos WHERE id=%s", (id,), commit=True)
    flash("Serviço excluído.", "success")
    return redirect(url_for("servicos"))


# ──────────────────────────────────────────────
# FUNCIONÁRIOS
# ──────────────────────────────────────────────
@app.route("/funcionarios")
def funcionarios():
    rows = query_db("SELECT * FROM funcionarios ORDER BY nome")
    return render_template("funcionarios/index.html", funcionarios=rows)

@app.route("/funcionarios/novo", methods=["GET","POST"])
def funcionario_novo():
    if request.method == "POST":
        f = request.form
        if not f["nome"] or not f["cargo"]:
            flash("Nome e cargo são obrigatórios.", "error")
            return render_template("funcionarios/form.html", funcionario=f, action="novo")
        query_db(
            "INSERT INTO funcionarios (nome, cargo, telefone, email) VALUES (%s,%s,%s,%s)",
            (f["nome"], f["cargo"], f["telefone"] or None, f["email"] or None),
            commit=True
        )
        flash("Funcionário cadastrado!", "success")
        return redirect(url_for("funcionarios"))
    return render_template("funcionarios/form.html", funcionario={}, action="novo")

@app.route("/funcionarios/<int:id>/editar", methods=["GET","POST"])
def funcionario_editar(id):
    func = query_db("SELECT * FROM funcionarios WHERE id=%s", (id,), one=True)
    if not func:
        flash("Funcionário não encontrado.", "error")
        return redirect(url_for("funcionarios"))
    if request.method == "POST":
        f = request.form
        query_db(
            "UPDATE funcionarios SET nome=%s, cargo=%s, telefone=%s, email=%s, ativo=%s WHERE id=%s",
            (f["nome"], f["cargo"], f["telefone"] or None, f["email"] or None,
             1 if f.get("ativo") else 0, id),
            commit=True
        )
        flash("Funcionário atualizado!", "success")
        return redirect(url_for("funcionarios"))
    return render_template("funcionarios/form.html", funcionario=func, action="editar", id=id)

@app.route("/funcionarios/<int:id>/excluir", methods=["POST"])
def funcionario_excluir(id):
    query_db("DELETE FROM funcionarios WHERE id=%s", (id,), commit=True)
    flash("Funcionário excluído.", "success")
    return redirect(url_for("funcionarios"))


# ──────────────────────────────────────────────
# AGENDAMENTOS
# ──────────────────────────────────────────────
@app.route("/agendamentos")
def agendamentos():
    rows = query_db("""
        SELECT a.id, a.data_hora, a.status, a.observacoes,
               p.nome AS pet, c.nome AS cliente,
               s.nome AS servico, s.preco,
               f.nome AS funcionario
        FROM agendamentos a
        JOIN pets p        ON p.id = a.pet_id
        JOIN clientes c    ON c.id = p.cliente_id
        JOIN servicos s    ON s.id = a.servico_id
        LEFT JOIN funcionarios f ON f.id = a.funcionario_id
        ORDER BY a.data_hora DESC
    """)
    return render_template("agendamentos/index.html", agendamentos=rows)

@app.route("/agendamentos/novo", methods=["GET","POST"])
def agendamento_novo():
    pets        = query_db("SELECT p.id, p.nome, c.nome AS dono FROM pets p JOIN clientes c ON c.id=p.cliente_id ORDER BY p.nome")
    servicos    = query_db("SELECT id, nome, preco FROM servicos WHERE ativo=1 ORDER BY nome")
    funcionarios= query_db("SELECT id, nome FROM funcionarios WHERE ativo=1 ORDER BY nome")
    if request.method == "POST":
        f = request.form
        if not f["pet_id"] or not f["servico_id"] or not f["data_hora"]:
            flash("Pet, serviço e data/hora são obrigatórios.", "error")
            return render_template("agendamentos/form.html", pets=pets, servicos=servicos,
                                   funcionarios=funcionarios, ag=f, action="novo")
        query_db(
            """INSERT INTO agendamentos (pet_id, servico_id, funcionario_id, data_hora, observacoes)
               VALUES (%s,%s,%s,%s,%s)""",
            (f["pet_id"], f["servico_id"], f["funcionario_id"] or None,
             f["data_hora"], f["observacoes"] or None),
            commit=True
        )
        flash("Agendamento criado!", "success")
        return redirect(url_for("agendamentos"))
    return render_template("agendamentos/form.html", pets=pets, servicos=servicos,
                           funcionarios=funcionarios, ag={}, action="novo")

@app.route("/agendamentos/<int:id>/editar", methods=["GET","POST"])
def agendamento_editar(id):
    ag          = query_db("SELECT * FROM agendamentos WHERE id=%s", (id,), one=True)
    pets        = query_db("SELECT p.id, p.nome, c.nome AS dono FROM pets p JOIN clientes c ON c.id=p.cliente_id ORDER BY p.nome")
    servicos    = query_db("SELECT id, nome, preco FROM servicos WHERE ativo=1 ORDER BY nome")
    funcionarios= query_db("SELECT id, nome FROM funcionarios WHERE ativo=1 ORDER BY nome")
    if not ag:
        flash("Agendamento não encontrado.", "error")
        return redirect(url_for("agendamentos"))
    if request.method == "POST":
        f = request.form
        query_db(
            """UPDATE agendamentos
               SET pet_id=%s, servico_id=%s, funcionario_id=%s,
                   data_hora=%s, status=%s, observacoes=%s
               WHERE id=%s""",
            (f["pet_id"], f["servico_id"], f["funcionario_id"] or None,
             f["data_hora"], f["status"], f["observacoes"] or None, id),
            commit=True
        )
        flash("Agendamento atualizado!", "success")
        return redirect(url_for("agendamentos"))
    # formata data_hora para o input datetime-local
    if ag.get("data_hora"):
        ag["data_hora_fmt"] = ag["data_hora"].strftime("%Y-%m-%dT%H:%M")
    return render_template("agendamentos/form.html", pets=pets, servicos=servicos,
                           funcionarios=funcionarios, ag=ag, action="editar", id=id)

@app.route("/agendamentos/<int:id>/excluir", methods=["POST"])
def agendamento_excluir(id):
    query_db("DELETE FROM agendamentos WHERE id=%s", (id,), commit=True)
    flash("Agendamento excluído.", "success")
    return redirect(url_for("agendamentos"))

@app.route("/agendamentos/<int:id>/status", methods=["POST"])
def agendamento_status(id):
    novo_status = request.form.get("status")
    if novo_status in ("agendado","concluido","cancelado"):
        query_db("UPDATE agendamentos SET status=%s WHERE id=%s", (novo_status, id), commit=True)
        flash(f"Status alterado para '{novo_status}'.", "success")
    return redirect(url_for("agendamentos"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=False)