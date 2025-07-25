# forms.py

from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import (
    StringField, PasswordField, SubmitField, TextAreaField, MultipleFileField, RadioField
)
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from taverna.models import Usuario

# ---------- Formulário de Login ----------
class FormLogin(FlaskForm):
    email = StringField("E-mail", validators=[DataRequired(), Email()])
    senha = PasswordField("Senha", validators=[DataRequired()])
    botao_confirmacao = SubmitField("Entrar na Taverna")

# ---------- Formulário de Criação de Conta ----------
from wtforms import RadioField  # Certifique-se que essa importação esteja presente

class FormCriarConta(FlaskForm):
    email = StringField("E-mail", validators=[DataRequired(), Email()])
    username = StringField("Username", validators=[DataRequired()])
    senha = PasswordField("Senha", validators=[DataRequired(), Length(6, 20)])
    confirmacao_senha = PasswordField("Confirmação de senha", validators=[
        DataRequired(), EqualTo("senha")
    ])
    
    avatar = RadioField("Avatar", choices=[
        ("avatar1.jpeg", "Avatar 1"),
        ("avatar2.jpeg", "Avatar 2"),
        ("avatar3.jpeg", "Avatar 3"),
        ("avatar4.jpeg", "Avatar 4"),
        ("avatar5.jpg", "Avatar 5")
    ], default="avatar1.jpeg")

    botao_confirmacao = SubmitField("Criar Conta")

    # ✅ Apenas uma função de validação é suficiente
    def validate_email(self, email):
        usuario = Usuario.query.filter_by(email=email.data).first()
        if usuario:
            raise ValidationError("E-mail já cadastrado! Faça login para continuar, meu chapa!")


# ---------- Formulário de Upload de Arquivo Avulso ----------
class FormFoto(FlaskForm):
    foto = FileField("Arquivo", validators=[
        DataRequired(),
        FileAllowed(['jpg', 'png', 'pdf', 'docx', 'pptx', 'mp4'], 
                    "Formatos permitidos: .jpg, .png, .pdf, .docx, .pptx, .mp4")
    ])
    tags = StringField("Tags (separadas por vírgula)")
    botao_confirmacao = SubmitField("Enviar")

# ---------- Formulário para Comentários em Arquivos ou Projetos ----------
class FormComentario(FlaskForm):
    texto = TextAreaField("Comentário", validators=[DataRequired(), Length(max=200)])
    botao_comentario = SubmitField("Comentar")

# ---------- Formulário para Criar Projeto com Upload de Arquivos ----------
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FileField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length
from flask_wtf.file import FileAllowed, FileRequired, FileField

class FormProjeto(FlaskForm):
    titulo = StringField("Título", validators=[DataRequired()])
    descricao = TextAreaField("Descrição", validators=[DataRequired()])
    conteudo = TextAreaField("Conteúdo adicional")
    
    categoria = SelectField("Categoria", choices=[
        ("História", "História"),
        ("Matemática", "Matemática"),
        ("Português", "Português"),
        ("Ciências", "Ciências"),
        ("Geografia", "Geografia"),
        ("Outra", "Outra")
    ], validators=[DataRequired()])
    
    ano_escolar = SelectField("Ano Escolar", choices=[
        ("1º Ano", "1º Ano"),
        ("2º Ano", "2º Ano"),
        ("3º Ano", "3º Ano"),
        ("4º Ano", "4º Ano"),
        ("5º Ano", "5º Ano")
    ], validators=[DataRequired()])
    
    tags = StringField("Tags (mínimo 1)", validators=[DataRequired(), Length(min=2)])

    arquivos = MultipleFileField("Arquivos", validators=[
    FileAllowed(['jpg', 'jpeg', 'png', 'mp4', 'pdf', 'doc', 'docx', 'ppt', 'pptx'], "Tipos permitidos.")
])
    
    botao_confirmacao = SubmitField("Enviar Projeto")



# ---------- Comentários Específicos para Projetos ----------
class FormComentarioProjeto(FlaskForm):
    texto = TextAreaField("Comentário", validators=[DataRequired()])
    botao_comentario = SubmitField("Comentar")
