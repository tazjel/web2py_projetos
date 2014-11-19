# -*- coding: utf-8 -*-
from forms import controlGroup, selectbox
from tables import ProjetosTable
from SIEProjeto import *


def index():
    session.projetos = None

    projetos = SIEProjeto()
    form = FORM(
        controlGroup( "Título", "titulo", INPUT(_name="TITULO") ),
        controlGroup( "Nome Participante", "participante", INPUT(_name="participante") ),
        controlGroup( "Unidade" , "unidade", selectbox(projetos.unidades(), 'ID_UNIDADE', 'NOME_UNIDADE') ),
        controlGroup( "Ano", 'ano', selectbox(projetos.anos(), 'ANO_REFERENCIA', 'ANO_REFERENCIA') ),
        controlGroup( "Classificação CNPQ", "area", selectbox(projetos.areasTematicas(), 'ID_AREA', 'AREA_CNPQ') ),
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


def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/manage_users (requires membership in
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()

