# coding=utf-8
from tables import ProjetosTable


def index():
    if not session.projetos:
        session.flash = "Você precisa realizar uma busca."
        redirect(URL('default', 'index'))

    table = ProjetosTable(session.projetos)

    return dict(
        result = table.printTable()
    )