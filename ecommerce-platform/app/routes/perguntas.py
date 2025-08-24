from flask import Blueprint, render_template, request, redirect, url_for, flash
from .. import db
from ..models import Pergunta, Usuario, Anuncio
from flask_login import login_required

bp = Blueprint("perguntas", __name__, template_folder="../templates/perguntas")

@bp.route("/")
def listar():
    perguntas = Pergunta.query.order_by(Pergunta.id.desc()).all()
    return render_template("perguntas/list.html", perguntas=perguntas)

@bp.route("/novo", methods=["GET", "POST"])
@login_required
def criar():
    usuarios = Usuario.query.all()
    anuncios = Anuncio.query.all()
    if request.method == "POST":
        p = Pergunta(
            texto=request.form["texto"],
            resposta=request.form.get("resposta") or None,
            anuncio_id=request.form["anuncio_id"],
            usuario_id=request.form["usuario_id"],
        )
        db.session.add(p)
        db.session.commit()
        flash("Pergunta criada!", "success")
        return redirect(url_for(".listar"))
    return render_template("perguntas/form.html", pergunta=None, usuarios=usuarios, anuncios=anuncios)

@bp.route("/<int:id>/editar", methods=["GET", "POST"])
@login_required
def editar(id):
    pergunta = Pergunta.query.get_or_404(id)
    usuarios = Usuario.query.all()
    anuncios = Anuncio.query.all()
    if request.method == "POST":
        pergunta.texto = request.form["texto"]
        pergunta.resposta = request.form.get("resposta") or None
        pergunta.anuncio_id = request.form["anuncio_id"]
        pergunta.usuario_id = request.form["usuario_id"]
        db.session.commit()
        flash("Pergunta atualizada!", "success")
        return redirect(url_for(".listar"))
    return render_template("perguntas/form.html", pergunta=pergunta, usuarios=usuarios, anuncios=anuncios)

@bp.route("/<int:id>/excluir", methods=["GET", "POST"])
@login_required
def excluir(id):
    pergunta = Pergunta.query.get_or_404(id)
    if request.method == "POST":
        db.session.delete(pergunta)
        db.session.commit()
        flash("Pergunta excluída.", "info")
        return redirect(url_for(".listar"))
    return render_template("confirm_delete.html", titulo="Excluir Pergunta", item=f"#{pergunta.id}", action=url_for(".excluir", id=id))