import os
from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from urllib.parse import quote_plus
from dotenv import load_dotenv

db = SQLAlchemy()

def create_app():
    load_dotenv()

    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev")

    server   = os.getenv("DB_SERVER", "SeuServidorAqui")
    database = os.getenv("DB_NAME", "SeuBancoAqui")
    user     = os.getenv("DB_USER", "SeuUsuarioAqui")
    password = os.getenv("DB_PASS", "SuaSenhaAqui")

    odbc_str = (
        f"DRIVER={{ODBC Driver 17 for SQL Server}};"
        f"SERVER={server};"
        f"DATABASE={database};"
        f"UID={user};"
        f"PWD={password};"
        "TrustServerCertificate=yes;"
    )
    connect_uri = "mssql+pyodbc:///?odbc_connect=" + quote_plus(odbc_str)

    app.config["SQLALCHEMY_DATABASE_URI"]        = os.getenv("DATABASE_URL", connect_uri)
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    print(">>> Conectando em:", app.config["SQLALCHEMY_DATABASE_URI"])

    from .models import Usuario, Categoria, Anuncio, Pergunta, Compra, Favorito

    from .routes.usuarios    import bp as usuarios_bp
    from .routes.categorias  import bp as categorias_bp
    from .routes.anuncios    import bp as anuncios_bp
    from .routes.perguntas   import bp as perguntas_bp
    from .routes.compras     import bp as compras_bp
    from .routes.favoritos   import bp as favoritos_bp

    app.register_blueprint(usuarios_bp,   url_prefix="/usuarios")
    app.register_blueprint(categorias_bp, url_prefix="/categorias")
    app.register_blueprint(anuncios_bp,   url_prefix="/anuncios")
    app.register_blueprint(perguntas_bp,  url_prefix="/perguntas")
    app.register_blueprint(compras_bp,    url_prefix="/compras")
    app.register_blueprint(favoritos_bp,  url_prefix="/favoritos")

    @app.route("/")
    def index():
        return redirect(url_for("anuncios.listar"))

    @app.cli.command("init-db")
    def init_db():
        """Recria todas as tabelas do banco."""
        db.drop_all()
        db.create_all()
        print("Banco inicializado.")

    return app