# Framework Flask para criação da API
from flask import Flask

# Banco de dados SQL
from flask_sqlalchemy import SQLAlchemy

# Gerenciador de Senhas
from flask_login import LoginManager

# Criptografia de Dados
from flask_bcrypt import Bcrypt

app = Flask(__name__)

# Banco de dados
import os
basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{os.path.join(basedir, '..', 'instance', 'comunidade.db')}"




# pasta padrão de upload de fotos
# # onde são armazenadas as fotos
app.config['UPLOAD_FOLDER'] = '/static/fotos_posts'

# chave de segurança que garante a referencia de segurança do uso do app
app.config["SECRET_KEY"] = "72a3760eee448a3cbc3505881319d511"
database = SQLAlchemy(app)

# Criptografia de dados
bcrypt = Bcrypt(app)


login_manager = LoginManager(app)

## view e routes são a mesma coisa
login_manager.login_view = "homepage"

from taverna import routes
