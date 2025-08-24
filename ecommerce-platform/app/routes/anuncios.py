from flask import Blueprint, render_template, request, redirect, url_for, flash
from .. import db
from ..models import Anuncio, Usuario, Categoria
from flask_login import login_required

bp = Blueprint("anuncios", __name__, template_folder="../templates/anuncios")

@bp.route("/")
def listar():
    anuncios = Anuncio.query.order_by(Anuncio.id.desc()).all()
    return render_template("anuncios/list.html", anuncios=anuncios)

@bp.route("/novo", methods=["GET", "POST"])
@login_required
def criar():
    usuarios = Usuario.query.all()
    categorias = Categoria.query.all()
    if request.method == "POST":
        a = Anuncio(
            titulo=request.form["titulo"],
            descricao=request.form["descricao"],
            preco=request.form["preco"],
            usuario_id=request.form["usuario_id"],
            categoria_id=request.form["categoria_id"],
        )
        db.session.add(a)
        db.session.commit()
        flash("Anúncio criado!", "success")
        return redirect(url_for(".listar"))
    return render_template("anuncios/form.html", anuncio=None, usuarios=usuarios, categorias=categorias)

@bp.route("/<int:id>/editar", methods=["GET", "POST"])
@login_required
def editar(id):
    anuncio = Anuncio.query.get_or_404(id)
    usuarios = Usuario.query.all()
    categorias = Categoria.query.all()
    if request.method == "POST":
        anuncio.titulo = request.form["titulo"]
        anuncio.descricao = request.form["descricao"]
        anuncio.preco = request.form["preco"]
        anuncio.usuario_id = request.form["usuario_id"]
        anuncio.categoria_id = request.form["categoria_id"]
        db.session.commit()
        flash("Anúncio atualizado!", "success")
        return redirect(url_for(".listar"))
    return render_template("anuncios/form.html", anuncio=anuncio, usuarios=usuarios, categorias=categorias)

@bp.route("/<int:id>/excluir", methods=["GET", "POST"])
@login_required
def excluir(id):
    anuncio = Anuncio.query.get_or_404(id)
    if request.method == "POST":
        db.session.delete(anuncio)
        db.session.commit()
        flash("Anúncio excluído.", "info")
        return redirect(url_for(".listar"))
    return render_template("confirm_delete.html", titulo="Excluir Anúncio", item=anuncio.titulo, action=url_for(".excluir", id=id))