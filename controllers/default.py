# -*- coding: utf-8 -*-
import form

def index():
    form = FORM(
                forms.printControlGroup( "Título", "titulo", INPUT(_name="titulo") ),
                forms.printControlGroup( "Nome Participante", "participante", INPUT(_name="participante") ),
                forms.printControlGroup( "Unidade" , "unidade", forms.printProjetosUnidades() ),
                forms.printControlGroup( "Ano", 'ano', forms.printProjetosAnos() ),
                forms.printControlGroup( "Classificação CNPQ", "area", forms.printAreaConhecimento() ),
                forms.printControlGroup( "Grupo CNPQ", "grupo", forms.printGrupoCNPQ() ),
                INPUT(_value="Buscar",_type='submit'),
                _class="form-horizontal"
            )

    if form.process().accepted:
        try:
            filtros = form.vars
            queryFilter = QueryFilter(filtros)

            projetos = dbfunctions.getProjetos( queryFilter.getFilters() )
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
