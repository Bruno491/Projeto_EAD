from flask import Blueprint, render_template, request, redirect, url_for, flash
from .. import db
from ..models import Usuario

bp = Blueprint("usuarios", __name__, template_folder="../templates/usuarios")

@bp.route("/")
def listar():
    usuarios = Usuario.query.order_by(Usuario.id.desc()).all()
    return render_template("usuarios/list.html", usuarios=usuarios)

@bp.route("/novo", methods=["GET", "POST"])
def criar():
    if request.method == "POST":
        u = Usuario(
            nome=request.form["nome"],
            email=request.form["email"],
            senha=request.form["senha"]
        )
        db.session.add(u)
        db.session.commit()
        flash("Usuário criado com sucesso!", "success")
        return redirect(url_for(".listar"))
    return render_template("usuarios/form.html", usuario=None)

@bp.route("/<int:id>/editar", methods=["GET", "POST"])
def editar(id):
    usuario = Usuario.query.get_or_404(id)
    if request.method == "POST":
        usuario.nome = request.form["nome"]
        usuario.email = request.form["email"]
        if request.form.get("senha"):
            usuario.senha = request.form["senha"]
        db.session.commit()
        flash("Usuário atualizado!", "success")
        return redirect(url_for(".listar"))
    return render_template("usuarios/form.html", usuario=usuario)

@bp.route("/<int:id>/excluir", methods=["GET", "POST"])
def excluir(id):
    usuario = Usuario.query.get_or_404(id)
    if request.method == "POST":
        db.session.delete(usuario)
        db.session.commit()
        flash("Usuário excluído.", "info")
        return redirect(url_for(".listar"))
    return render_template("confirm_delete.html", titulo="Excluir Usuário", item=usuario.nome, action=url_for(".excluir", id=id))