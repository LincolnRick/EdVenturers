"""Helper script to ensure the database schema is up to date.

This module is executed during application start-up and can also be run
directly. It checks for the existence of required tables and columns,
creating them when necessary so that the application can operate without
manual migrations.
"""

from taverna import database, app
from sqlalchemy import inspect, text
from taverna.models import Comentario, Projeto, Midia, ComentarioProjeto, Usuario


def upgrade():
    """Verify tables and columns, creating them if missing."""

    with app.app_context():
        inspector = inspect(database.engine)
        tabelas_existentes = inspector.get_table_names()

        # Criar tabelas se não existirem
        if 'comentario' not in tabelas_existentes:
            Comentario.__table__.create(database.engine)
        if 'projeto' not in tabelas_existentes:
            Projeto.__table__.create(database.engine)
        if 'midia' not in tabelas_existentes:
            Midia.__table__.create(database.engine)
        if 'comentarioprojeto' not in tabelas_existentes:
            ComentarioProjeto.__table__.create(database.engine)
        if 'usuario' not in tabelas_existentes:
            Usuario.__table__.create(database.engine)

        # Verificar colunas da tabela midia
        colunas_midia = [col['name'] for col in inspector.get_columns('midia')]
        if 'tags' not in colunas_midia:
            database.session.execute(text("ALTER TABLE midia ADD COLUMN tags TEXT"))
        if 'data_criacao' not in colunas_midia:
            database.session.execute(text("ALTER TABLE midia ADD COLUMN data_criacao DATETIME DEFAULT CURRENT_TIMESTAMP"))

        # Verificar colunas da tabela usuario
        colunas_usuario = [col['name'] for col in inspector.get_columns('usuario')]
        if 'avatar' not in colunas_usuario:
            database.session.execute(text("ALTER TABLE usuario ADD COLUMN avatar TEXT DEFAULT 'avatar1.jpeg'"))
        if 'pontos' not in colunas_usuario:
            database.session.execute(text("ALTER TABLE usuario ADD COLUMN pontos INTEGER DEFAULT 0"))

        database.session.commit()
        print("Banco verificado e atualizado com sucesso.")


if __name__ == "__main__":
    upgrade()
