from EdVenture.taverna import database, login_manager
from datetime import datetime
from flask_login import UserMixin

# ---------- Carregamento do usuário logado ----------
@login_manager.user_loader
def load_usuario(id_usuario):
    return Usuario.query.get(int(id_usuario))

# ---------- Modelo de Usuário ----------
class Usuario(database.Model, UserMixin):
    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String, nullable=False)
    email = database.Column(database.String, nullable=False, unique=True)
    senha = database.Column(database.String, nullable=False)

    avatar = database.Column(database.String, default="avatar1.jpeg")  # <- novo campo

    # Relacionamentos
    projetos = database.relationship("Projeto", backref="autor", lazy=True)
    midias = database.relationship("Midia", backref="usuario", lazy=True)
    comentarios_midia = database.relationship("Comentario", backref="usuario", lazy=True)
    comentarios_projeto = database.relationship("ComentarioProjeto", backref="usuario", lazy=True)


# ---------- Modelo de Projeto ----------
class Projeto(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    titulo = database.Column(database.String, nullable=False)
    descricao = database.Column(database.Text, nullable=False)
    conteudo = database.Column(database.Text)
    tags = database.Column(database.String, nullable=False)
    categoria = database.Column(database.String, nullable=False)
    ano_escolar = database.Column(database.String, nullable=False)
    objetivo = database.Column(database.String)  # opcional
    data_criacao = database.Column(database.DateTime, default=datetime.utcnow)

    id_usuario = database.Column(database.Integer, database.ForeignKey('usuario.id'), nullable=False)

    # Relacionamentos
    midias = database.relationship('Midia', backref='projeto', lazy=True)
    comentarios = database.relationship('ComentarioProjeto', backref='projeto', lazy=True)

# ---------- Modelo de Mídia (Imagens, Vídeos, Docs, etc.) ----------
class Midia(database.Model):
    __tablename__ = "midia"

    id = database.Column(database.Integer, primary_key=True)
    nome_arquivo = database.Column(database.String(200), nullable=False)
    tipo = database.Column(database.String(20))  # jpg, mp4, pdf, etc.
    tags = database.Column(database.String(255))
    data_criacao = database.Column(database.DateTime, default=datetime.utcnow)

    id_projeto = database.Column(database.Integer, database.ForeignKey("projeto.id"), nullable=True)
    id_usuario = database.Column(database.Integer, database.ForeignKey("usuario.id"), nullable=False)

    # Relacionamentos
    comentarios = database.relationship("Comentario", backref="midia", lazy=True)

# ---------- Modelo de Comentários em Projetos ----------
class ComentarioProjeto(database.Model):
    __tablename__ = "comentarioprojeto"

    id = database.Column(database.Integer, primary_key=True)
    texto = database.Column(database.Text, nullable=False)
    data_criacao = database.Column(database.DateTime, default=datetime.utcnow)

    id_usuario = database.Column(database.Integer, database.ForeignKey("usuario.id"), nullable=False)
    id_projeto = database.Column(database.Integer, database.ForeignKey("projeto.id"), nullable=False)

# ---------- Modelo de Comentários em Mídias ----------
class Comentario(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    texto = database.Column(database.Text, nullable=False)
    data_criacao = database.Column(database.DateTime, default=datetime.utcnow)

    id_usuario = database.Column(database.Integer, database.ForeignKey('usuario.id'), nullable=False)
    id_midia = database.Column(database.Integer, database.ForeignKey('midia.id'), nullable=False)
