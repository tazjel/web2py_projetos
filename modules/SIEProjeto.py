# coding=utf-8
from gluon import current
from operator import itemgetter


class SIEProjeto(object):
    def __init__(self):
        self.apiRequest = current.api
        self.lmin = 0
        self.lmax = 1000
        self.cacheTime = 86400


    def _getContent(self, path, params={}, fields=[]):
        """

        :type params: dict
        """
        limits = {"LMIN" : self.lmin, "LMAX" : self.lmax}
        for k, v in params.items():
            params[k] = str(params[k]).upper()
        params.update(limits)
        try:
            return self.apiRequest.performGETRequest(path, params, fields, cached=self.cacheTime).content
        except AttributeError:
            return []

    def _sortedContent(self, path, key):
        return sorted(self._getContent(path), key=itemgetter(key))

    def areasTematicas(self):
        return self._sortedContent("V_PROJETOS_AREAS_PESQUISA_CNPQ", 'AREA_CNPQ')

    def unidades(self):
        return self._sortedContent("V_PROJETOS_UNIDADES", "NOME_UNIDADE")

    def areasConhecimento(self):
        return self._sortedContent("V_PROJETOS_AREAS_CONHECIMENTO", "DESCRICAO")

    def gruposCNPQ(self):
        return self._sortedContent("V_PROJETOS_GRUPO_CNPQ", "GRUPO_CNPQ")

    def anos(self):
        if not current.session.anos:
            result = self._getContent("V_PROJETOS", {"SORT": "ANO_REFERENCIA"}, ["ANO_REFERENCIA"])
            anosUnicos = set(v["ANO_REFERENCIA"] for v in result)
            current.session.anos = [{"ANO_REFERENCIA": v} for v in anosUnicos]

        return current.session.anos

    def classificacoes(self, ID_PROJETO):
        return self._getContent("V_PROJETOS_CLASSIFICACOES", {
            "ID_PROJETO": ID_PROJETO
        })

    def getProjetos(self, filters):
        """

        :rtype : list
        """
        if filters["participante"]:
            comParticipante = self.projetosWithParticipante(filters["participante"])
            allProjects = self._sortedContent("V_PROJETOS", "ID_PROJETO")
            projetos = [p for p in allProjects if p["ID_PROJETO"] in comParticipante]
        else:
            projetos = self._getContent("V_PROJETOS", filters)

        return sorted(projetos, key=itemgetter("TITULO"))

    def projetosWithArea(self, area):
        pass

    def projetosWithParticipante(self, nome):
        """
        Metódo retorna uma lista com todos os projetos no qual o nome passado é participante

        :type nome: str
        :rtype : list
        :param nome: O nome ou parte de um nome de um participante
        :return: Uma lista de ID_PROJETO
        """
        result = self.apiRequest.performGETRequest(
            "V_PROJETOS_PARTICIPANTES",
            {"LMIN": 0, "LMAX": 1000, "NOME_PESSOA": nome.upper()},
            ["ID_PROJETO"]
        )
        return set(projeto["ID_PROJETO"] for projeto in result.content)

    def getParticipantes(self, filters):
        return self._getContent("V_PROJETOS_PARTICIPANTES", filters)