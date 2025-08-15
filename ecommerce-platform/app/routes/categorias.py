from flask import Blueprint, render_template, request, redirect, url_for, flash
from .. import db
from ..models import Categoria

bp = Blueprint("categorias", __name__, template_folder="../templates/categorias")

@bp.route("/")
def listar():
    categorias = Categoria.query.order_by(Categoria.nome.asc()).all()
    return render_template("categorias/list.html", categorias=categorias)

@bp.route("/novo", methods=["GET", "POST"])
def criar():
    if request.method == "POST":
        c = Categoria(nome=request.form["nome"])
        db.session.add(c)
        db.session.commit()
        flash("Categoria criada!", "success")
        return redirect(url_for(".listar"))
    return render_template("categorias/form.html", categoria=None)

@bp.route("/<int:id>/editar", methods=["GET", "POST"])
def editar(id):
    categoria = Categoria.query.get_or_404(id)
    if request.method == "POST":
        categoria.nome = request.form["nome"]
        db.session.commit()
        flash("Categoria atualizada!", "success")
        return redirect(url_for(".listar"))
    return render_template("categorias/form.html", categoria=categoria)

@bp.route("/<int:id>/excluir", methods=["GET", "POST"])
def excluir(id):
    categoria = Categoria.query.get_or_404(id)
    if request.method == "POST":
        db.session.delete(categoria)
        db.session.commit()
        flash("Categoria excluída.", "info")
        return redirect(url_for(".listar"))
    return render_template("confirm_delete.html", titulo="Excluir Categoria", item=categoria.nome, action=url_for(".excluir", id=id))