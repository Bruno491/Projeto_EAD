from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')

    db.init_app(app)
    login.init_app(app)

    from .routes.auth import auth_bp
    from .routes.main import main_bp
    from .routes.listing import listing_bp
    from .routes.question import question_bp
    from .routes.purchase import purchase_bp
    from .routes.favorite import favorite_bp
    from .routes.report import report_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(listing_bp, url_prefix='/listings')
    app.register_blueprint(question_bp, url_prefix='/questions')
    app.register_blueprint(purchase_bp, url_prefix='/purchases')
    app.register_blueprint(favorite_bp, url_prefix='/favorites')
    app.register_blueprint(report_bp, url_prefix='/reports')

    return app