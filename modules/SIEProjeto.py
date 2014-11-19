# coding=utf-8
from gluon import current
from unirio.api import UNIRIOAPIRequest
from operator import itemgetter


class SIEProjeto(object):
    def __init__(self):
        self.apiRequest = UNIRIOAPIRequest(current.kAPIKey)
        self.lmin = 0
        self.lmax = 1000


    def _getContent(self, path, params={}, fields=[]):
        """

        :type params: dict
        """
        limits = {"LMIN" : self.lmin, "LMAX" : self.lmax}
        for k, v in params.items():
            params[k] = str(params[k]).upper()
        params.update(limits)

        api = self.apiRequest.performGETRequest(path, params, fields)
        return api.content

    def _sortedContent(self, path, key):
        return sorted(self._getContent(path), key=itemgetter(key))

    def areasTematicas(self):
        if not current.session.areasTematicas:
            current.session.areasTematicas = self._sortedContent("V_PROJETOS_AREAS_PESQUISA_CNPQ", 'AREA_CNPQ')
        return current.session.areasTematicas


    def unidades(self):
        if not current.session.unidades:
            current.session.unidades = self._sortedContent("V_PROJETOS_UNIDADES", "NOME_UNIDADE")
        return current.session.unidades

    def areasConhecimento(self):
        if not current.session.areasConhecimento:
            current.session.areasConhecimento = self._sortedContent("V_PROJETOS_AREAS_CONHECIMENTO", "DESCRICAO")
        return current.session.areasConhecimento

    def gruposCNPQ(self):
        if not current.session.gruposCNPQ:
            current.session.gruposCNPQ =  self._sortedContent("V_PROJETOS_GRUPO_CNPQ", "GRUPO_CNPQ")
        return current.session.gruposCNPQ

    def anos(self):
        if not current.session.anos:
            result = self._getContent("V_PROJETOS", {"SORT": "ANO_REFERENCIA"}, ["ANO_REFERENCIA"])
            anosUnicos = set(v["ANO_REFERENCIA"] for v in result)
            current.session.anos = [{"ANO_REFERENCIA": v} for v in anosUnicos]

        return current.session.anos

    def getProjetos(self, filters):
        """

        :rtype : list
        """
        if filters["participante"]:
            comParticipante = self.projetosWithParticipante(filters["participante"])
            if not current.session.allProjects:
                current.session.allProjects = self._sortedContent("V_PROJETOS", "ID_PROJETO")

            projetos = [p for p in current.session.allProjects if p["ID_PROJETO"] in comParticipante]
        else:
            projetos = self._getContent("V_PROJETOS", filters)

        return sorted(projetos, key=itemgetter("TITULO"))

    def projetosWithArea(self, area):
        pass

    def projetosWithParticipante(self, nome):
        """
        Metódo retorna uma lista com todos os projetos no qual o nome passado é participante

        :rtype : list
        :param nome: O nome ou parte de um nome de um participante
        :return: Uma lista de ID_PROJETO
        """
        result = self.apiRequest.performGETRequest(
            "V_PROJETOS_PARTICIPANTES",
            {"LMIN": 0, "LMAX": 1000, "NOME_PESSOA": nome},
            ["ID_PROJETO"]
        )
        return set(projeto["ID_PROJETO"] for projeto in result.content)

    def getParticipantes(self, filters):
        return self._getContent("V_PROJETOS_PARTICIPANTES", filters)