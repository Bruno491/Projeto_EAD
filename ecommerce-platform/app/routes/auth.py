from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from ..models import Usuario

bp = Blueprint("auth", __name__, template_folder="../templates/auth")

@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        senha = request.form["senha"]
        usuario = Usuario.query.filter_by(email=email).first()
        
        if usuario and usuario.senha == senha:
            login_user(usuario)
            flash("Login realizado com sucesso!", "success")
            return redirect(url_for("usuarios.listar"))
        else:
            flash("Credenciais inválidas", "danger")

    return render_template("auth/login.html")

@bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Você saiu da conta.", "info")
    return redirect(url_for("auth.login"))