from flask import Blueprint, render_template, request, redirect, url_for, flash
from .. import db
from ..models import Favorito, Usuario, Anuncio

bp = Blueprint("favoritos", __name__, template_folder="../templates/favoritos")

@bp.route("/")
def listar():
    favoritos = Favorito.query.order_by(Favorito.id.desc()).all()
    return render_template("favoritos/list.html", favoritos=favoritos)

@bp.route("/novo", methods=["GET", "POST"])
def criar():
    usuarios = Usuario.query.all()
    anuncios = Anuncio.query.all()
    if request.method == "POST":
        try:
            f = Favorito(
                usuario_id=request.form["usuario_id"],
                anuncio_id=request.form["anuncio_id"],
            )
            db.session.add(f)
            db.session.commit()
            flash("Favorito adicionado!", "success")
        except Exception as e:
            db.session.rollback()
            flash("Já existe esse favorito ou dados inválidos.", "warning")
        return redirect(url_for(".listar"))
    return render_template("favoritos/form.html", favorito=None, usuarios=usuarios, anuncios=anuncios)

@bp.route("/<int:id>/editar", methods=["GET", "POST"])
def editar(id):
    favorito = Favorito.query.get_or_404(id)
    usuarios = Usuario.query.all()
    anuncios = Anuncio.query.all()
    if request.method == "POST":
        favorito.usuario_id = request.form["usuario_id"]
        favorito.anuncio_id = request.form["anuncio_id"]
        try:
            db.session.commit()
            flash("Favorito atualizado!", "success")
        except Exception:
            db.session.rollback()
            flash("Combinação usuário/anúncio já existente.", "warning")
        return redirect(url_for(".listar"))
    return render_template("favoritos/form.html", favorito=favorito, usuarios=usuarios, anuncios=anuncios)

@bp.route("/<int:id>/excluir", methods=["GET", "POST"])
def excluir(id):
    favorito = Favorito.query.get_or_404(id)
    if request.method == "POST":
        db.session.delete(favorito)
        db.session.commit()
        flash("Favorito removido.", "info")
        return redirect(url_for(".listar"))
    return render_template("confirm_delete.html", titulo="Excluir Favorito", item=f"#{favorito.id}", action=url_for(".excluir", id=id))