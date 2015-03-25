# -*- coding: utf-8 -*-
from forms import controlGroup, selectbox
from SIEProjeto import *


def index():
    session.projetos = None

    projetos = SIEProjeto()
    form = FORM(
        controlGroup( "Título", "titulo", INPUT(_name="TITULO") ),
        controlGroup( "Nome Participante", "participante", INPUT(_name="participante") ),
        controlGroup( "Unidade" , "unidade", selectbox(projetos.unidades(), 'ID_UNIDADE', 'NOME_UNIDADE') ),
        controlGroup( "Ano", 'ano', selectbox(projetos.anos(), 'ANO_REFERENCIA', 'ANO_REFERENCIA') ),
        #controlGroup( "Classificação CNPQ", "area", selectbox(projetos.areasTematicas(), 'ID_AREA', 'AREA_CNPQ') ),
        controlGroup( "Grupo CNPQ", "grupo", selectbox(projetos.gruposCNPQ(), 'ID_CLASSIFICACAO', 'GRUPO_CNPQ')),
        INPUT(_value="Buscar",_type='submit'),
        _class="form-horizontal"
    )

    if form.process().accepted:
        try:
            session.projetos = projetos.getProjetos(form.vars)
            redirect(URL('search', 'index'))
        except ValueError:
            response.flash = "Nenhum projeto encontrado. Tente novamente com novos parâmetros de busca."

    return dict(form=form)