# taverna/utils.py

from collections import Counter
from taverna.models import Projeto


def get_ranking_de_tags(limit=10):
    projetos = Projeto.query.with_entities(Projeto.tags).all()
    contador = Counter()

    for (tags_str,) in projetos:
        if tags_str:
            tags = [t.strip() for t in tags_str.split(',') if t.strip()]
            contador.update(tags)

    return contador.most_common(limit)


def get_ranking_de_categorias(limit=10):
    projetos = Projeto.query.with_entities(Projeto.categoria).all()
    contador = Counter()

    for (categoria,) in projetos:
        if categoria:
            contador.update([categoria.strip()])

    return contador.most_common(limit)


def get_ranking_de_anos(limit=10):
    projetos = Projeto.query.with_entities(Projeto.ano_escolar).all()
    contador = Counter()

    for (ano,) in projetos:
        if ano:
            contador.update([ano.strip()])

    return contador.most_common(limit)
