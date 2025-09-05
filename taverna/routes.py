from taverna import app, database, bcrypt
from taverna.forms import (
    FormLogin, FormCriarConta, FormProjeto,
    FormComentario, FormComentarioProjeto
)
from taverna.models import (
    Usuario, Projeto, Comentario, ComentarioProjeto, Midia
)
from flask import render_template, url_for, redirect, request, abort
from flask_login import login_required, login_user, logout_user, current_user
import os
import mimetypes
from werkzeug.utils import secure_filename
from sqlalchemy import or_

from taverna.utils import (
    get_ranking_de_tags,
    get_ranking_de_categorias,
    get_ranking_de_anos,
    calcular_nivel
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
            dir_midias = os.path.join(app.root_path, 'static', 'projetos_midias')
            os.makedirs(dir_midias, exist_ok=True)
            caminho = os.path.join(dir_midias, nome_seguro)
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

    usuario = Usuario.query.get(usuario_id)
    if usuario:
        usuario.pontos = (usuario.pontos or 0) + 10
        database.session.commit()

    return projeto

# ---------------- Perfil com Upload de Projeto ----------------
@app.route("/perfil/<id_usuario>", methods=["GET", "POST"])
@login_required
def perfil(id_usuario):
    usuario = Usuario.query.get_or_404(int(id_usuario))
    form_projeto = FormProjeto()
    form_comentario = FormComentario()

    nivel, progresso = calcular_nivel(usuario.pontos)

    # Criação de novo projeto com arquivos
    if current_user.id == usuario.id and form_projeto.validate_on_submit():
        criar_projeto(form_projeto, current_user.id)
        return redirect(url_for("perfil", id_usuario=usuario.id))

    return render_template(
        "perfil.html",
        usuario=usuario,
        form=form_projeto,
        form_comentario=form_comentario,
        nivel=nivel,
        progresso=progresso
    )


# ---------------- Feed Global com filtros unificados ----------------
@app.route("/feed", methods=["GET", "POST"])
@login_required
def feed():
    form_comentario = FormComentario()

    # Opções de filtros
    years = [ano for ano, _ in get_ranking_de_anos(limit=20)]
    categories = [cat for cat, _ in get_ranking_de_categorias(limit=20)]
    tags = [tag for tag, _ in get_ranking_de_tags(limit=30)]

    # Valores selecionados
    sel_years = request.args.getlist('year')
    sel_cats = request.args.getlist('category')
    sel_tags = request.args.getlist('tag')
    q_user = request.args.get('q_user', '').strip()

    # Base da query
    query = Projeto.query

    if sel_years:
        query = query.filter(Projeto.ano_escolar.in_(sel_years))
    if sel_cats:
        query = query.filter(Projeto.categoria.in_(sel_cats))
    if sel_tags:
        filtros_tag = [Projeto.tags.ilike(f"%{t}%") for t in sel_tags]
        query = query.filter(or_(*filtros_tag))
    if q_user:
        query = query.join(Usuario).filter(
            or_(Usuario.username.ilike(f"%{q_user}%"), Usuario.email.ilike(f"%{q_user}%"))
        )

    page = int(request.args.get('page', 1))
    per_page = 12
    pagination = query.order_by(Projeto.data_criacao.desc()).paginate(page=page, per_page=per_page, error_out=False)
    projetos = pagination.items

    niveis_autores = {
        projeto.autor.id: calcular_nivel(projeto.autor.pontos)[0]
        for projeto in projetos
    }

    if form_comentario.validate_on_submit():
        id_midia = int(request.form["id_midia"])
        novo_comentario = Comentario(
            texto=form_comentario.texto.data,
            id_usuario=current_user.id,
            id_midia=id_midia
        )
        database.session.add(novo_comentario)
        usuario = Usuario.query.get(current_user.id)
        if usuario:
            usuario.pontos = (usuario.pontos or 0) + 2
        database.session.commit()
        return redirect(url_for("feed", **request.args.to_dict(flat=False)))

    return render_template(
        "feed.html",
        projetos=projetos,
        form_comentario=form_comentario,
        years=years,
        categories=categories,
        tags=tags,
        pagination=pagination,
        niveis_autores=niveis_autores
    )


# ---------------- Rotas auxiliares ----------------
@app.route("/taverna")
def taverna():
    ranking_usuarios = Usuario.query.order_by(Usuario.pontos.desc()).limit(5).all()
    niveis = {u.id: calcular_nivel(u.pontos)[0] for u in ranking_usuarios}
    return render_template("taverna.html", ranking_usuarios=ranking_usuarios, niveis=niveis)

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

@app.route("/projeto/<int:id_projeto>/editar", methods=["GET", "POST"])
@login_required
def editar_projeto(id_projeto):
    projeto = Projeto.query.get_or_404(id_projeto)
    if projeto.id_usuario != current_user.id:
        abort(403)

    form_projeto = FormProjeto()
    if form_projeto.validate_on_submit():
        projeto.titulo = form_projeto.titulo.data
        projeto.descricao = form_projeto.descricao.data
        projeto.conteudo = form_projeto.conteudo.data
        projeto.categoria = form_projeto.categoria.data
        projeto.ano_escolar = form_projeto.ano_escolar.data
        projeto.tags = form_projeto.tags.data

        arquivos = form_projeto.arquivos.data or []
        for arquivo in arquivos:
            if arquivo and arquivo.filename:
                nome_seguro = secure_filename(arquivo.filename)
                dir_midias = os.path.join(app.root_path, 'static', 'projetos_midias')
                os.makedirs(dir_midias, exist_ok=True)
                caminho = os.path.join(dir_midias, nome_seguro)
                arquivo.save(caminho)
                extensao = nome_seguro.rsplit('.', 1)[-1].lower()
                midia = Midia(
                    nome_arquivo=nome_seguro,
                    tipo=extensao,
                    id_projeto=projeto.id,
                    id_usuario=current_user.id
                )
                database.session.add(midia)
        database.session.commit()
        return redirect(url_for("visualizar_projeto", id_projeto=projeto.id))
    elif request.method == "GET":
        form_projeto.titulo.data = projeto.titulo
        form_projeto.descricao.data = projeto.descricao
        form_projeto.conteudo.data = projeto.conteudo
        form_projeto.categoria.data = projeto.categoria
        form_projeto.ano_escolar.data = projeto.ano_escolar
        form_projeto.tags.data = projeto.tags

    return render_template("novo_projeto.html", form=form_projeto, projeto=projeto)

@app.route("/projeto/<int:id_projeto>", methods=["GET", "POST"])
@login_required
def visualizar_projeto(id_projeto):
    projeto = Projeto.query.get_or_404(id_projeto)
    form_comentario = FormComentario()

    projeto.title = projeto.titulo
    midias = []
    for m in projeto.midias:
        caminho = f"projetos_midias/{m.nome_arquivo}"
        mime_type, _ = mimetypes.guess_type(m.nome_arquivo)
        midias.append({
            "filepath": caminho,
            "mime_type": mime_type,
            "alt": m.nome_arquivo
        })
    projeto.media = midias

    if form_comentario.validate_on_submit():
        novo_comentario = ComentarioProjeto(
            texto=form_comentario.texto.data,
            id_usuario=current_user.id,
            id_projeto=id_projeto
        )

        database.session.add(novo_comentario)
        usuario = Usuario.query.get(current_user.id)
        if usuario:
            usuario.pontos = (usuario.pontos or 0) + 2
        database.session.commit()
        return redirect(url_for("visualizar_projeto", id_projeto=projeto.id))

    return render_template(
        "visualizar_projeto.html",
        project=projeto,
        comments=projeto.comentarios,
        form=form_comentario
    )


# ---------------- Edição de comentário em projeto ----------------
@app.route("/comentario/<int:id_comentario>/editar", methods=["GET", "POST"])
@login_required
def editar_comentario(id_comentario):
    comentario = ComentarioProjeto.query.get_or_404(id_comentario)
    if comentario.id_usuario != current_user.id:
        abort(403)

    form = FormComentario()
    if form.validate_on_submit():
        comentario.texto = form.texto.data
        database.session.commit()
        return redirect(url_for("visualizar_projeto", id_projeto=comentario.id_projeto))
    elif request.method == "GET":
        form.texto.data = comentario.texto
    return render_template("editar_comentario.html", form=form, comentario=comentario)


# ---------------- Remoção de comentário em projeto ----------------
@app.route("/comentario/<int:id_comentario>/deletar", methods=["POST"])
@login_required
def deletar_comentario(id_comentario):
    comentario = ComentarioProjeto.query.get_or_404(id_comentario)
    if comentario.id_usuario != current_user.id:
        abort(403)
    id_projeto = comentario.id_projeto
    database.session.delete(comentario)
    database.session.commit()
    return redirect(url_for("visualizar_projeto", id_projeto=id_projeto))


# ---------------- Remoção de projeto (punitivo leve) ----------------
@app.route("/projeto/<int:id_projeto>/deletar", methods=["POST"])
@login_required
def deletar_projeto(id_projeto):
    projeto = Projeto.query.get_or_404(id_projeto)
    if projeto.id_usuario != current_user.id:
        abort(403)

    for midia in projeto.midias:
        caminho = os.path.join(app.root_path, 'static', 'projetos_midias', midia.nome_arquivo)
        if os.path.exists(caminho):
            os.remove(caminho)
        database.session.delete(midia)

    for comentario in projeto.comentarios:
        database.session.delete(comentario)

    database.session.delete(projeto)

    usuario = Usuario.query.get(current_user.id)
    if usuario:
        usuario.pontos = max(0, (usuario.pontos or 0) - 5)

    database.session.commit()
    return redirect(url_for("perfil", id_usuario=current_user.id))

@app.route('/sponsors')
def sponsors():
    return render_template('sponsors.html')
