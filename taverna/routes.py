from taverna import app, database, bcrypt
from taverna.forms import (
    FormLogin, FormCriarConta, FormProjeto,
    FormComentario, FormComentarioProjeto
)
from taverna.models import (
    Usuario, Projeto, Comentario, ComentarioProjeto, Midia
)
from flask import render_template, url_for, redirect, request
from flask_login import login_required, login_user, logout_user, current_user
import os
from werkzeug.utils import secure_filename

from taverna.utils import (
    get_ranking_de_tags,
    get_ranking_de_categorias,
    get_ranking_de_anos
)



# ---------------- Página Inicial ----------------
@app.route("/", methods=["GET", "POST"])
def homepage():
    form_login = FormLogin()
    if form_login.validate_on_submit():
        usuario = Usuario.query.filter_by(email=form_login.email.data).first()
        if usuario and bcrypt.check_password_hash(usuario.senha, form_login.senha.data):
            login_user(usuario)
            return redirect(url_for("perfil", id_usuario=usuario.id))
    return render_template("homepage.html", form=form_login)


# ---------------- Criação de Conta ----------------
@app.route("/criarconta", methods=["GET", "POST"])
def criarconta():
    form = FormCriarConta()
    if form.validate_on_submit():
        senha = bcrypt.generate_password_hash(form.senha.data)
        usuario = Usuario(
            username=form.username.data,
            email=form.email.data,
            senha=senha,
            avatar=form.avatar.data
        )
        database.session.add(usuario)
        database.session.commit()
        login_user(usuario, remember=True)
        return redirect(url_for("perfil", id_usuario=usuario.id))
    return render_template("criarconta.html", form=form)


# ---------------- Helper Function for Project Creation ----------------
def criar_projeto(form_projeto, usuario_id):
    projeto = Projeto(
        titulo=form_projeto.titulo.data,
        descricao=form_projeto.descricao.data,
        conteudo=form_projeto.conteudo.data,
        categoria=form_projeto.categoria.data,
        ano_escolar=form_projeto.ano_escolar.data,
        tags=form_projeto.tags.data,
        id_usuario=usuario_id
    )
    database.session.add(projeto)
    database.session.commit()

    arquivos = form_projeto.arquivos.data or []
    for arquivo in arquivos:
        if arquivo and arquivo.filename:
            nome_seguro = secure_filename(arquivo.filename)
            caminho = os.path.join(app.root_path, 'static', 'projetos_midias', nome_seguro)
            arquivo.save(caminho)
            extensao = nome_seguro.rsplit('.', 1)[-1].lower()
            midia = Midia(
                nome_arquivo=nome_seguro,
                tipo=extensao,
                id_projeto=projeto.id,
                id_usuario=usuario_id
            )
            database.session.add(midia)
    database.session.commit()
    return projeto

# ---------------- Perfil com Upload de Projeto ----------------
@app.route("/perfil/<id_usuario>", methods=["GET", "POST"])
@login_required
def perfil(id_usuario):
    usuario = Usuario.query.get_or_404(int(id_usuario))
    form_projeto = FormProjeto()
    form_comentario = FormComentario()

    # Criação de novo projeto com arquivos
    if current_user.id == usuario.id and form_projeto.validate_on_submit():
        criar_projeto(form_projeto, current_user.id)
        return redirect(url_for("perfil", id_usuario=usuario.id))

    return render_template(
        "perfil.html",
        usuario=usuario,
        form=form_projeto,
        form_comentario=form_comentario
    )


# ---------------- Feed Global (com filtro por tags) ----------------
@app.route("/feed", methods=["GET", "POST"])
@login_required
def feed():
    form_comentario = FormComentario()

    # Filtros
    tag_filtro = request.args.get("tag", "").strip()
    categoria_filtro = request.args.get("categoria", "").strip()
    ano_filtro = request.args.get("ano", "").strip()

    # Base da query
    query = Projeto.query

    if tag_filtro:
        query = query.filter(Projeto.tags.ilike(f"%{tag_filtro}%"))
    if categoria_filtro:
        query = query.filter(Projeto.categoria == categoria_filtro)
    if ano_filtro:
        query = query.filter(Projeto.ano_escolar == ano_filtro)

    projetos = query.order_by(Projeto.data_criacao.desc()).all()

    # Rankings
    tags_rank = get_ranking_de_tags()
    categorias_rank = get_ranking_de_categorias()
    anos_rank = get_ranking_de_anos()

    if form_comentario.validate_on_submit():
        id_midia = int(request.form["id_midia"])
        novo_comentario = Comentario(
            texto=form_comentario.texto.data,
            id_usuario=current_user.id,
            id_midia=id_midia
        )
        database.session.add(novo_comentario)
        database.session.commit()
        return redirect(url_for("feed", tag=tag_filtro or None, categoria=categoria_filtro or None, ano=ano_filtro or None))

    return render_template(
        "feed.html",
        projetos=projetos,
        form_comentario=form_comentario,
        tag_filtro=tag_filtro,
        categoria_filtro=categoria_filtro,
        ano_filtro=ano_filtro,
        tags_rank=tags_rank,
        categorias_rank=categorias_rank,
        anos_rank=anos_rank
    )


# ---------------- Rotas auxiliares ----------------
@app.route("/taverna")
def taverna():
    return render_template("taverna.html")

@app.route("/missoes")
def missoes():
    return render_template("missoes.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("homepage"))

@app.route("/novo_projeto", methods=["GET", "POST"])
@login_required
def novo_projeto():
    form_projeto = FormProjeto()
    if form_projeto.validate_on_submit():
        criar_projeto(form_projeto, current_user.id)
        return redirect(url_for("perfil", id_usuario=current_user.id))

    return render_template("novo_projeto.html", form=form_projeto)

@app.route("/projeto/<int:id_projeto>", methods=["GET", "POST"])
@login_required
def visualizar_projeto(id_projeto):
    projeto = Projeto.query.get_or_404(id_projeto)
    form_comentario = FormComentario()

    if form_comentario.validate_on_submit():
        novo_comentario = ComentarioProjeto(
    texto=form_comentario.texto.data,
    id_usuario=current_user.id,
    id_projeto=id_projeto
)

        database.session.add(novo_comentario)
        database.session.commit()
        return redirect(url_for("visualizar_projeto", id_projeto=projeto.id))

    return render_template(
        "visualizar_projeto.html",
        projeto=projeto,
        form_comentario=form_comentario
    )

@app.route('/sponsors')
def sponsors():
    return render_template('sponsors.html')
