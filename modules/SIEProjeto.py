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
        path = "V_PROJETOS_UNIDADES"
        return self._sortedContent(path, "NOME_UNIDADE")

    def anosReferencia(self):
        path = "V_PROJETOS"
        fields = ["ANO_REFERENCIA"]
        return self._getContent(path)

    def areaConhecimento(self):
        path = "V_PROJETOS_AREAS_CONHECIMENTO"
        return self._sortedContent(path, "DESCRICAO")

    def grupoCNPQ(self):
        path = "V_PROJETOS_GRUPO_CNPQ"
        return self._sortedContent(path, "GRUPO_CNPQ")

    def getProjetos(self, filters):
        path = "V_PROJETOS"
        return self._getContent(path, filters)