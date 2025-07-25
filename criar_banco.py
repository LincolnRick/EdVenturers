# Ferramenta de criação do Banco de dados

# # Importação dos módulos do Notebook vinculados
from EdVenture.taverna import database, app
from EdVenture.taverna import models

# comando de criação de banco
with app.app_context():
    database.create_all()