from datetime import datetime
from . import db

class Usuario(db.Model):
    __tablename__ = "usuarios"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha = db.Column(db.String(255), nullable=False)

    anuncios  = db.relationship("Anuncio", backref="dono", lazy=True, cascade="all, delete-orphan")
    perguntas = db.relationship("Pergunta", backref="autor", lazy=True, cascade="all, delete-orphan")
    compras   = db.relationship("Compra", backref="comprador", lazy=True, cascade="all, delete-orphan")
    favoritos = db.relationship("Favorito", backref="usuario", lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Usuario {self.id} – {self.email}>"

class Categoria(db.Model):
    __tablename__ = "categorias"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False, unique=True)
    anuncios = db.relationship("Anuncio", backref="categoria", lazy=True)

    def __repr__(self):
        return f"<Categoria {self.id} – {self.nome}>"

class Anuncio(db.Model):
    __tablename__ = "anuncios"

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(120), nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    preco = db.Column(db.Numeric(10, 2), nullable=False)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    usuario_id = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=False)
    categoria_id = db.Column(db.Integer, db.ForeignKey("categorias.id"), nullable=False)

    perguntas = db.relationship("Pergunta", backref="anuncio", lazy=True, cascade="all, delete-orphan")
    compras = db.relationship("Compra", backref="anuncio", lazy=True)
    favoritos = db.relationship("Favorito", backref="anuncio", lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Anuncio {self.id} – {self.titulo}>"

class Pergunta(db.Model):
    __tablename__ = "perguntas"

    id = db.Column(db.Integer, primary_key=True)
    texto = db.Column(db.Text, nullable=False)
    resposta = db.Column(db.Text)
    criado_em  = db.Column(db.DateTime, default=datetime.utcnow,nullable=False)

    anuncio_id = db.Column(db.Integer, db.ForeignKey("anuncios.id"), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=False)

    def __repr__(self):
        return f"<Pergunta {self.id} – Anúncio {self.anuncio_id}>"

class Compra(db.Model):
    __tablename__ = "compras"

    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    anuncio_id = db.Column(db.Integer, db.ForeignKey("anuncios.id"), nullable=False)
    comprador_id = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=False)

    def __repr__(self):
        return f"<Compra {self.id} – {self.data}>"

class Favorito(db.Model):
    __tablename__ = "favoritos"

    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=False)
    anuncio_id = db.Column(db.Integer, db.ForeignKey("anuncios.id"), nullable=False)

    __table_args__ = (db.UniqueConstraint("usuario_id", "anuncio_id",name="uq_usuario_anuncio_favorito"),)

    def __repr__(self): return f"<Favorito U{self.usuario_id}–A{self.anuncio_id}>"