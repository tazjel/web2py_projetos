# coding=utf-8
from gluon.html import *


class DefaultTable(object):
    contents = None
    _titleList = None
    _headTRclass = None
    _headTDclass = None
    _bodyTRclass = None
    _bodyTDclass = None

    def __init__(self, contents, titleList=None):
        self.contents = contents
        self._titleList = titleList

    def printTable(self, tableClass=None):
        return TABLE(self.getTableHead(), self.getTableBody(), _class=tableClass)

    # print THEAD(TR(TH('<hello>')), _class='test', _id=0)
    def getTableHead(self, tdClass=None, trClass=None):
        heads = []
        for title in self._titleList:
            heads.append(TD(SPAN(title), _class=self._headTDclass))
        return THEAD(TR(heads, _class=self._headTRclass))

    def getTableBody(self):
        return TBODY(self.getTableRows())

    def getTableRows(self):
        rows = []
        for content in self.contents:
            rows.append(TR(self.getRowContent(content), _class=self._bodyTRclass))
        return rows

    def getRowContent(self, content):
        pass


class ParticipantesTable(DefaultTable):
    _headTRclass = "dr-table-subheader rich-table-subheader tituloTabela"
    _headTDclass = "dr-table-subheadercell rich-table-subheadercell tituloTabela"
    _bodyTRclass = "dr-table-firstrow rich-table-firstrow"
    _bodyTDclass = "dr-table-cell rich-table-cell"

    def __init__(self, contents, titleList=None):
        DefaultTable.__init__(self, contents, titleList)

    def getRowContent(self, content):
        row = []
        row.append(TD(content['NOME_PESSOA'], _class=self._bodyTRclass))
        row.append(TD(content['FUNCAO'], _class=self._bodyTRclass))
        row.append(TD(content['DESCR_MAIL'], _class=self._bodyTRclass))
        row.append(TD(content['VINCULO'], _class=self._bodyTRclass))
        row.append(TD(str(content['DT_INICIAL']) + " a " + str(content['DT_FINAL']), _class=self._bodyTRclass))
        return row


class ProjetosTable(object):
    projetos = None
    _titleList = [
        'Título',
        'Unidade Responsável',
        'Grupo CNPQ',
        'Coordenador',
        'Data de Início'
        # 'Resumo'
    ]


    def __init__(self, projetos):
        self.projetos = projetos

    def printTable(self):
        return TABLE(self.getTableHead(), self.getTableBody(), _class="dr-table rich-table table table-striped")

    # print THEAD(TR(TH('<hello>')), _class='test', _id=0)
    def getTableHead(self):
        heads = []
        for title in self._titleList:
            heads.append(TD(SPAN(title), _class="dr-table-subheadercell rich-table-subheadercell tituloTabela"))
        return THEAD(TR(heads, _class="dr-table-subheader rich-table-subheader tituloTabela"))

    def getTableBody(self):
        return TBODY(self.getTableRows())

    def getTableRows(self):
        rows = []
        for projeto in self.projetos:
            rows.append(TR(self.getRowContent(projeto), _class="dr-table-firstrow rich-table-firstrow "))
        return rows

    def getRowContent(self, projeto):
        row = []
        row.append(TD(A(projeto['TITULO'], _href=URL("projeto", "index", vars=dict(ID_PROJETO=projeto['ID_PROJETO']))), _class="dr-table-cell rich-table-cell"))
        row.append(TD(projeto['UNIDADE_RESPONSAVEL'], _class="dr-table-cell rich-table-cell"))
        row.append(TD(projeto['GRUPO_CNPQ'], _class="dr-table-cell rich-table-cell"))
        row.append(TD(projeto['COORDENADOR'], _class="dr-table-cell rich-table-cell"))
        row.append(TD(projeto['ANO_REFERENCIA'], _class="dr-table-cell rich-table-cell"))
        # row.append(
        #     TD(A("Detalhes", _href=URL("projeto", "index", vars=dict(ID_PROJETO=projeto['ID_PROJETO']))),
        #        _class="dr-table-cell rich-table-cell"))
        return row


class ClassificacoesTable(DefaultTable):
    _headTRclass = "dr-table-subheader rich-table-subheader tituloTabela"
    _headTDclass = "dr-table-subheadercell rich-table-subheadercell tituloTabela"
    _bodyTRclass = "dr-table-firstrow rich-table-firstrow"
    _bodyTDclass = "dr-table-cell rich-table-cell"

    def __init__(self, contents, titleList=None):
        DefaultTable.__init__(self, contents, titleList)

    def getRowContent(self, content):
        row = []
        row.append(TD(content['TIPO_CLASSIFICACAO'], _class=self._bodyTRclass))
        row.append(TD(content['CLASSIFICACAO'], _class=self._bodyTRclass))
        return row


class ResumoTable(object):
    projeto = None

    def __init__(self, projeto):
        self.projeto = projeto

    def printTable(self):
        return TABLE(self.printBody(), _class="table")

    def printBody(self):
        return TBODY(self.getTableRows())

    def getTableRows(self):
        rows = []
        rows.append(self.getRow(self.projeto['TITULO'], "Título"))
        rows.append(self.getRow(self.projeto['RESUMO'], "Resumo"))
        rows.append(self.getRow(self.projeto['UNIDADE_RESPONSAVEL'], "Unidade Responsável"))
        rows.append(self.getRow(self.projeto['COORDENADOR'], "Coordenador(a)"))
        rows.append(self.getRow(self.projeto['DT_INICIAL'], "Data de Início"))
        rows.append(self.getRow(self.projeto['ANO_REFERENCIA'], "Ano de Referência"))
        rows.append(self.getRow(self.projeto['DESCR_MAIL'], "E-mail"))

        return rows

    def getRow(self, content, title):
        if not content:
            content = "Não cadastrado"
        return TR(TD(title), TD(SPAN(content, _class="textoForm")))