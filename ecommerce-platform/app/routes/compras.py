from flask import Blueprint, render_template, request, redirect, url_for, flash
from .. import db
from ..models import Compra, Usuario, Anuncio
from flask_login import login_required

bp = Blueprint("compras", __name__, template_folder="../templates/compras")

@bp.route("/")
def listar():
    compras = Compra.query.order_by(Compra.id.desc()).all()
    return render_template("compras/list.html", compras=compras)

@bp.route("/novo", methods=["GET", "POST"])
@login_required
def criar():
    usuarios = Usuario.query.all()
    anuncios = Anuncio.query.all()
    if request.method == "POST":
        c = Compra(
            anuncio_id=request.form["anuncio_id"],
            comprador_id=request.form["comprador_id"],
        )
        db.session.add(c)
        db.session.commit()
        flash("Compra registrada!", "success")
        return redirect(url_for(".listar"))
    return render_template("compras/form.html", compra=None, usuarios=usuarios, anuncios=anuncios)

@bp.route("/<int:id>/editar", methods=["GET", "POST"])
@login_required
def editar(id):
    compra = Compra.query.get_or_404(id)
    usuarios = Usuario.query.all()
    anuncios = Anuncio.query.all()
    if request.method == "POST":
        compra.anuncio_id = request.form["anuncio_id"]
        compra.comprador_id = request.form["comprador_id"]
        db.session.commit()
        flash("Compra atualizada!", "success")
        return redirect(url_for(".listar"))
    return render_template("compras/form.html", compra=compra, usuarios=usuarios, anuncios=anuncios)

@bp.route("/<int:id>/excluir", methods=["GET", "POST"])
@login_required
def excluir(id):
    compra = Compra.query.get_or_404(id)
    if request.method == "POST":
        db.session.delete(compra)
        db.session.commit()
        flash("Compra excluída.", "info")
        return redirect(url_for(".listar"))
    return render_template("confirm_delete.html", titulo="Excluir Compra", item=f"#{compra.id}", action=url_for(".excluir", id=id))