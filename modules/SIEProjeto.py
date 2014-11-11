from gluon import current
from unirio.api import UNIRIOAPIRequest
from operator import itemgetter


class SIEProjeto(object):
    def __init__(self):
        self.apiRequest = UNIRIOAPIRequest(current.kAPIKey)
        self.lmin = 0
        self.lmax = 300


    def _getContent(self, path, params={}):
        """

        :type params: dict
        """
        limits = {"LMIN" : self.lmin, "LMAX" : self.lmax}
        for k, v in params.items():
            params[k] = str(params[k]).upper()
        params.update(limits)

        api = self.apiRequest.performGETRequest(path, params)
        return api.content

    def _sortedContent(self, path, key):
        return sorted(self._getContent(path), key=itemgetter(key))

    def areasTematicas(self):
        path = "V_PROJETOS_AREAS_PESQUISA_CNPQ"
        return self._sortedContent(path, 'AREA_CNPQ')


    def unidades(self):
        if current.session.unidades:
            return current.session.unidades
        current.session.unidades = self._sortedContent("V_PROJETOS_UNIDADES", "NOME_UNIDADE")
        return current.session.unidades

    def anosReferencia(self):
        path = "V_PROJETOS"
        fields = ["ANO_REFERENCIA"]
        return self._getContent(path)

    def areasConhecimento(self):
        if current.session.areasConhecimento:
            return current.session.areasConhecimento
        current.session.areasConhecimento = self._sortedContent("V_PROJETOS_AREAS_CONHECIMENTO", "DESCRICAO")
        return current.session.areasConhecimento

    def gruposCNPQ(self):
        if current.session.gruposCNPQ:
            return current.session.gruposCNPQ
        current.session.gruposCNPQ =  self._sortedContent("V_PROJETOS_GRUPO_CNPQ", "GRUPO_CNPQ")
        return current.session.gruposCNPQ

    def getProjetos(self, filters):
        return self._getContent("V_PROJETOS", filters)