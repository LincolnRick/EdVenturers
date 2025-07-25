# Ferramenta de criação do Banco de dados

# # Importação dos módulos do Notebook vinculados
from taverna import database, app
from taverna import models

# comando de criação de banco
with app.app_context():
    database.create_all()