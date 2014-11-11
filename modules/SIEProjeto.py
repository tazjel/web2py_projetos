from gluon import current
from unirio.api import UNIRIOAPIRequest


class SIEProjeto(object):
    def __init__(self):
        self.apiRequest = UNIRIOAPIRequest(current.kAPIKey)
        self.lmin = 0
        self.lmax = 100

