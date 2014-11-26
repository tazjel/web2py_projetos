# coding=utf-8
from datetime import datetime
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
        row.append(TD(content['DESCR_MAIL'] if content['DESCR_MAIL'] else "--", _class=self._bodyTRclass))
        row.append(TD(content['VINCULO'], _class=self._bodyTRclass))
        row.append(TD(formatedDate(content['DT_INICIAL']) + " a " + formatedDate(content['DT_FINAL']), _class=self._bodyTRclass))
        return row


class ProjetosTable(object):
    projetos = None
    _headTRclass = "dr-table-subheader rich-table-subheader tituloTabela"
    _headTDclass = "dr-table-subheadercell rich-table-subheadercell tituloTabela"
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
        heads = [TD(SPAN(title), _class=self._headTDclass) for title in self._titleList]
        return THEAD(TR(heads, _class=self._headTRclass))

    def getTableBody(self):
        return TBODY(self.getTableRows())

    def getTableRows(self):
        rows = []
        for projeto in self.projetos:
            rows.append(TR(self.getRowContent(projeto), _class="dr-table-firstrow rich-table-firstrow "))
        return rows

    def getRowContent(self, projeto):
        return [
            TD(A(projeto['TITULO'], _href=URL("projeto", "index", vars=dict(ID_PROJETO=projeto['ID_PROJETO']))),
               _class="dr-table-cell rich-table-cell"),
            TD(projeto['UNIDADE_RESPONSAVEL'], _class="dr-table-cell rich-table-cell"),
            TD(projeto['GRUPO_CNPQ'], _class="dr-table-cell rich-table-cell"),
            TD(projeto['COORDENADOR'], _class="dr-table-cell rich-table-cell"),
            TD(projeto['ANO_REFERENCIA'], _class="dr-table-cell rich-table-cell")
        ]
        #     TD(A("Detalhes", _href=URL("projeto", "index", vars=dict(ID_PROJETO=projeto['ID_PROJETO']))),
        #        _class="dr-table-cell rich-table-cell")



class ClassificacoesTable(DefaultTable):
    _headTRclass = "dr-table-subheader rich-table-subheader tituloTabela"
    _headTDclass = "dr-table-subheadercell rich-table-subheadercell tituloTabela"
    _bodyTRclass = "dr-table-firstrow rich-table-firstrow"
    _bodyTDclass = "dr-table-cell rich-table-cell"

    def __init__(self, contents, titleList=None):
        DefaultTable.__init__(self, contents, titleList)

    def getRowContent(self, content):
        return [
            TD(content['TIPO_CLASSIFICACAO'], _class=self._bodyTRclass),
            TD(content['CLASSIFICACAO'], _class=self._bodyTRclass)
        ]



class ResumoTable(object):
    projeto = None

    def __init__(self, projeto):
        self.projeto = projeto

    def printTable(self):
        return TABLE(self.printBody(), _class="table")

    def printBody(self):
        return TBODY(self.getTableRows())

    @property
    def emailCoordenador(self):
        email = self.projeto['DESCR_MAIL'] if self.projeto['DESCR_MAIL'] else "--"
        return "( " + email + " )"

    @property
    def vigencia(self):
        return formatedDate(self.projeto['DT_INICIAL']) + " a " + formatedDate(self.projeto['DT_FINAL'])

    def getTableRows(self):
        return [
            self.getRow(self.projeto['TITULO'], "Título"), self.getRow(self.projeto['RESUMO'], "Resumo"),
            self.getRow(self.projeto['UNIDADE_RESPONSAVEL'], "Unidade Responsável"),
            self.getRow(self.projeto['COORDENADOR'] + self.emailCoordenador, "Coordenador(a)"),
            self.getRow(self.projeto['DESCR_FUNDACAO'], "Fonte de Financiamento"),
            self.getRow(self.projeto['DESCR_SITUACAO'], "Situação do Projeto"),
            self.getRow(self.vigencia, "Vigência"),
            self.getRow(self.projeto['ANO_REFERENCIA'], "Ano de Referência"),
        ]

    def getRow(self, content, title):
        if not content:
            content = "Não cadastrado"
        return TR(TD(title), TD(SPAN(content, _class="textoForm")))


def formatedDate(date):
    return datetime.strptime(date, "%Y-%m-%d").strftime('%d/%m/%Y') if date else "--/--/----"