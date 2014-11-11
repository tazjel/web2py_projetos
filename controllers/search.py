from tables import ProjetosTable


def index():
    table = ProjetosTable(session.projetos)

    return dict(
        result = table.printTable()
    )