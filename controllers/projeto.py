# -*- coding: utf-8 -*-
from tables import ParticipantesTable, ClassificacoesTable, ResumoTable
from SIEProjeto import *


@cache.action(time_expire=300000, cache_model=cache.disk, quick='VP')
def index():
    projetos = SIEProjeto()
    tableProjeto = ResumoTable(projetos.getProjetos(request.vars)[0])       # Uma consulta por ID_PROJETO sempre retornará uma úncia entrada

    tableParticipantes = ParticipantesTable(
        projetos.getParticipantes(request.vars),
        "Participante Função E-mail Vínculo Vigência".split()
    )

    # tableClassificacoes = ClassificacoesTable(
    #     projetos.getClassificacoes(request.vars.ID_PROJETO),
    #     "Tipo Classificação".split()
    # )

    return dict(
        projeto=tableProjeto.printTable(),
        participantes=tableParticipantes.printTable("dr-table rich-table table table-striped"),
        # classificacoes=tableClassificacoes.printTable("dr-table rich-table table table-striped")
    )