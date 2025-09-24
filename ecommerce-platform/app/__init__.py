import os
from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from urllib.parse import quote_plus
from dotenv import load_dotenv
from flask_login import LoginManager
login_manager = LoginManager()

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    load_dotenv()

    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev")
 
    app.config["SQLALCHEMY_DATABASE_URI"] = (
    "mssql+pyodbc://sa:Fenix9710%409710@(localdb)\\MSSQLLocalDB/Trabalho_EAD?driver=ODBC+Driver+17+for+SQL+Server"
)
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    login_manager.login_message_category = "info"

    print(">>> Conectando em:", app.config["SQLALCHEMY_DATABASE_URI"])

    # Importa models e blueprints
    from .models import Usuario, Categoria, Anuncio, Pergunta, Compra, Favorito
    from .routes.usuarios    import bp as usuarios_bp
    from .routes.categorias  import bp as categorias_bp
    from .routes.anuncios    import bp as anuncios_bp
    from .routes.perguntas   import bp as perguntas_bp
    from .routes.compras     import bp as compras_bp
    from .routes.favoritos   import bp as favoritos_bp
    from .routes import auth

    # Registra blueprints
    app.register_blueprint(usuarios_bp,   url_prefix="/usuarios")
    app.register_blueprint(categorias_bp, url_prefix="/categorias")
    app.register_blueprint(anuncios_bp,   url_prefix="/anuncios")
    app.register_blueprint(perguntas_bp,  url_prefix="/perguntas")
    app.register_blueprint(compras_bp,    url_prefix="/compras")
    app.register_blueprint(favoritos_bp,  url_prefix="/favoritos")
    app.register_blueprint(auth.bp,       url_prefix="/auth")

    @login_manager.user_loader
    def load_user(user_id):
        return Usuario.query.get(int(user_id))

    @app.route("/")
    def index():
        return redirect(url_for("anuncios.listar"))

    @app.cli.command("init-db")
    def init_db():
        """Cria as tabelas que ainda não existem no banco."""
        db.create_all()
        print("Tabelas verificadas/criadas com sucesso.")

    return app
    db.init_app(app)
    
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    login_manager.login_message_category = "info"


    print(">>> Conectando em:", app.config["SQLALCHEMY_DATABASE_URI"])

    from .models import Usuario, Categoria, Anuncio, Pergunta, Compra, Favorito

    from .routes.usuarios    import bp as usuarios_bp
    from .routes.categorias  import bp as categorias_bp
    from .routes.anuncios    import bp as anuncios_bp
    from .routes.perguntas   import bp as perguntas_bp
    from .routes.compras     import bp as compras_bp
    from .routes.favoritos   import bp as favoritos_bp
    from .models import Usuario
    from .routes import auth

    app.register_blueprint(usuarios_bp,   url_prefix="/usuarios")
    app.register_blueprint(categorias_bp, url_prefix="/categorias")
    app.register_blueprint(anuncios_bp,   url_prefix="/anuncios")
    app.register_blueprint(perguntas_bp,  url_prefix="/perguntas")
    app.register_blueprint(compras_bp,    url_prefix="/compras")
    app.register_blueprint(favoritos_bp,  url_prefix="/favoritos")
    app.register_blueprint(auth.bp, url_prefix="/auth")

    
    @login_manager.user_loader
    def load_user(user_id):
        return Usuario.query.get(int(user_id))


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