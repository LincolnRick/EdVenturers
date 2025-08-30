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


def calcular_nivel(pontos):
    """Calcula o nível do usuário e o progresso para o próximo nível.

    A cada nível, a quantidade de experiência necessária aumenta
    progressivamente. O primeiro nível requer 100 pontos, o segundo
    requer 200, o terceiro 300 e assim por diante.

    Retorna uma tupla (nivel, progresso), onde ``nivel`` é o nível
    atual e ``progresso`` é a porcentagem (0-100) de experiência
    acumulada no nível atual.
    """

    nivel = 1
    pontos_restantes = pontos or 0
    xp_necessaria = 100

    while pontos_restantes >= xp_necessaria:
        pontos_restantes -= xp_necessaria
        nivel += 1
        xp_necessaria = 100 * nivel

    progresso = int((pontos_restantes / xp_necessaria) * 100) if xp_necessaria else 0
    return nivel, progresso
