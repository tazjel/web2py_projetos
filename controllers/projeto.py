# -*- coding: utf-8 -*-
def index():
    tableProjeto = ResumoTable(dbfunctions.getProjetoById(request.vars.ID_PROJETO))

    tableParticipantes = ParticipantesTable(
        dbfunctions.getParticipantes(request.vars.ID_PROJETO),
        "Participante Função E-mail Vínculo Vigência".split()
    )

    tableClassificacoes = ClassificacoesTable(
        dbfunctions.getClassificacoes(request.vars.ID_PROJETO),
        "Tipo Classificação".split()
    )

    return dict(
        projeto=tableProjeto.printTable(),
        participantes=tableParticipantes.printTable("dr-table rich-table table table-striped"),
        classificacoes=tableClassificacoes.printTable("dr-table rich-table table table-striped")
    )