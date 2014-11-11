# -*- coding: utf-8 -*-
from forms import controlGroup, selectbox
from tables import ProjetosTable
from SIEProjeto import *


@cache(request.env.path_info, time_expire=600, cache_model=cache.ram)
def index():
    projetos = SIEProjeto()
    form = FORM(
                controlGroup( "Título", "titulo", INPUT(_name="titulo") ),
                controlGroup( "Nome Participante", "participante", INPUT(_name="participante") ),
                controlGroup( "Unidade" , "unidade", selectbox(projetos.unidades(), 'ID_UNIDADE', 'NOME_UNIDADE') ),
                # controlGroup( "Ano", 'ano', projetos.anosReferencia() ),
                controlGroup( "Classificação CNPQ", "area", selectbox(projetos.areasTematicas(), 'ID_AREA', 'AREA_CNPQ') ),
                controlGroup( "Grupo CNPQ", "grupo", selectbox(projetos.grupoCNPQ(), 'ID_CLASSIFICACAO', 'GRUPO_CNPQ') ),
                INPUT(_value="Buscar",_type='submit'),
                _class="form-horizontal"
            )

    if form.process().accepted:
        try:
            filtros = form.vars

            # projetos = dbfunctions.getProjetos( queryFilter.getFilters() )
            table = ProjetosTable(projetos)

            return dict(form=form, results=table.printTable() )
        except Exception, e:
            raise e

    return dict(form=form, results=None )


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


@auth.requires_login() 
def api():
    """
    this is example of API with access control
    WEB2PY provides Hypermedia API (Collection+JSON) Experimental
    """
    from gluon.contrib.hypermedia import Collection
    rules = {
        '<tablename>': {'GET':{},'POST':{},'PUT':{},'DELETE':{}},
        }
    return Collection(db).process(request,response,rules)
